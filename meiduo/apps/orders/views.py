"""
需求：
    提交订单页面的展示
前端：
        发送一个axios请求来获取 地址信息和购物车中选中商品的信息
后端：
    请求：         必须是登录用户才可以访问
    业务逻辑：      地址信息，购物车中选中商品的信息
    响应：         JSON
    路由：
            GET     orders/settlement/
    步骤：

        1.获取用户信息
        2.地址信息
            2.1 查询用户的地址信息 [Address,Address,...]
            2.2 将对象数据转换为字典数据
        3.购物车中选中商品的信息
            3.1 连接redis
            3.2 hash        {sku_id:count,sku_id:count}
            3.3 set         [1,2]
            3.4 重新组织一个 选中的信息
            3.5 根据商品的id 查询商品的具体信息 [SKU,SKU,SKu...]
            3.6 需要将对象数据转换为字典数据
"""

import json
from apps.orders.models import OrderInfo, OrderGoods
from django.views import View
from utils.views import LoginRequiredJSONMixin
from apps.users.models import Address
from django_redis import get_redis_connection
from apps.goods.models import SKU
from django.http import JsonResponse
from django.db import transaction


class OrderSettlementView(LoginRequiredJSONMixin, View):
    def get(self, request):
        # 获取用户信息
        user = request.user
        # 查询用户地址
        addresses = Address.objects.filter(is_deleted=False)
        # 将对象数据转为字典数据
        addresses_list = []
        for address in addresses:
            addresses_list.append({
                'id': address.id,
                'province': address.province.name,
                'city': address.city.name,
                'district': address.district.name,
                'place': address.place,
                'receiver': address.receiver,
                'mobile': address.mobile,
            })
        # 购物车选中的商品信息
        # 连接redis
        redis_cli = get_redis_connection('carts')
        pipeline = redis_cli.pipeline()
        pipeline.hgetall(f'carts_{user.id}')
        pipeline.smembers(f'selected_{user.id}')
        result = pipeline.execute()
        sku_id_count = result[0]
        selected_ids = result[1]
        selected_carts = {}
        for sku_id in selected_ids:
            selected_carts[int(sku_id)] = int(sku_id_count[sku_id])
        sku_list = []
        for sku_id, count in selected_carts.items():
            sku = SKU.objects.get(pk=sku_id)
            sku_list.append({
                'id': sku.id,
                'name': sku.name,
                'count': count,
                'default_image_url': sku.default_image.url,
                'price': sku.price,
            })

        # 运费
        from decimal import Decimal
        freight = Decimal('100')
        """
        float double
        decimal --货币类型
        01010101
        整数
        小数的保存 特殊
        12.5
        12  0.5
        1100  1
        12.33
        0.33
        100 / 3 = 33.33
        33.33   33.33     33.34
        """
        context = {
            'skus': sku_list,
            'addresses': addresses_list,
            'freight': freight  # 运费
        }
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'context': context})


class OrderCommitView(LoginRequiredJSONMixin, View):
    def post(self, request):
        user = request.user
        # 1.接受请求
        data = json.loads(request.body.decode())
        address_id = data.get('address_id')
        pay_method = data.get('pay_method')

        # 2.验证数据
        if not all([address_id, pay_method]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        try:
            address = Address.objects.get(id=address_id)
        except Address.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '参数不正确'})

        if pay_method not in [OrderInfo.PAY_METHODS_ENUM['CASH'], OrderInfo.PAY_METHODS_ENUM['ALIPAY']]:
            return JsonResponse({'code': 400, 'errmsg': '参数不正确'})

        from django.utils import timezone
        order_id = timezone.localtime().strftime('%Y%m%d%H%M%S%f') + '%09d' % user.id
        from datetime import datetime
        # order_id = datetime.strptime('%Y%m%d%H%M%S') + '%09d' % user.id

        if pay_method == OrderInfo.PAY_METHODS_ENUM['CASH']:
            status = OrderInfo.ORDER_STATUS_ENUM['UNSEND']
        else:
            status = OrderInfo.ORDER_STATUS_ENUM['UNPAID']

        total_count = 0
        from decimal import Decimal
        total_amount = Decimal('0')
        # 运费
        freight = Decimal('10.00')

        # 事务 要么全部成功，要么全部失败
        with transaction.atomic():
            # 事务开始点
            point = transaction.savepoint()
            orderinfo = OrderInfo.objects.create(
                order_id=order_id,
                user=user,
                address=address,
                total_count=total_count,
                total_amount=total_amount,
                freight=freight,
                pay_method=pay_method,
                status=status
            )
            # 连接redis
            redis_cli = get_redis_connection('carts')
            sku_id_counts = redis_cli.hgetall(f'carts_{user.id}')
            selected_ids = redis_cli.smembers(f'selected_{user.id}')
            carts = {}
            for sku_id in selected_ids:
                carts[int(sku_id)] = int(sku_id_counts[sku_id])
            for sku_id, count in carts.items():
                while True:
                    sku = SKU.objects.get(id=sku_id)
                    if sku.stock < count:
                        # 事务回滚点
                        transaction.savepoint_rollback(point)
                        return JsonResponse({'code': 400, 'errmsg': '库存不足'})
                    # from time import sleep
                    # sleep(5)

                    # sku.stock -= count
                    # sku.sales += count
                    # sku.save()
                    old_stock = sku.stock
                    new_stock = sku.stock - count
                    new_sales = sku.sales + count
                    result = SKU.objects.filter(id=sku_id, stock=old_stock).update(stock=new_stock, sales=new_sales)
                    if result == 0:
                        continue
                        # transaction.savepoint_rollback(point)
                        # return JsonResponse({'code': 400, 'errmsg': '下单失败---'})

                    # 累加总数量和总金额
                    orderinfo.total_count += count
                    orderinfo.total_amount += (count * sku.price)

                    # 保存订单信息
                    OrderGoods.objects.create(
                        order=orderinfo,
                        sku=sku,
                        count=count,
                        price=sku.price
                    )
                    break
            orderinfo.save()
            # 事务提交点
            transaction.savepoint_commit(point)
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'order_id': order_id})


'''
sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
transaction-isolation=READ-COMMITTED
sudo service mysql restart
'''

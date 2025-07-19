import json
import pickle
import base64

from django.http import JsonResponse
from django.views import View
from django_redis import get_redis_connection
from apps.goods.models import SKU


class CartsView(View):
    def post(self, request):
        data = json.loads(request.body.decode())
        sku_id = data.get('sku_id')
        count = data.get('count')

        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '查无此商品'})
        try:
            count = int(count)
        except Exception:
            count = 1
        user = request.user
        if user.is_authenticated:
            redis_cli = get_redis_connection('carts')
            # redis 优化
            pipeline = redis_cli.pipeline()
            # hincrby 进行累加操作
            pipeline.hincrby(f'carts_{user.id}', sku_id, count)
            # 操作set
            pipeline.sadd(f'selected_{user.id}', sku_id)
            # 执行pipeline
            pipeline.execute()

            # redis_cli.hset(f'carts_{user.id}', sku_id, count)
            # redis_cli.sadd(f'selected_{user.id}', sku_id)
            return JsonResponse({'code': 0, 'errmsg': 'ok'})
        else:
            # carts = {
            #     sku_id: {
            #         'count': count,
            #         'selected': True
            #     }
            # }

            cookie_carts = request.COOKIES.get('carts')
            if cookie_carts:
                carts = pickle.loads(base64.b64decode(cookie_carts))
            else:
                carts = {}

            if sku_id in carts:
                origin_count = carts[sku_id]['count']
                count += origin_count
            carts[sku_id] = {
                'count': count,
                'selected': True
            }

            carts_bytes = pickle.dumps(carts)
            base64encode = base64.b64encode(carts_bytes)
            response = JsonResponse({'code': 0, 'errmsg': 'ok'})
            response.set_cookie('carts', base64encode.decode(), max_age=3600 * 24 * 12)
            return response

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            redis_cli = get_redis_connection('carts')
            sku_id_counts = redis_cli.hgetall('carts_%s' % user.id)
            selected_ids = redis_cli.smembers('selected_%s' % user.id)
            carts = {}

            for sku_id, count in sku_id_counts.items():
                carts[int(sku_id)] = {
                    'count': int(count),
                    'selected': sku_id in selected_ids
                }
        else:
            cookie_carts = request.COOKIES.get('carts')
            if cookie_carts is not None:
                carts = pickle.loads(base64.b64decode(cookie_carts))
            else:
                carts = {}
        sku_ids = carts.keys()
        skus = SKU.objects.filter(id__in=sku_ids)
        sku_list = []
        for sku in skus:
            sku_list.append({
                'id': sku.id,
                'price': sku.price,
                'name': sku.name,
                'default_image_url': sku.default_image.url,
                'selected': carts[sku.id]['selected'],  # 选中状态
                'count': int(carts[sku.id]['count']),  # 数量
                'amount': sku.price * carts[sku.id]['count']  # 总价格
            })
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'cart_skus': sku_list})

    def put(self, request):
        # 1.获取用户信息
        user = request.user
        # 2.接受数据
        data = json.loads(request.body.decode())
        sku_id = data.get('sku_id')
        count = data.get('count')
        selected = data.get('selected')
        # 3.验证数据
        if not all([sku_id, count]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        try:
            SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '没有次商品'})
        try:
            count = int(count)
        except Exception:
            count = 1

        if user.is_authenticated:
            # 登录用户跟新redis
            # 连接redis
            redis_cli = get_redis_connection('carts')
            redis_cli.hset(f'carts_{user.id}', sku_id, count)
            if selected:
                redis_cli.sadd(f'selected_{user.id}', sku_id)
            else:
                redis_cli.srem(f'selected_{user.id}', sku_id)
            return JsonResponse({'code': 0, 'errmsg': 'ok', 'cart_sku': {'count': count, 'selected': selected}})
        else:
            # 未登录用户更新cookie
            # 先读取购物车数据
            cookie_cart = request.COOKIES.get('carts')
            # 判断有没有
            if cookie_cart is not None:
                # 有数据则解密数据
                carts = pickle.loads(base64.b64decode(cookie_cart))
            else:
                # 没有则初始化一个空字典
                carts = {}
            # 更新数据
            if sku_id in carts:
                carts[sku_id] = {
                    'count': count,
                    'selected': selected
                }
            # 新字典进行编码和base64加密
            new_carts = base64.b64encode(pickle.dumps(carts))
            # cookie
            response = JsonResponse({'code': 0, 'errmsg': 'ok', 'cart_sku': {'count': count, 'selected': selected}})
            response.set_cookie('carts', new_carts.decode(), max_age=14 * 24 * 3600)
            return response

    def delete(self, request):
        # 1.接收请求
        data = json.loads(request.body.decode())
        # 2.验证参数
        sku_id = data.get('sku_id')
        try:
            SKU.objects.get(pk=sku_id)
        except SKU.objects.get(pk=sku_id):
            return JsonResponse({'code': 400, 'errmsg': '没有此商品'})
        # 3.根据用户状态
        user = request.user
        if user.is_authenticated:
            # 4.登录用户操作redis
            #     4.1 连接redis
            redis_cli = get_redis_connection('carts')
            #     4.2 hash
            redis_cli.hdel(f'carts_{user.id}', sku_id)
            #     4.3 set
            redis_cli.srem(f'selected_{user.id}', sku_id)
            #     4.4 返回响应
            return JsonResponse({'code': 400, 'errmsg': 'ok'})
        else:
            # 5.未登录用户操作cookie
            #     5.1 读取cookie中的购物车数据
            cookie_cart = request.COOKIES.get('carts')
            #     判断数据是否存在
            if cookie_cart is not None:
                #     存在则解码
                carts = pickle.loads(base64.b64decode(cookie_cart))
            else:
                # 不存在则初始化字典
                carts = {}
            #     5.2 删除数据 {}
            del carts[sku_id]
            #     5.3 我们需要对字典数据进行编码和base64的处理
            new_carts = base64.b64encode(pickle.dumps(carts))
            #     5.4 设置cookie
            response = JsonResponse({'code': 0, 'errmsg': 'ok'})
            response.set_cookie('carts', new_carts.decode(), max_age=14 * 24 * 3600)
            #     5.5 返回响应
            return response


class CartsSimpleView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            # 用户已登录
            redis_cli = get_redis_connection('carts')
            redis_cart = redis_cli.hgetall(f'carts_{user.id}')
            cart_selected = redis_cli.smembers(f'selected_{user.id}')
            cart_dict = {}
            for sku_id, count in redis_cart.items():
                cart_dict[int(sku_id)] = {
                    'count': int(count),
                    'selected': sku_id in cart_selected
                }
        else:
            # 用户未登录
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                cart_dict = {}

        # 构造简单购物车json数据
        cart_skus = []
        sku_ids = cart_dict.keys()
        skus = SKU.objects.filter(id__in=sku_ids)
        for sku in skus:
            cart_skus.append({
                'id': sku.id,
                'name': sku.name,
                'count': cart_dict.get(sku.id).get('count'),
                'default_image_url': sku.default_image.url
            })
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'cart_skus': cart_skus})

"""
需求:
    当用户点击去支付按钮的时候,要后端生成一个跳转的连接

前端:
        axios 请求. 携带 订单id
后端:

    请求:             获取订单id
    业务逻辑:          生成支付宝链接(读取文档)
                    读取应用私钥和支付宝公钥
                    创建支付宝实例,调用支付宝的方法
                    拼接连接
    响应:
    路由:     GET    payment/order_id/
    步骤:
        1. 获取订单id
        2. 验证订单id (根据订单id查询订单信息)
        3. 读取应用私钥和支付宝公钥
        4. 创建支付宝实例
        5. 调用支付宝的支付方法
        6.  拼接连接
        7. 返回响应

"""

from django.views import View
from apps.orders.models import OrderInfo
from utils.views import LoginRequiredJSONMixin
from django.http import JsonResponse
from meiduo_mall import settings
# from alipay import AliPay, AliPayConfig
from apps.pay.models import Payment


class PayUrlView(LoginRequiredJSONMixin, View):
    def get(self, request, order_id):
        user = request.user
        try:
            order = OrderInfo.objects.get(
                order_id=order_id,
                status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'],
                user=user
            )
        except OrderInfo.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '没有此订单'})
        # 读取应用私钥和支付宝公钥
        app_private_key_string = open(settings.APP_PRIVATE_KEY_PATH).read()
        alipay_public_key_string = open(settings.ALIPAY_PUBLIC_KEY_PATH).read()

        # alipay = AliPay(
        #     appid=settings.ALIPAY_APPID,
        #     app_notify_url=settings.ALIPAY_RETURN_URL,  # 默认回调url
        #     app_private_key_string=app_private_key_string,
        #     # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        #     alipay_public_key_string=alipay_public_key_string,
        #     sign_type="RSA2",  # RSA 或者 RSA2
        #     debug=settings.ALIPAY_DEBUG,  # 默认False
        #     config=AliPayConfig(timeout=15)  # 可选, 请求超时时间
        # )

        #
        subject = '美多商城测试订单'
        # order_string = alipay.api_alipay_trade_page_pay(
        #     out_trade_no=order_id,
        #     total_amount=str(order.total_amount),  # 一定要进行类型转换,因为decimal不是基本数据类型
        #     subject=subject,
        #     return_url=settings.ALIPAY_RETURN_URL,  # 支付成功之后,跳转的页面
        #     notify_url=settings.ALIPAY_RETURN_URL  # 可选, 不填则使用默认notify url
        # )
        # 拼接连接
        # pay_url = 'https://openapi-sandbox.dl.alipaydev.com/gateway.do?' + order_string
        # return JsonResponse({'code': 0, 'errmsg': 'ok', 'alipay_url': pay_url})


class PaymentStatusView(View):
    def put(self, request):
        # 1.接受数据
        data = request.GET
        # 2.查询字符串转换为字典 验证数据
        data = data.dict()
        # 验证没有问题获取支付宝交易流水号
        signature = data.pop('sign')

        app_private_key_string = open(settings.APP_PRIVATE_KEY_PATH).read()
        alipay_public_key_string = open(settings.ALIPAY_PUBLIC_KEY_PATH).read()

        # 创建支付宝实例
        # alipay = AliPay(
        #     appid=settings.ALIPAY_APPID,
        #     app_notify_url=None,  # 默认回调url
        #     app_private_key_string=app_private_key_string,
        #     # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        #     alipay_public_key_string=alipay_public_key_string,
        #     sign_type="RSA2",  # RSA 或者 RSA2
        #     debug=settings.ALIPAY_DEBUG,  # 默认False
        #     config=AliPayConfig(timeout=15)  # 可选, 请求超时时间
        # )
        # success = alipay.verify(data, signature)
        #
        # if success:
        #     trade_no = data.get('trade_no')
        #     order_id = data.get('out_trade_no')
        #     Payment.objects.create(
        #         trade_id=trade_no,
        #         order_id=order_id
        #     )
        #     # 改变订单状态
        #     OrderInfo.objects.filter(order_id=order_id).update(status=OrderInfo.ORDER_STATUS_ENUM['UNSEND'])
        #     return JsonResponse({'code': 0, 'errmsg': 'ok', 'trade_id': trade_no})
        # else:
        #     return JsonResponse({'code': 400, 'errmsg': '请到个人中心的订单中查询订单状态'})

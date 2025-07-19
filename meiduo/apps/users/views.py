import json
import re
from django.views import View
from django_redis import get_redis_connection
from apps.goods.models import SKU
from apps.users.models import User, Address
from django.http import JsonResponse
from django.contrib.auth import login  # 状态保持
from django.contrib.auth import logout
from utils.views import LoginRequiredMixin, LoginRequiredJSONMixin

from rest_framework.views import APIView
from rest_framework.response import Response


class UsernameCountView(APIView):
    """
    获取指定用户名存在的数量
    """

    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        data = {'code': 0, 'count': count, 'errmsg': 'ok'}
        return Response(data)


# class UsernameCountView(View):
#     def get(self, request, username):
#         count = User.objects.filter(username=username).count()
#         return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})


class RegisterView(View):
    def post(self, request):
        body_bytes = request.body
        body_str = body_bytes.decode()
        body_dict = json.loads(body_str)

        username = body_dict.get('username')
        password = body_dict.get('password')
        password2 = body_dict.get('password2')
        # mobile = body_dict.get('mobile')
        allow = body_dict.get('allow')

        if not all([username, password, password2, allow]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        if not re.match('[a-zA-Z_-]{5,20}', username):
            return JsonResponse({'code': 400, 'errmsg': '用户名不满足规则'})
        # user = User.objects.create(username=username, password=password, mobile=mobile)  密码不加密
        # create_user 密码加密
        user = User.objects.create_user(username=username, password=password)

        login(request, user)  # 状态保持

        return JsonResponse({'code': 0, 'errmsg': 'ok'})


class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        remembered = data.get('remembered')

        if not all([username, password]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})

        # 判断是根据手机号查询 还是 根据用户名查询
        if re.match('1[3-9]\d{9}', username):
            User.USERNAME_FIELD = 'mobile'
        else:
            User.USERNAME_FIELD = 'username'

        from django.contrib.auth import authenticate

        user = authenticate(username=username, password=password)

        if user is None:
            return JsonResponse({'code': 400, 'errmsg': '账号或密码错误'})
        from django.contrib.auth import login
        login(request, user)

        if remembered:
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)
        # 首页用户信息的展示
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.set_cookie('username', username)

        # 合并cookie数据道redis中，必须是登录后合并
        from apps.carts.utils import merge_cookie_to_redis
        response = merge_cookie_to_redis(request, response)
        return response


class LogoutView(View):
    def delete(self, request):
        """
        405 前后端请求方法不一样
        WARNING base 146 Method Not Allowed (DELETE): /logout/
        WARNING logs 241 Method Not Allowed: /logout/
        WARNING basehttp 212 "DELETE /logout/ HTTP/1.1" 405 0
        """
        # 删除session信息
        logout(request)
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        #  2. 删除cookie信息,因为前端是根据cookie信息来判断用户是否登录的
        response.delete_cookie('username')
        return response


class CenterView(LoginRequiredMixin, View):
    def get(self, request):
        info_data = {
            'username': request.user.username,
            'email': request.user.email,
            'mobile': request.user.mobile,
            'email_active': request.user.email_active,
        }
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'info_data': info_data})


class EmailView(View):
    def put(self, request):
        data = json.loads(request.body)
        email = data.get('email')
        user = request.user
        user.email = email
        user.save()
        # 发送激活邮件
        subject = "美多商城激活邮件"
        message = ""
        from_email = "美多商城<zjx_py@163.com>"
        recipient_list = ['zjx_py@163.com']
        from utils.email_verify import generic_email_verify_token
        token = generic_email_verify_token(request.user.id)
        # html_message = "点击按钮进行激活<a href='https://www.itcast.cn/?token=%s'>激活</a>" % token
        verify_url = f"http://www.meiduo.site:8080/success_verify_email.html?token={token}"

        html_message = '<p>尊敬的用户您好！</p>' \
                       '<p>感谢您使用美多商城。</p>' \
                       '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                       '<p><a href="%s">%s<a></p>' % (email, verify_url, verify_url)
        # from django.core.mail import send_mail
        # send_mail(
        #     subject=subject,
        #     message=message,
        #     from_email=from_email,
        #     recipient_list=recipient_list,
        #     html_message=html_message
        # )
        from celery_tasks.email.tasks import celery_send_email
        celery_send_email.delay(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message
        )

        return JsonResponse({'code': 0, 'errmsg': 'ok'})


class EmailVerifyView(View):
    def put(self, request):
        params = request.GET
        token = params.get('token')
        if token is None:
            return JsonResponse({'code': 400, 'errmsg': '参数确实'})
        from utils.email_verify import check_verify_token
        user_id = check_verify_token(token)
        if user_id is None:
            return JsonResponse({'code': 400, 'errmsg': '参数错误'})
        user = User.objects.get(id=user_id)
        user.email_active = True
        user.save()
        return JsonResponse({'code': 0, 'errmsg': 'ok'})


class AddressCreateView(LoginRequiredJSONMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        # 2.获取参数，验证参数
        receiver = data.get('receiver')
        province_id = data.get('province_id')
        city_id = data.get('city_id')
        district_id = data.get('district_id')
        place = data.get('place')
        mobile = data.get('mobile')
        tel = data.get('tel')
        email = data.get('email')
        user = request.user

        # 3.数据入库
        address = Address.objects.create(
            user=user,
            title=receiver,
            receiver=receiver,
            province_id=province_id,
            city_id=city_id,
            district_id=district_id,
            place=place,
            mobile=mobile,
            tel=tel,
            email=email
        )

        address_dict = {
            'id': address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }

        # 4.返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'address': address_dict})


class AddressView(LoginRequiredJSONMixin, View):
    def get(self, request):
        # 1.查询指定数据
        user = request.user
        # addresses=user.addresses
        addresses = Address.objects.filter(user=user, is_deleted=False)
        # 2.将对象数据转换为字典数据
        address_list = []
        for address in addresses:
            address_list.append({
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            })
        # 3.返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'addresses': address_list})

    def put(self, request, id):
        """
        修改收货地址
        """


"""
一 根据页面效果，分析需求（细心+经验）
    1. 最近浏览记录 只有登录用户才可以访问。 我们只记录登录用户的浏览记录
    2. 浏览记录应该有顺序
    3. 没有分页
二  功能
① 在用户访问商品详情的时候， 添加浏览记录
② 在个人中心，展示浏览记录

三 分析
问题1： 保存哪些数据？ 用户id，商品id,顺序（访问时间）
问题2： 保存在哪里？   一般要保存在数据库 （缺点： ① 慢 ② 频繁操作数据库） 授课
                    最好保存在redis中

都可以。看公司具体的安排。 服务器内存比较大。 mysql + redis  


user_id,sku_id,顺序

key: value

redis:
    string:   x  
    hash:     x 
    list:     v  
    set:      x  
    zset:     v 
            权重：值
"""

"""
添加浏览记录
    前端：
            当登录用户，访问某一个具体SKU页面的时候，发送一个axios请求。 请求携带 sku_id
    后端：
         请求：        接收请求，获取请求参数，验证参数
         业务逻辑；    连接redis，先去重，在保存到redsi中，只保存5条记录
         响应：        返回JSON

        路由：     POST        browse_histories 
        步骤：
            1. 接收请求
            2. 获取请求参数
            3. 验证参数
            4. 连接redis    list
            5. 去重
            6. 保存到redsi中
            7. 只保存5条记录
            8. 返回JSON
展示浏览记录
"""


class UserHistoryView(LoginRequiredJSONMixin, View):
    def post(self, request):
        user = request.user
        data = json.loads(request.body.decode())
        sku_id = data.get('sku_id')
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '没有此商品'})
        redis_cli = get_redis_connection('history')
        redis_cli.lrem(f'history_{user.id}', 0, sku_id)
        redis_cli.lpush(f'history_{user.id}', sku_id)
        redis_cli.ltrim(f'history_{user.id}', 0, 4)
        return JsonResponse({'code': 0, 'errmsg': 'ok'})

    def get(self, request):
        redis_cli = get_redis_connection('history')
        ids = redis_cli.lrange(f'history_{request.user.id}', 0, 4)
        history_list = []
        for sku_id in ids:
            sku = SKU.objects.get(id=sku_id)
            history_list.append({
                'id': int(sku_id),
                'name': sku.name,
                'default_image_url': sku.default_image.url,
                'price': sku.price
            })
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'skus': history_list})

from django.views import View
from django.http import HttpResponse, JsonResponse
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
import random
from libs.rlyun import send_sms_code
from celery_tasks.sms.tasks import celery_send_sms_code


class ImageCodeView(View):
    def get(self, request, uuid):
        text, image = captcha.generate_captcha()
        redis_cli = get_redis_connection('code')
        redis_cli.setex(uuid, 100, text)
        return HttpResponse(image, content_type='image/jpeg')


class SmsCodeView(View):
    def get(self, request, mobile):
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')
        if not all([image_code, uuid]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        redis_cli = get_redis_connection('code')
        redis_image_code = redis_cli.get(uuid)
        if redis_image_code is None:
            return JsonResponse({'code': 400, 'errmsg': '图片验证码已过期'})
        if redis_image_code.decode().casefold() != image_code.casefold():
            return JsonResponse({'code': 400, 'errmsg': '图片验证码已过期'})
        send_flag = redis_cli.get('send_flag_%s' % mobile)
        if send_flag is not None:
            return JsonResponse({'code': 400, 'errmsg': '不要频繁发送短信'})
        sms_code = random.randint(1000, 9999)

        # redis管道 3步
        # 新建一个管道
        pipeline = redis_cli.pipeline()
        # 管道收集指令
        pipeline.setex(mobile, 300, sms_code)
        pipeline.setex('send_flag_%s' % mobile, 60, 1)
        #  管道执行指令
        pipeline.execute()

        # send_sms_code.send_code(mobile, sms_code)
        celery_send_sms_code.delay(mobile, sms_code)
        return JsonResponse({'code': 0, 'errmsg': 'ok'})

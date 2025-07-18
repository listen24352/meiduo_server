from celery_tasks.main import app
from libs.rlyun import send_sms_code


@app.task
def celery_send_sms_code(mobile, code):
    send_sms_code.send_code(mobile, code)

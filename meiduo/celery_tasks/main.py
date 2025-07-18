import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.settings')

app = Celery('celery_tasks')
app.config_from_object('celery_tasks.config')
app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.email'])

# 在base_dir 启动celery命令 celery -A celery_tasks.main worker -l INFO

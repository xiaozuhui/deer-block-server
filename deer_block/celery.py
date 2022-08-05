import os

import django
from celery import Celery
from django.conf import settings

# 设置系统环境变量，安装django，必须设置，否则在启动celery时会报错
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deer_block.settings')
django.setup()

celery_app = Celery('deer_block')
celery_app.config_from_object('django.conf:settings')
celery_app.autodiscover_tasks(['apps.celerytask'], related_name="*_task")

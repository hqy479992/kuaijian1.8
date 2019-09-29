from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

#为celery设置默认的django设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE','proj.settings')

app=Celery('laboratory')

#namespace='CELERY'意思是和celery相关的配置键。前缀都要有'CELERY_'开头
app.config_from_object('django.conf:settings',namespace='CELERY')

#在工程下的所有app下自动加载每一个的task
app.autodiscover_tasks()

#maybe debug?
@app.task(bind=True)
def debug_task(self):
	print('Request: {0!r}'.format(self.request))
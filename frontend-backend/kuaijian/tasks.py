from __future__ import absolute_import
from celery import shared_task


@shared_task
def testCelery(task_name,video_list,config,audio_list):
	print(task_name,'\n',
			video_list,'\n',
			config,'\n',
			audio_list)
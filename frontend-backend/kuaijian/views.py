import os,cv2,shutil
import threading
from django.http import HttpResponse,StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import simplejson as json
from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie
from kuaijian.tasks import testCelery

# Create your views here.
#文件内全局变量
task_name=''
audio_list=[]
video_list=[]
config={
	'window_size_0':0,
	'window_size_1':150,       #后面也都默认150
	'min_output_duration_0':10,
	'min_output_duration_1':10,
	'max_output_duration_0':15,
	'max_output_duration_1':20,#后面都默认20
	'head_duration':10,
	'tail_duration':10
}

#此变量与前端globalvar.js中的only_audio_suffix一致
audiosuffix=['.wav','.flac','.ape','.m4a','.wv',
						'.mp3','.m4b','.m4p','.m4r','.m4v',
						'.aac','.opus']

videosuffix=['.flv','.avi','.wmv','asf','.wmvhd',
				'.dat','.vob','.mpg','.mpeg',
				'.mp4','3gp','.3g2','.mkv','rm',
				'.rmvb','.mov','.qt','.ogg',
				'.ogv','.oga','.mod']

#界面
def indexhtml(request):
	return render(request,'index.html')
def guidehtml(request):
	return render(request,'guide.html')
def questionhtml(request):
	return render(request,'question.html')
def todohtml(request):
	return render(request,'todo.html')
def doinghtml(request):
	return render(request,'doing.html')
def donehtml(request):
	mvtojpg('static/resultfiles')
	return render(request,'done.html')
def aboutushtml(request):
	return render(request,'aboutus.html')
def contactushtml(request):
	return render(request,'contactus.html')
def settingshtml(request):
	return render(request,'settings.html')
def navbarhtml(request):
	return render(request,'navbar.html')
def headerhtml(request):
	return render(request,'header.html')

#数据传递
#index界面
@require_http_methods(['POST'])
@ensure_csrf_cookie
def uploadfile(request):
	try:
		obj=request.FILES
		filelist=obj.getlist('file')
		pathlist=request.POST.getlist('path')
		if not filelist:
			return HttpResponse('error')
		else:
			for file in filelist:
				position=os.path.join(os.path.join(os.getcwd(),'static/uploadfiles'),
										'/'.join(pathlist[filelist.index(file)].split('/')[:-1]))
				if not os.path.exists(position):
					os.makedirs(position)
				stroage=open(position+'/'+file.name,'wb+')
				for chunk in file.chunks():
					stroage.write(chunk)
				stroage.close()
		mvtojpg('static/uploadfiles')
		return HttpResponse('success')
	except:
		return HttpResponse('error')

#todo界面
@require_http_methods(['POST'])
@ensure_csrf_cookie
def getdirsbyupload(request):
	try:
		return HttpResponse(get_pathSuffixDict('static/uploadfiles'))
	except:
		return HttpResponse('error')

@require_http_methods(['POST'])
@ensure_csrf_cookie
def synfolderlist(request):
	global audio_list,video_list,audiosuffix,videosuffix
	try:
		obj=json.loads(request.body.decode())
		#如果有单独的音频文件夹
		if obj['audioByVideo']==False:
			#音频列表
			filelistindir(os.path.join('static/uploadfiles',obj['audioFolder']),audio_list,audiosuffix)
			obj['videoAudiolist'].remove(obj['audioFolder'])
		else:
			#音频列表
			filelistindir(os.path.join('static/uploadfiles',obj['audioFolder']),audio_list,videosuffix)
		#视频列表
		for i in range(0,len(obj['videoAudiolist'])):
			tem_video_list=[]
			filelistindir(os.path.join('static/uploadfiles',obj['videoAudiolist'][i]),tem_video_list,videosuffix)
			video_list.append(tem_video_list)
		return HttpResponse('success')
	except Exception as e:
		raise e
		return HttpResponse('error')

@require_http_methods(['POST'])
@ensure_csrf_cookie
def deletefile(request):
	global videosuffix
	try:
		obj=json.loads(request.body.decode())
		deletefilename=obj['deletefilename']
		nowfolder=obj['nowfolder']
		path='static/uploadfiles' #即static
		if os.path.isdir(os.path.join(path,deletefilename)):
			shutil.rmtree(os.path.join(os.getcwd(),path,deletefilename))
		elif os.path.splitext(deletefilename)[1] in videosuffix:
			os.remove(os.path.join(path,deletefilename))
			os.remove(os.path.join(path,os.path.splitext(deletefilename)[0]+'mvtojpg.jpg'))
		else:
			os.remove(os.path.join(path,deletefilename))
		return HttpResponse(get_pathSuffixDict(os.path.join(path,nowfolder)))
	except:
		return HttpResponse('error')

@require_http_methods(['POST'])
@ensure_csrf_cookie
def renamefile(request):
	global videosuffix
	try:
		obj=json.loads(request.body.decode())
		originname=obj['originname']
		nowfolder=obj['nowfolder']
		newname=obj['newname']
		path='static/uploadfiles'
		#如果是视频的话，需要第一帧图片和视频两个都重命名
		os.rename(os.path.join(path,originname),
					os.path.join(path,nowfolder,newname+os.path.splitext(originname)[1]))
		if os.path.splitext(originname)[1] in videosuffix:
			os.rename(os.path.join(path,os.path.splitext(originname)[0]+'mvtojpg.jpg'),
						os.path.join(path,nowfolder,newname+'mvtojpg.jpg'))
		return HttpResponse(get_pathSuffixDict(os.path.join(path,nowfolder)))
	except:
		return HttpResponse('error')


@require_http_methods(['POST'])
@ensure_csrf_cookie
def openfolder(request):
	obj=json.loads(request.body.decode())
	folder=obj['openfolder']
	filelist=os.listdir(os.path.join('static/uploadfiles',folder))
	if len(filelist)==0:
		return HttpResponse('error')
	return HttpResponse(get_pathSuffixDict(os.path.join('static/uploadfiles',folder)))

@require_http_methods(['POST'])
@ensure_csrf_cookie
def backtoprevious(request):
	try:
		obj=json.loads(request.body.decode())
		folder=obj['backtoprevious']
		return HttpResponse(get_pathSuffixDict(os.path.join('static/uploadfiles',folder)))
	except Exception as e:
		raise e

#settings界面
#默认的config只在后端储存，需要时请求，保证前后端的分离
@require_http_methods(['POST'])
@ensure_csrf_cookie
def getDefaultConfig(request):
	global config
	try:
		obj=json.loads(request.body.decode())
		chanelsum=int(obj['chanelsum']) #仅指视频通道个数,json传过来是字符串，转化为数字
		for i in range(2,chanelsum):
			config['window_size_'+str(i)]=config['window_size_1']
			config['min_output_duration_'+str(i)]=config['min_output_duration_1']
			config['max_output_duration_'+str(i)]=config['max_output_duration_1']
		return HttpResponse(json.dumps(config))
	except Exception as e:
		return HttpResponse('error')
		raise e

@require_http_methods(['POST'])
@ensure_csrf_cookie
def settingsvalue(request):
	global task_name, config, video_list, audio_list
	try:
		obj=json.loads(request.body.decode())
		task_name=obj['task_name']
		config=obj['config']
		#开始合成
		testCelery.delay(task_name,video_list,config,audio_list)
		return HttpResponse('success')
	except Exception as e:
		raise e
		return HttpResponse('error')

#doing界面
@require_http_methods(['POST'])
@ensure_csrf_cookie
def progress(request):
	global task_name
	try:
		progress={'task_name':task_name,'progress_rate':progress_rate}
		return HttpResponse('success')
	except:
		return HttpResponse('error')

#done界面
@require_http_methods(['POST'])
@ensure_csrf_cookie
def resultfiles(request):
	try:
		return HttpResponse(get_pathSuffixDict('static/resultfiles'))
	except:
		return HttpResponse('error')

@require_http_methods(['GET'])
@csrf_exempt
def downloadbigfile(request):
	obj=request.GET.get('filename')
	def read_file(fn, buf_size=262144):
		f = open(fn,'rb')
		while True:
			c=f.read(buf_size)
			if c:
				yield c 
			else:
				break
		f.close()
	response = StreamingHttpResponse(read_file(os.path.join(os.getcwd(),'static/resultfiles',obj)))
	print(os.path.join(os.getcwd(),'static/resultfiles',obj))
	response['Content-Type']='application/octet-stream'
	response['Content-Disposition']='attachment;filename="'+obj+'"'
	return response

#其他函数
#path路径下，将文件后缀在suffix（list类型）中的文件列表列出在list_name中
def filelistindir(path,list_name,suffix):
	for file in os.listdir(path):
		file_path=os.path.join(path,file)
		if os.path.isdir(file_path):
			filelistindir(file_path,list_name,suffix)
		elif os.path.splitext(file_path)[1].lower() in suffix:
			list_name.append(file_path)

#将视频第一帧变为图片，存储在和视频同路径下，原视频名+mvtojpg.jpg为第一帧截图名，供显示用
def mvtojpg(path):
	global videosuffix
	mvtojpglist=[]
	filelistindir(os.path.join(os.getcwd(),path),mvtojpglist,videosuffix)
	for mv in mvtojpglist:
		vc=cv2.VideoCapture(mv)
		rval, frame = vc.read()
		if rval:
			cv2.imencode('.jpg',frame)[1].tofile(os.path.splitext(mv)[0]+'mvtojpg.jpg')
		vc.release()

#获取path路径下第一级目录的文件名、后缀名，格式：{相对路径+文件名：后缀，}
def get_pathSuffixDict(path):
	global audiosuffix
	try:
		filelist=os.listdir(path)
		pathsuffixdict={}
		for file in filelist:
			file_path=os.path.join(path,file)
			if (os.path.isdir(file_path)):
				audioorvideo=[]
				filelistindir(file_path,audioorvideo,audiosuffix)
				if audioorvideo==[]:
					pathsuffixdict[file_path[len('static/uploadfiles')+1:]]='dir'
				else:
					pathsuffixdict[file_path[len('static/uploadfiles')+1:]]='musicdir'
			else:
				pathsuffixdict[file_path[len('static/uploadfiles')+1:]]=os.path.splitext(file)[1]
		return json.dumps(pathsuffixdict)
	except Exception as e:
		raise e
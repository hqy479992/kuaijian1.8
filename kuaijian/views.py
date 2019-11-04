import cv2
import json
import os
import shutil
from kuaijian.util.executor import Executor

from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from patch import ExtractAudioTrack
from soundxHandler import SoundxHandler

from multiprocessing import Queue

# Create your views here.
# 文件内全局变量
audio_list = []
video_list = []
audio_in_videolist=0
config = {
    'window_size_0': 0,
    'window_size_1': 150,  # 后面也都默认150
    'min_output_duration_0': 10,
    'min_output_duration_1': 10,
    'max_output_duration_0': 15,
    'max_output_duration_1': 20,  # 后面都默认20
    'head_duration': 10,
    'tail_duration': 10
}

# 此变量与前端globalvar.js中的only_audio_suffix一致
audio_suffix = ['.wav', '.flac', '.ape', '.m4a', '.wv',
                '.mp3', '.m4b', '.m4p', '.m4r', '.m4v',
                '.aac', '.opus']

video_suffix = ['.flv', '.avi', '.wmv', 'asf', '.wmvhd',
                '.dat', '.vob', '.mpg', '.mpeg',
                '.mp4', '3gp', '.3g2', '.mkv', 'rm',
                '.rmvb', '.mov', '.qt', '.ogg',
                '.ogv', '.oga', '.mod']

executor = Executor()


# 界面
def index_pagehtml(request):
	return render(request,'index_page.html')

def index_html(request):
    return render(request, 'index.html')


def guide_html(request):
    return render(request, 'guide.html')


def question_html(request):
    return render(request, 'question.html')


def todo_html(request):
    return render(request, 'todo.html')


def doing_html(request):
    return render(request, 'doing.html')


def done_html(request):
    mvtojpg('static/resultfiles')
    return render(request, 'done.html')


def aboutus_html(request):
    return render(request, 'aboutus.html')


def contactus_html(request):
    return render(request, 'contactus.html')


def settings_html(request):
    return render(request, 'settings.html')


def navbar_html(request):
    return render(request, 'navbar.html')


def header_html(request):
    return render(request, 'header.html')


# 数据传递
# index界面
@require_http_methods(['POST'])
@ensure_csrf_cookie
def uploadfile(request):
    try:
        obj = request.FILES
        filelist = obj.getlist('file')
        pathlist = request.POST.getlist('path')
        if not filelist:
            return HttpResponse('error')
        else:
            for file in filelist:
                position = os.path.join(os.path.join(os.getcwd(), 'static/uploadfiles'),
                                        '/'.join(pathlist[filelist.index(file)].split('/')[:-1]))
                if not os.path.exists(position):
                    os.makedirs(position)
                stroage = open(position + '/' + file.name, 'wb+')
                for chunk in file.chunks():
                    stroage.write(chunk)
                stroage.close()
        mvtojpg('static/uploadfiles')
        return HttpResponse('success')
    except:
        return HttpResponse('error')


# todo界面
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
    global audio_list,video_list,audio_in_videolist
    obj = json.loads(request.body.decode())
    audio_list.clear()
    video_list.clear()
    try:
        if os.path.splitext(obj['audioFolder'])[1] != '': #如果不是文件夹，而是单独的一个音频文件
            audio_list.append(obj['audioFolder'])
            obj['videoAudiolist'].remove(obj['audioFolder'])
        else:
            # 如果有单独的音频文件夹
            if obj['audioByVideo'] == False: #如果是有单独的音频文件夹，而不是视频作音频
                # 音频列表
                filelistindir(os.path.join('static/uploadfiles', obj['audioFolder']), audio_list, audio_suffix)
                obj['videoAudiolist'].remove(obj['audioFolder'])
            else:
                # 音频列表
                #filelistindir(os.path.join('static/uploadfiles', obj['audioFolder']), audio_list, video_suffix)
                #audio_list.sort()
                audio_in_videolist=obj['videoAudiolist'].index(obj['audioFolder']) #此时audio_list是空的
        # 视频列表
        for i in range(0, len(obj['videoAudiolist'])):
            tem_video_list = []
            filelistindir(os.path.join('static/uploadfiles', obj['videoAudiolist'][i]), tem_video_list, video_suffix)
            tem_video_list.sort()
            video_list.append(tem_video_list)
        return HttpResponse('success')
    except Exception as e:
        return HttpResponse('error')
        raise e


@require_http_methods(['POST'])
@ensure_csrf_cookie
def deletefile(request):
    global video_suffix
    try:
        obj = json.loads(request.body.decode())
        deletefilename = obj['deletefilename']
        nowfolder = obj['nowfolder']
        path = 'static/uploadfiles'  # 即static
        if os.path.isdir(os.path.join(path, deletefilename)):
            shutil.rmtree(os.path.join(os.getcwd(), path, deletefilename))
        elif os.path.splitext(deletefilename)[1] in video_suffix:
            os.remove(os.path.join(path, deletefilename))
            os.remove(os.path.join(path, os.path.splitext(deletefilename)[0] + 'mvtojpg.jpg'))
        else:
            os.remove(os.path.join(path, deletefilename))
        return HttpResponse(get_pathSuffixDict(os.path.join(path, nowfolder)))
    except:
        return HttpResponse('error')


@require_http_methods(['POST'])
@ensure_csrf_cookie
def renamefile(request):
    global video_suffix
    try:
        obj = json.loads(request.body.decode())
        originname = obj['originname']
        nowfolder = obj['nowfolder']
        newname = obj['newname']
        path = 'static/uploadfiles'
        # 如果是视频的话，需要第一帧图片和视频两个都重命名
        os.rename(os.path.join(path, originname),
                  os.path.join(path, nowfolder, newname + os.path.splitext(originname)[1]))
        if os.path.splitext(originname)[1] in video_suffix:
            os.rename(os.path.join(path, os.path.splitext(originname)[0] + 'mvtojpg.jpg'),
                      os.path.join(path, nowfolder, newname + 'mvtojpg.jpg'))
        return HttpResponse(get_pathSuffixDict(os.path.join(path, nowfolder)))
    except:
        return HttpResponse('error')


@require_http_methods(['POST'])
@ensure_csrf_cookie
def openfolder(request):
    obj = json.loads(request.body.decode())
    folder = obj['openfolder']
    filelist = os.listdir(os.path.join('static/uploadfiles', folder))
    if len(filelist) == 0:
        return HttpResponse('error')
    return HttpResponse(get_pathSuffixDict(os.path.join('static/uploadfiles', folder)))


@require_http_methods(['POST'])
@ensure_csrf_cookie
def backtoprevious(request):
    try:
        obj = json.loads(request.body.decode())
        folder = obj['backtoprevious']
        return HttpResponse(get_pathSuffixDict(os.path.join('static/uploadfiles', folder)))
    except Exception as e:
        raise e


# settings界面
# 默认的config只在后端储存，需要时请求，保证前后端的分离
@require_http_methods(['POST'])
@ensure_csrf_cookie
def getDefaultConfig(request):
    global config,video_list
    try:
        obj = json.loads(request.body.decode())
        chanelsum = int(obj['chanelsum'])  # 仅指视频通道个数,json传过来是字符串，转化为数字
        for i in range(2, chanelsum):
            config['window_size_' + str(i)] = config['window_size_1']
            config['min_output_duration_' + str(i)] = config['min_output_duration_1']
            config['max_output_duration_' + str(i)] = config['max_output_duration_1']
        return HttpResponse(json.dumps({'config':config,'video_list':video_list}))
    except Exception as e:
        return HttpResponse('error')


@require_http_methods(['POST'])
@ensure_csrf_cookie
def settingsvalue(request):
    try:
        obj = json.loads(request.body.decode())
        task_name = obj['task_name']
        conf = obj['config']
        queue = Queue()
        audio_path = ExtractAudioTrack(task_name, video_list, audio_in_videolist) if len(audio_list) == 0 else audio_list[0]
        executor.submit(task_name, queue, exe_clip, task_name, queue, conf, video_list.copy(), audio_path)
        return HttpResponse(json.dumps(task_name))
    except:
        return HttpResponse('error')


def exe_clip(task_name, process_bar, conf, video_ls, audio_path):
    import discriminator
    from discriminator import FuzzyDetection, ShakeDetection
    from clip_utils import ClipControler
    import tensorflow as tf

    config = tf.compat.v1.ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = 0.4
    session = tf.Session(config=config)
    try:
        # 开始合成
        syn_handler = SoundxHandler()
        dis = discriminator.YOLOv3_discriminator()
        cc = ClipControler(task_name, process_bar, video_ls, audio_path, "./static/resultfiles/" + task_name + ".mp4", syn_handler,
                           dis, FuzzyDetection(), ShakeDetection(), conf)
        cc.run()
        del cc
    except Exception as e:
        raise e



# doing界面
@require_http_methods(['POST'])
@ensure_csrf_cookie
def progress(request):
    tasks = executor.get_all_tasks()
    rates = [{'task_name': task, 'progress_rate': executor.get_process(task)} for task in tasks]
    return HttpResponse(json.dumps(rates))

@require_http_methods(['POST'])
@ensure_csrf_cookie
def get_all_task(request):
    try:
        tasks = executor.get_all_tasks()
        print(tasks)
        return HttpResponse(json.dumps(tasks))
    except Exception as e:
        raise e
        return HttpResponse('error')

# done界面
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
    obj = request.GET.get('filename')

    def read_file(fn, buf_size=262144):
        f = open(fn, 'rb')
        while True:
            c = f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()

    response = StreamingHttpResponse(read_file(os.path.join(os.getcwd(), 'static/resultfiles', obj)))
    print(os.path.join(os.getcwd(), 'static/resultfiles', obj))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="' + obj + '"'
    return response


@require_http_methods(['POST'])
@ensure_csrf_cookie
def stop_task(request):
    try:
        js_obj = json.loads(request.body.decode())
        task_name = js_obj['task_name']
        executor.stop(task_name)
        return HttpResponse(json.loads({'result': 'stopped'}))
    except:
        return HttpResponse('error')


# 其他函数
# path路径下，将文件后缀在suffix（list类型）中的文件列表列出在list_name中
def filelistindir(path, list_name, suffix):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            filelistindir(file_path, list_name, suffix)
        elif os.path.splitext(file_path)[1].lower() in suffix:
            list_name.append(file_path)


# 将视频第一帧变为图片，存储在和视频同路径下，原视频名+mvtojpg.jpg为第一帧截图名，供显示用
def mvtojpg(path):
    global video_suffix
    mvtojpglist = []
    filelistindir(os.path.join(os.getcwd(), path), mvtojpglist, video_suffix)
    for mv in mvtojpglist:
        vc = cv2.VideoCapture(mv)
        rval, frame = vc.read()
        if rval:
            cv2.imencode('.jpg', frame)[1].tofile(os.path.splitext(mv)[0] + 'mvtojpg.jpg')
        vc.release()


# 获取path路径下第一级目录的文件名、后缀名，格式：{相对路径+文件名：后缀，}
def get_pathSuffixDict(path):
    global audio_suffix
    try:
        filelist = os.listdir(path)
        pathsuffixdict = {}
        for file in filelist:
            file_path = os.path.join(path, file)
            if (os.path.isdir(file_path)):
                audioorvideo = []
                filelistindir(file_path, audioorvideo, audio_suffix)
                if audioorvideo == []:
                    pathsuffixdict[file_path[len('static/uploadfiles') + 1:]] = 'dir'
                else:
                    pathsuffixdict[file_path[len('static/uploadfiles') + 1:]] = 'musicdir'
            else:
                pathsuffixdict[file_path[len('static/uploadfiles') + 1:]] = os.path.splitext(file)[1]
        return json.dumps(pathsuffixdict)
    except Exception as e:
        raise e

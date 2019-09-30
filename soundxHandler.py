import os
import subprocess
from glob import glob
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from soundx import Soundx

import argparse

class SoundxHandler:
    def __init__(self):
        pass

    def fun(self, ref_audio, video_dir, result_file_path):

        self.check_file(ref_audio, video_dir, result_file_path)
        clip_list = glob(video_dir + '*.MP4')
        # 提取音轨
        command = "ffmpeg -i {} -f wav -ar 44100 {}".format(ref_audio, "ref.wav")
        os.system(command)

        # results = []
        # results.append((ref_clip, 0))  # 参考音轨的偏移为0
        for clip in clip_list:
            clip_file = os.path.splitext(clip)[0] + ".wav" 
            print('从视频提取语音数据中.......')
            if os.path.exists(clip_file):
                os.remove(clip_file)
            command = "ffmpeg -i {0} -f wav -ar 44100 {1}".format(clip, clip_file)
            os.system(command)
            print('执行语音匹配算法中......')
            command = "praat audioMatch.praat {0} ref.wav {1}".format(clip_file, result_file_path)
            os.system(command)
            os.remove(clip_file)  # 临时语音文件删除

        return "success!"

    def check_file(self, ref_audio, video_dir, result_file_path):
        if os.path.exists("ref.wav"):
            os.remove("ref.wav")
        if os.path.exists(result_file_path):
            os.remove(result_file_path)
        if not os.path.exists(ref_audio):
            raise RuntimeError('指定文件' + ref_audio + "不存在")
        if not os.path.exists(video_dir):
            raise RuntimeError('指定文件夹' + video_dir + "不存在")

    def check_file(self, ref_audio, video_file, result_file_path):
        if os.path.exists("ref.wav"):
            os.remove("ref.wav")
        if os.path.exists(result_file_path):
            os.remove(result_file_path)
        if not os.path.exists(ref_audio):
            raise RuntimeError('指定文件' + ref_audio + "不存在")
        if not os.path.exists(video_file):
            raise RuntimeError('指定文件夹' + video_file + "不存在")

    def fun2(self, ref_audio, video_file, result_file_path):

        self.check_file(ref_audio, video_file, result_file_path)
        clip_list = glob(video_file)
        # 提取音轨
        command = "ffmpeg -i {} -f wav -ar 44100 {}".format(ref_audio, "ref.wav")
        os.system(command)

        # results = []
        # results.append((ref_clip, 0))  # 参考音轨的偏移为0
        for clip in clip_list:
            clip_file = os.path.splitext(clip)[0] + ".wav" 
            print('从视频提取语音数据中.......')
            if os.path.exists(clip_file):
                os.remove(clip_file)
            command = "ffmpeg -i {0} -f wav -ar 44100 {1}".format(clip, clip_file)
            os.system(command)
            print('执行语音匹配算法中......')
            command = "praat audioMatch.praat {0} ref.wav {1}".format(clip_file, result_file_path)
            os.system(command)
            os.remove(clip_file)  # 临时语音文件删除

        return "success!"

if __name__ == '__main__':

	# 加入parser
	parser = argparse.ArgumentParser(description='input reference file')
	parser.add_argument('--ref_audio', default=os.path.expanduser('/var/data/main.mp3'),
                    help='The file name for reference audio')
	parser.add_argument('--video_file', default=os.path.expanduser('/var/data/v1.mp4'),
                    help='The file name of video for process')
	parser.add_argument('--result_file_path', default=os.path.expanduser('/var/data/result.txt'),
                    help='The results of offsets')
	args = parser.parse_args()

	ref_audio = args.ref_audio
	video_file = args.video_file
	result_file_path = args.result_file_path

	# ref_clip_index = 0  # 作为参考的内容片段
	# ref_clip = clip_list[ref_clip_index]
	# clip_list.pop(ref_clip_index)  # 将参考片段从list


	print("\n")
	print("-------------------算法服务已启动-----------------")
	print("\n")
	print("\n")
	# handler processer 类
	handler = SoundxHandler()
	handler.fun2(ref_audio, video_file, result_file_path)

	#processor = Soundx.Processor(handler)

	#transport = TSocket.TServerSocket("0.0.0.0", 8990)
	# 传输方式，使用buffer
	#tfactory = TTransport.TBufferedTransportFactory()
	# 传输数据类型：二进制
	#pfactory = TBinaryProtocol.TBinaryProtocolFactory()
	# 创建一个thrift服务
	#server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

	#server.serve()
	print("-------------------算法服务结束服务------------------------------")

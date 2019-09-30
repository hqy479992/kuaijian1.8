from pydub import AudioSegment
import cv2

def ExtractAudioTrack(task_name, audio_list):
# 函数作用：提取指定通道的音轨
    new_voice = None  # 新的音轨
    for i in range(0, len(audio_list)):  # 遍历指定通道的所有视频
        temp_voice = AudioSegment.from_file(audio_list[i])  # 获取视频的音轨
        if i == 0:  # 第一段音轨
            new_voice = temp_voice
        else:  # 之后的音轨
            new_voice = new_voice + temp_voice
    new_voice.export('./static/uploadfiles/' + task_name + '.mp3' , format = "mp3")  # 保存提取后的音轨-音轨地址
    return './static/uploadfiles/' + task_name + '.mp3'  # 返回音轨地址-音轨地址

# def ExtractVideoMaterial(a):
# # 函数作用：提取指定通道的视频素材
#     temp_video_cap = cv2.VideoCapture(a)
#     temp = temp_video_cap[:1000]

# if __name__ == "__main__":
#     video_list = [["/media/wsn/N/sample_video/whole_short/test_whole_1.MP4",
#                 "/media/wsn/N/sample_video/whole_short/test_whole_2.MP4"],
#                 ["/media/wsn/N/sample_video/main_short/test_main_1.MP4",
#                 "/media/wsn/N/sample_video/main_short/test_main_2.MP4",
#                 "/media/wsn/N/sample_video/main_short/test_main_3.MP4"]]
#     # print(ExtractAudioTrack(video_list, 1))
#     ExtractVideoMaterial("/media/wsn/N/sample_video/whole_short/test_whole_1.MP4")
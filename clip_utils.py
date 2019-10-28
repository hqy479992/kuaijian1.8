import cv2
import video_utils
import discriminator
import os
import random
from pydub import AudioSegment
from soundxHandler import SoundxHandler



class ClipControler():

    """
    The controler of whole clip procedure.
    
    Totally 6 stage:
    1. Synchronization of videos and audio, clip a temp audio.
    2. Output overall view video with designated duraion.
    3. Compose videos
    4. Output remainder of overall view video.
    5. Compose temp output video and audio.mp3
    6. Release video track and remove temp files.
    """

    _video_path_list = None
    _audio_path = None
    _config = None
    _video_track_list = []
    _discriminator = None
    _output_file_path = None
    _temp_video_writer = None
    _temp_video_path = None
    _fps = None
    _resolution = None
    _temp_audio_path = None
    _syn_handler = None

    def __init__(self, task_name, queue, video_path_list, audio_path, output_file_path, syn_handler, discriminator, config):

        """
        Input:
        video_path_list: 2D list, channel is the first dimention, which contains video path seperated of this channel.
                         Note that, the overall view video should be in first place.
        audio_path: str, the path of main audio.
        config: dict, for further configuration.
        """

        self._task_name = task_name
        self._video_track_list = []
        self._video_path_list = video_path_list
        self._audio_path = audio_path
        self._config = config
        self._discriminator = discriminator
        self._temp_video_writer = None
        self._output_file_path = output_file_path
        self._fps = None
        self._resolution = None
        self._overall_view_remainder_length = None
        self._syn_handler = syn_handler
        self._queue = queue
        self._total = 0.0

        # initialize video track
        for i in range(len(video_path_list)):

            # build video queue for each channel
            temp_video_queue = video_utils.VideoQueue(video_path_list[i])

            # judge availability of each channel
            if self._fps is None or self._resolution is None:
                self._fps = int(temp_video_queue.get_fps())
                self._resolution = temp_video_queue.get_resolution()
            else:
                if self._fps != int(temp_video_queue.get_fps()):
                    raise Exception("Different FPS!")
                if self._resolution != temp_video_queue.get_resolution():
                    raise Exception("Different resolution!")

            # build video track for each channel
            temp_video_track = video_utils.VideoTrack(temp_video_queue, discriminator, self._config["window_size_" + str(i)])
            self._video_track_list.append(temp_video_track)

            print("Finish video track initialization #", str(i))

        # display stage
        print("\n-----------------------  Video Information  -----------------------------")
        print("FPS", self._fps)
        print("Resolution", self._resolution)
        print("-------------------------------------------------------------------------\n")

        # initialize video writer
        self._temp_video_path = os.path.splitext(self._output_file_path)[0] + "_temp.mp4"
        self._temp_video_writer = cv2.VideoWriter(self._temp_video_path,
                                                cv2.VideoWriter_fourcc("X","V","I","D"),
                                                int(self._fps),
                                                self._resolution)

    def run(self):
        print(self.stage1_synchonization())
        print(self.stage2_overall_view_designated_duration())
        print(self.stage3_compose_videos_method_1())
        print(self.stage4_output_overall_view_remainder())
        print(self.stage5_compose_temp_video_and_audio())

    def _read_next_frame(self):
        """
        All video tracks need to synchronously read next frame.

        Return:
        frames: list, next frame for each channel.
        """

        temp_frame_list = [None] * len(self._video_track_list)
        for i in range(len(self._video_track_list)):
            print('当前通道：',i)
            temp_frame_list[i] = self._video_track_list[i].next_frame()
        return temp_frame_list

    def _compose_video_audio(self, video_path, audio_path):

        """
        Compose video and audio.

        Return:
        0: success.
        1: failure.
        """

        try:
            cmd = "ffmpeg -y -i " + audio_path + " -i " + video_path + " -vcodec h264 " + self._output_file_path
            os.system(cmd)
        except Exception as e:
            return 1
        return 0

    def _syn_helper(self, audio_path, video_path):

        """
        Hepler function of synchronization. Input path of audio and video, and return the bias time in float.

        Return:
        bias_time: float, bias time from audio to video.
        If bias_time < 0, it means the video is faster than the audio.
        If bias_time > 0, it means the audio is faster than the video.
        """

        # calculate the bias time
        self._syn_handler.fun2(audio_path, video_path, "./temp/" + str(self._task_name) + ".txt")

        # read the bias time
        temp_txt_file = open("./temp/" + str(self._task_name) + ".txt")
        temp_str = temp_txt_file.readline()
        bias_time = float(temp_str.split("_")[-1])
        temp_txt_file.close()

        # remove temp txt file
        os.remove("./temp/" + str(self._task_name) + ".txt")

        return bias_time

    def stage1_synchonization(self):

        """
        Synchonization of videos and audio. After this function, the videos should start at the same time point.

        Return:
        0: success.
        """

        # display stage
        print("\n-----------------------------  Stage 1  ---------------------------------")
        print("-------------------------------------------------------------------------\n")

        # if there was no audio path, we believe the videos are already synchonized.
        if self._audio_path == None:
            return 0

        # calculate bias for each video
        self._video_audio_bias = [None] * len(self._video_path_list)
        for i in range(len(self._video_path_list)):

            # calculate bias time
            self._video_audio_bias[i] = self._syn_helper(self._audio_path, self._video_path_list[i][0])
            print("Calculated bias #" + str(i))

        # read audio
        temp_audio = AudioSegment.from_mp3(self._audio_path)

        ########### to synchronize all videos base on the highest bias time ##########

        # obtain the maximum of bias as baseline
        max_bias = max(self._video_audio_bias)

        # max bias > 0 means there is a video lower than the audio
        if max_bias > 0:

            # synchronize all videos
            for i in range(len(self._video_track_list)):

                # calculate bias frame count
                temp_bias_frame_count = int(abs(max_bias - self._video_audio_bias[i]) * self._fps)

                # read the redundant frames
                print("Synchronize #" + str(i), self._video_audio_bias[i])
                for j in range(temp_bias_frame_count):
                    _ = self._video_track_list[i].next_frame()
                    print(j)

                print("Remainder length #" + str(i), self._video_track_list[i].get_remainder_length())

            # synchronize audio
            temp_audio = temp_audio[int(max_bias * 1000):]
            temp_audio_length = int(len(temp_audio) // 1000)

        # max bias < 0 means all videos are faster than the audio
        else:

            # synchronize all videos
            for i in range(len(self._video_track_list)):

                # calculate bias frame count
                temp_bias_frame_count = int(abs(self._video_audio_bias[i]) * self._fps)

                # read the redundant frames
                print("Synchronize #" + str(i))
                for j in range(temp_bias_frame_count):
                    _ = self._video_track_list[i].next_frame()
                    print(j)
            temp_audio_length = int(len(temp_audio) // 1000)


        ########### to synchronize audio and set overall remiander length ##########

        # obtain overall view video remainder length
        if self._video_track_list[0].get_remainder_length() // self._fps < temp_audio_length:
            print('\n\n\n',temp_audio_length,'!!!!!!!\n\n\n!!!!!!!!!!!!!!!!!!')
            # length of audio > length of video
            self._total = self._video_track_list[0].get_remainder_length()
            self._overall_view_remainder_length = self._video_track_list[0].get_remainder_length()
            self._write_rate()
            temp_audio = temp_audio[:int(self._overall_view_remainder_length * 1000 // self._fps)]

        else:
            # length of audio < length of video
            print('\n\n\n',temp_audio_length,'!!!!!!!!!!!!!!!!!!!!!!!!!')
            self._overall_view_remainder_length = temp_audio_length * self._fps
            self._write_rate()

        # output temp audio
        print(len(temp_audio)/1000)
        self._temp_audio_path = "./temp/" + str(self._task_name) + ".mp3"
        temp_audio.export(self._temp_audio_path, "mp3")

        print("Finish audio synchronization.")

        return 0

    def stage2_overall_view_designated_duration(self):

        """
        Output overall view shot with designated duration.

        Return:
        0: success.
        1: overall view video is too short.
        """

        # display stage
        print("\n-----------------------------  Stage 2  ---------------------------------")
        print("-------------------------------------------------------------------------\n")

        # head_duraion: int, length of head overall view video.
        head_duration = self._config["head_duration"]

        for i in range(head_duration * self._fps):

            # read next frames of all video track
            temp_frames = self._read_next_frame()
            self._overall_view_remainder_length -= 1
            self._write_rate()

            # overall view video is used up
            if temp_frames[0] is None:
                return 1
            else:
                # output frame of overall view
                self._temp_video_writer.write(temp_frames[0])

        print("Finish head video output.")

        return 0

    def stage3_compose_videos_method_1(self):

        """
        Compose videos.

        Input:

        Return:
        0: success.
        1: overall view video is too short.
        """

        # display stage
        print("\n-----------------------------  Stage 3  ---------------------------------")
        print("-------------------------------------------------------------------------\n")

        # tail_duraion: int, length of tail overall view video.
        tail_duration = self._config["tail_duration"]

        # obtain minimum and maximum of each video track
        min_output_duration = []
        max_output_duration = []
        for i in range(len(self._video_track_list)):
            min_output_duration.append(self._config["min_output_duration_" + str(i)])
            max_output_duration.append(self._config["max_output_duration_" + str(i)])


        ########## main loop to compose each video track ##########

        # last and current track is overall view track
        last_track_number = 0
        current_track_number = 0

        # initialize output duration
        temp_output_duration = 0

        # initialize point of output duration
        temp_output_point = 0

        while self._overall_view_remainder_length > tail_duration * self._fps:

            # If output point = 0, it means last output duration is used up.
            # 1. We need to first select all tracks which has state of True.
            # 2. Randomly shuffle track numbers from step 1 and select one that is different from last track number.
            # 3. Check the number of frames is enough for output, or select next track of shuffled numbers.
            # 4. If there is no track that satisfy the requirements, we select the safe track (#0 overall view video).

            if temp_output_point <= 0:

                # transfer track number and set the current track number as None
                last_track_number = current_track_number
                current_track_number = None

                # select satisfying numbers
                satisfying_number_list = []
                for number in range(len(self._video_track_list)):
                    print(self._video_track_list[number].get_current_state())
                    if self._video_track_list[number].get_current_state() == True and number != last_track_number:
                        satisfying_number_list.append(number)

                # shuffle satisfying numbers
                random.shuffle(satisfying_number_list)
                print(satisfying_number_list)

                # check whether the video track has enough frames
                for number in satisfying_number_list:

                    # generate the random duration for this video track
                    temp_output_duration = random.randint(min_output_duration[number], max_output_duration[number]) * self._fps

                    # check length is enough for output AND would not influence tail output
                    if temp_output_duration <= self._video_track_list[number].get_remainder_length() and \
                        temp_output_duration <= self._overall_view_remainder_length - tail_duration * self._fps:

                        # select this number as current output track
                        current_track_number = number
                        break

                # if there is no satisfying video track, we select the overall view video
                if current_track_number is None:
                    temp_output_duration = random.randint(min_output_duration[0], max_output_duration[0]) * self._fps
                    current_track_number = 0

            # output track
            temp_output_point = temp_output_duration
            while temp_output_point > 0:

                # read next frames of all video track
                temp_frames = self._read_next_frame()
                self._overall_view_remainder_length -= 1
                self._write_rate()
                temp_output_point -= 1
                print(temp_output_point, temp_output_duration)
                print(current_track_number)

                # overall view video is used up
                if temp_frames[current_track_number] is None:
                    return 1
                else:
                    # output frame of overall view
                    self._temp_video_writer.write(temp_frames[current_track_number])

                if current_track_number != 0 and self._video_track_list[current_track_number].get_first_state_list() == False:
                # 如果下一帧为 False 状态，切换镜头
                    temp_output_point = 0
                    break
        return 0


    def stage4_output_overall_view_remainder(self):

        """
        Output remainder frames of overall view.

        0: success.
        1: overall view video is used up.
        """

        # display stage
        print("\n-----------------------------  Stage 4  ---------------------------------")
        print("-------------------------------------------------------------------------\n")

        # overall view is used up
        if self._overall_view_remainder_length <= 0:
            return 1

        while self._overall_view_remainder_length > 0:
            self._overall_view_remainder_length -= 1
            self._write_rate()
            self._temp_video_writer.write(self._video_track_list[0].next_frame())

        return 0

    def stage5_compose_temp_video_and_audio(self):

        """
        Compose temp video and audio.

        0: success.
        1: failure.
        2: no audio.
        """

        # display stage
        print("\n-----------------------------  Stage 5  ---------------------------------")
        print("-------------------------------------------------------------------------\n")

        # release video writer
        self._temp_video_writer.release()

        # no audio
        if self._audio_path == None:
            return 2

        # no temp audio
        if self._temp_video_path == None:
            return self._compose_video_audio(self._temp_video_path, self._audio_path)
        else:
            return self._compose_video_audio(self._temp_video_path, self._temp_audio_path)

    def __del__(self):

        """
        After finishing clip, we need release all video tracks and remove all temp files.

        0: success.
        1: failure.
        """

        if self._video_track_list is not None:
            for temp_video_track in self._video_track_list:
                del temp_video_track

        # remove temp files
        if self._temp_video_path is not None:
            try:
                os.remove(self._temp_video_path)
            except Exception as e:
                return 1

        if self._temp_audio_path is not None:
            try:
                os.remove(self._temp_audio_path)
            except Exception as e:
                return 1

    def _compute_progress(self, remainder, total):
        return round(1 - (remainder / total), 2)

    def _write_rate(self):
        remainder = self._overall_view_remainder_length
        total = self._total
        try:
            self._queue.put_nowait(self._compute_progress(remainder, total))
        except:
            pass


if __name__ == "__main__":
    # video_path = [["/media/wsn/N/sample_video/whole_short/test_whole_1.MP4",
    #             "/media/wsn/N/sample_video/whole_short/test_whole_2.MP4"],
    #             ["/media/wsn/N/sample_video/main_short/test_main_1.MP4",
    #             "/media/wsn/N/sample_video/main_short/test_main_2.MP4",
    #             "/media/wsn/N/sample_video/main_short/test_main_3.MP4"]]
    # audio_path = "/media/wsn/N/sample_video/voice_short/main.wav"
    # config = {
    #     "window_size_0" : 0,
    #     "window_size_1" : 125,
    #     "min_output_duration_0" : 10,
    #     "max_output_duration_0" : 15,
    #     "min_output_duration_1" : 10,
    #     "max_output_duration_1" : 20,
    #     "head_duration" : 10,
    #     "tail_duration" : 10,
    # }
    # video_path = [["/media/wsn/TOSHIBAEXT/whole/BPAV/CLPR/C27_0247_01/C27_0247_01.MP4",
    #             "/media/wsn/TOSHIBAEXT/whole/BPAV/CLPR/C27_0247_02/C27_0247_02.MP4",
    #             "/media/wsn/TOSHIBAEXT/whole/BPAV/CLPR/C27_0247_03/C27_0247_03.MP4",
    #             "/media/wsn/TOSHIBAEXT/whole/BPAV/CLPR/C27_0247_04/C27_0247_04.MP4",
    #             "/media/wsn/TOSHIBAEXT/whole/BPAV/CLPR/C27_0247_05/C27_0247_05.MP4",
    #             "/media/wsn/TOSHIBAEXT/whole/BPAV/CLPR/C27_0247_06/C27_0247_06.MP4",
    #             "/media/wsn/TOSHIBAEXT/whole/BPAV/CLPR/C27_0247_07/C27_0247_07.MP4",
    #             "/media/wsn/TOSHIBAEXT/whole/BPAV/CLPR/C27_0248_01/C27_0248_01.MP4",
    #             "/media/wsn/TOSHIBAEXT/whole/BPAV/CLPR/C27_0248_02/C27_0248_02.MP4",
    #             "/media/wsn/TOSHIBAEXT/whole/BPAV/CLPR/C27_0248_03/C27_0248_03.MP4",
    #             "/media/wsn/TOSHIBAEXT/whole/BPAV/CLPR/C27_0248_04/C27_0248_04.MP4",
    #             "/media/wsn/TOSHIBAEXT/whole/BPAV/CLPR/C27_0248_05/C27_0248_05.MP4",
    #             "/media/wsn/TOSHIBAEXT/whole/BPAV/CLPR/C27_0248_06/C27_0248_06.MP4",
    #             "/media/wsn/TOSHIBAEXT/whole/BPAV/CLPR/C27_0248_07/C27_0248_07.MP4",
    #             "/media/wsn/TOSHIBAEXT/whole/BPAV/CLPR/C27_0248_08/C27_0248_08.MP4"],
                
    #             ["/media/wsn/TOSHIBAEXT/main/BPAV/CLPR/948_0364_01/948_0364_01.MP4",
    #             "/media/wsn/TOSHIBAEXT/main/BPAV/CLPR/948_0364_02/948_0364_02.MP4",
    #             "/media/wsn/TOSHIBAEXT/main/BPAV/CLPR/948_0364_03/948_0364_03.MP4",
    #             "/media/wsn/TOSHIBAEXT/main/BPAV/CLPR/948_0364_04/948_0364_04.MP4",
    #             "/media/wsn/TOSHIBAEXT/main/BPAV/CLPR/948_0364_05/948_0364_05.MP4",
    #             "/media/wsn/TOSHIBAEXT/main/BPAV/CLPR/948_0364_06/948_0364_06.MP4",
    #             "/media/wsn/TOSHIBAEXT/main/BPAV/CLPR/948_0364_07/948_0364_07.MP4",
    #             "/media/wsn/TOSHIBAEXT/main/BPAV/CLPR/948_0365_01/948_0365_01.MP4",
    #             "/media/wsn/TOSHIBAEXT/main/BPAV/CLPR/948_0365_02/948_0365_02.MP4",
    #             "/media/wsn/TOSHIBAEXT/main/BPAV/CLPR/948_0365_03/948_0365_03.MP4",
    #             "/media/wsn/TOSHIBAEXT/main/BPAV/CLPR/948_0365_04/948_0365_04.MP4",
    #             "/media/wsn/TOSHIBAEXT/main/BPAV/CLPR/948_0366_01/948_0366_01.MP4",
    #             "/media/wsn/TOSHIBAEXT/main/BPAV/CLPR/948_0366_02/948_0366_02.MP4",
    #             "/media/wsn/TOSHIBAEXT/main/BPAV/CLPR/948_0366_03/948_0366_03.MP4",
    #             "/media/wsn/TOSHIBAEXT/main/BPAV/CLPR/948_0366_04/948_0366_04.MP4"],
               
    #             ["/media/wsn/TOSHIBAEXT/3/CLPR/764_2489_01/764_2489_01.MP4",
    #             "/media/wsn/TOSHIBAEXT/3/CLPR/764_2489_02/764_2489_02.MP4",
    #             "/media/wsn/TOSHIBAEXT/3/CLPR/764_2489_03/764_2489_03.MP4",
    #             "/media/wsn/TOSHIBAEXT/3/CLPR/764_2490_01/764_2490_01.MP4",
    #             "/media/wsn/TOSHIBAEXT/3/CLPR/764_2490_02/764_2490_02.MP4",
    #             "/media/wsn/TOSHIBAEXT/3/CLPR/764_2491_01/764_2491_01.MP4",
    #             "/media/wsn/TOSHIBAEXT/3/CLPR/764_2491_02/764_2491_02.MP4",
    #             "/media/wsn/TOSHIBAEXT/3/CLPR/764_2491_03/764_2491_03.MP4",
    #             "/media/wsn/TOSHIBAEXT/3/CLPR/764_2491_04/764_2491_04.MP4",
    #             "/media/wsn/TOSHIBAEXT/3/CLPR/764_2491_05/764_2491_05.MP4",
    #             "/media/wsn/TOSHIBAEXT/3/CLPR/764_2491_06/764_2491_06.MP4",
    #             "/media/wsn/TOSHIBAEXT/3/CLPR/764_2491_07/764_2491_07.MP4",
    #             "/media/wsn/TOSHIBAEXT/3/CLPR/764_2491_08/764_2491_08.MP4"]
    #             ]
    video_path = [['/media/wsn/N/zhenai/whole/C27_0247_01.MP4',
                   '/media/wsn/N/zhenai/whole/C27_0247_02.MP4'],
                  ['/media/wsn/N/zhenai/main/948_0364_01.MP4',
                   '/media/wsn/N/zhenai/main/948_0364_02.MP4'],
                  ['/media/wsn/N/zhenai/3/764_2489_01.MP4',
                  '/media/wsn/N/zhenai/3/764_2489_02.MP4']]
    audio_path = "/home/wsn/Desktop/MONO-000.wav"

    video_path = [['/media/wsn/TOSHIBAEXT/2019.5.30youeryuan/whole/BPAV/CLPR/639_0492_01/639_0492_01.MP4',
                   '/media/wsn/TOSHIBAEXT/2019.5.30youeryuan/whole/BPAV/CLPR/639_0492_02/639_0492_02.MP4',
                   '/media/wsn/TOSHIBAEXT/2019.5.30youeryuan/whole/BPAV/CLPR/639_0492_03/639_0492_03.MP4'],
                   ['/media/wsn/TOSHIBAEXT/2019.5.30youeryuan/main/BPAV/CLPR/200_1019_01/200_1019_01.MP4',
                   '/media/wsn/TOSHIBAEXT/2019.5.30youeryuan/main/BPAV/CLPR/200_1019_02/200_1019_02.MP4',
                   '/media/wsn/TOSHIBAEXT/2019.5.30youeryuan/main/BPAV/CLPR/200_1019_03/200_1019_03.MP4'],
                   ['/media/wsn/TOSHIBAEXT/2019.5.30youeryuan/3/BPAV/CLPR/655_1079_01/655_1079_01.MP4',
                   '/media/wsn/TOSHIBAEXT/2019.5.30youeryuan/3/BPAV/CLPR/655_1079_02/655_1079_02.MP4',
                   '/media/wsn/TOSHIBAEXT/2019.5.30youeryuan/3/BPAV/CLPR/655_1079_03/655_1079_03.MP4']]
    audio_path = "/media/wsn/TOSHIBAEXT/2019.5.30youeryuan/voice/STEREO/FOLDER01/MONO-000.wav"
    config = {
        "window_size_0" : 0,
        "window_size_1" : 125,
        "window_size_2" : 125,
        "min_output_duration_0" : 5,
        "max_output_duration_0" : 10,
        "min_output_duration_1" : 10,
        "max_output_duration_1" : 20,
        "min_output_duration_2" : 5,
        "max_output_duration_2" : 10,
        "head_duration" : 10,
        "tail_duration" : 10,
    }

    # video_path = [['/media/wsn/N/kuaijian1.5/static/uploadfiles/whole_short/test_whole_1.MP4',
    #                '/media/wsn/N/kuaijian1.5/static/uploadfiles/whole_short/test_whole_2.MP4'],
    #                ['/media/wsn/N/kuaijian1.5/static/uploadfiles/main_short/test_main_1.MP4',
    #                '/media/wsn/N/kuaijian1.5/static/uploadfiles/main_short/test_main_2.MP4',
    #                '/media/wsn/N/kuaijian1.5/static/uploadfiles/main_short/test_main_3.MP4']]
    # audio_path = '/media/wsn/N/kuaijian1.5/static/uploadfiles/voice_short/main.wav'

    # video_path = [['/media/wsn/TOSHIBAEXT/2019.5.17huaxiweidao/whole/BPAV/CLPR/100_0919_01/100_0919_01.MP4',
    #                '/media/wsn/TOSHIBAEXT/2019.5.17huaxiweidao/whole/BPAV/CLPR/100_0919_02/100_0919_02.MP4'],
    #                ['/media/wsn/TOSHIBAEXT/2019.5.17huaxiweidao/main/BPAV/CLPR/200_0874_01/200_0874_01.MP4',
    #                '/media/wsn/TOSHIBAEXT/2019.5.17huaxiweidao/main/BPAV/CLPR/200_0874_02/200_0874_02.MP4']]
    # audio_path = '/media/wsn/TOSHIBAEXT/2019.5.17huaxiweidao/voice/STEREO/FOLDER01/MONO-000.wav'

    # config = {
    #     "window_size_0" : 0,
    #     "window_size_1" : 125,
    #     "min_output_duration_0" : 5,
    #     "max_output_duration_0" : 10,
    #     "min_output_duration_1" : 10,
    #     "max_output_duration_1" : 20,
    #     "head_duration" : 10,
    #     "tail_duration" : 10,
    # }
    # video_path = [['/media/wsn/N/yancao/whole/whole_1_whole.MP4',
    #                '/media/wsn/N/yancao/whole/whole_2.MP4'],
    #                ['/media/wsn/N/yancao/main/main_main.MP4']]
    # audio_path = '/media/wsn/N/yancao/voice/MONO-000.wav'
    # config = {
    #     "window_size_0" : 0,
    #     "window_size_1" : 125,
    #     "min_output_duration_0" : 10,
    #     "max_output_duration_0" : 15,
    #     "min_output_duration_1" : 10,
    #     "max_output_duration_1" : 20,
    #     "head_duration" : 10,
    #     "tail_duration" : 10,
    # }

    syn_handler = SoundxHandler()
    dis = discriminator.YOLOv3_discriminator()
    cc = ClipControler("123456", video_path, audio_path, "./temp/test_output.mp4", syn_handler, dis, config)
    print(cc.stage1_synchonization())
    print(cc.stage2_overall_view_designated_duration())
    print(cc.stage3_compose_videos_method_1())
    print(cc.stage4_output_overall_view_remainder())
    print(cc.stage5_compose_temp_video_and_audio())
    del cc
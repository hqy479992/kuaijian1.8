import cv2
from discriminator import YOLOv3_discriminator

class VideoQueue():

    # video queue attributes
    _video_filenames = None
    _fps = None
    _resolution = None
    _video_length = None
    _total_length = None

    # frame reading attributes
    _current_video_number = None
    _last_frame_cache = None
    _current_video_cap = None
    _current_video_cap_point = None
    _total_video_cap_point = None
    _drop_frame_count = 0

    def __init__(self, video_filenames):
        
        """Video queue class provide status of a shot.

        Input:
        video_filenames: list, addresses of all videos of this queue.
        """

        self._video_filenames = sorted(video_filenames)
        self._current_video_number = 0
        self._current_video_cap_point = 0
        self._total_video_cap_point = 0

        # judge availability and obtain attributes
        if len(self._video_filenames) == 0:
            raise Exception("Not found video filenames!")

        # judge availability of each video, obtain information of fps, resolution, length
        for i in range(len(self._video_filenames)):
            temp_video_cap = cv2.VideoCapture(self._video_filenames[i])

            # judge video's availability
            if temp_video_cap.isOpened() == False:
                raise Exception("Reading video error!")

            # obtain and judge information
            if i == 0:
                self._fps = temp_video_cap.get(cv2.CAP_PROP_FPS)
                self._resolution = (int(temp_video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(temp_video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
                self._video_length = [int(temp_video_cap.get(cv2.CAP_PROP_FRAME_COUNT))]
            else:
                if self._fps != temp_video_cap.get(cv2.CAP_PROP_FPS):
                    raise Exception("Different FPS!")
                if self._resolution != (int(temp_video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(temp_video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))):
                    raise Exception("Different resolution!")
                self._video_length.append(int(temp_video_cap.get(cv2.CAP_PROP_FRAME_COUNT)))

            # release temp video capture
            temp_video_cap.release()

        # calculate total length
        self._total_length = sum(self._video_length)

    def next_frame(self):
        """
        Read next video frame.

        Return:
        frame: np.array, frame with opencv matrix format.
               If return value is None, it means the video is used up.
        """
        
        # first video and first frame
        if self._current_video_cap == None:
            # initiate parameters
            self._current_video_cap = cv2.VideoCapture(self._video_filenames[self._current_video_number])

            # read first frame
            success, frame = self._current_video_cap.read()
            self._current_video_cap_point += 1
            self._total_video_cap_point += 1
            
            # read failure
            if success == False:
                raise Exception("Reading video frame failure!")
            
            # read success, update the frame cache
            self._last_frame_cache = frame

            return frame

        # other frames
        else:
            # check whether it is remainder video
            if self._current_video_number >= len(self._video_filenames):
                return None
            
            # check whether it is needed to change video capture
            if self._current_video_cap_point >= self._video_length[self._current_video_number]:
                
                # update current video sequence number
                self._current_video_number += 1

                # check whether it is remainder video
                if self._current_video_number >= len(self._video_filenames):
                    return None

                # change video
                self._current_video_cap.release()
                self._current_video_cap = cv2.VideoCapture(self._video_filenames[self._current_video_number])

                # check current video capture point
                self._current_video_cap_point = 0
                
                # check availability
                if self._current_video_cap.isOpened() == False:
                    raise Exception("Reading video error!")
            
            # read next frame
            success, frame = self._current_video_cap.read()
            self._current_video_cap_point += 1
            self._total_video_cap_point += 1

            # failure of reading the first frame means the video has error  
            if success == False and self._current_video_cap_point == 1:
                raise Exception("Reading video frame failure!")

            # deal with drop frames and return the cache frame
            if success == False and self._current_video_cap_point < self._video_length[self._current_video_number]:
                # record the count of drop frames
                self._drop_frame_count += 1
                return self._last_frame_cache

            # deal with unknown error
            if success == False:
                raise Exception("Unknown reading video frame failure!")

            # update frame cache and return current frame
            self._last_frame_cache = frame
            return frame    

    def get_total_video_cap_point(self):
        """Return point of total video capture"""
        return self._total_video_cap_point

    def get_tatal_length(self):
        """Return total length of video capture"""
        return self._total_length

    def get_remainder_length(self):
        """Return remainder length of video capture"""
        return self._total_length - self._total_video_cap_point
    
    def get_fps(self):
        """Return fps of video capture"""
        return self._fps

    def get_resolution(self):
        """Return fps of video capture"""
        return self._resolution

    def __del__(self):
        """
        Release video capture and memory.
        """
        if self._current_video_cap is not None:
            self._current_video_cap.release()



class VideoTrack():

    _video_queue = None
    _window_size = 125
    _window_image_list = []
    _window_state_list = []
    _current_state = None
    _window_none_count = None

    def __init__(self, video_queue, discriminator, window_size = 125):

        """
        Video track contains a VideoQueue object, which is utilized to encapsulate a track.
        This track has its own sliding window.

        Input:
        video_queue: VideoQueue.
        discriminator: discriminator class.
        window_size: int, default as 125. (0 means no sliding window)
        """

        self._video_queue = video_queue
        self._discriminator = discriminator
        self._window_size = window_size
        self._window_none_count = 0

        # video queue is too short
        if self._video_queue.get_remainder_length() < self._window_size:
            raise Exception("Video queue is too short!")

        # this video track need not to set sliding window, and its state would be true
        if self._window_size == 0:
            self._current_state = True
        # this video track has sliding window
        else:
            # build frame window
            for i in range(self._window_size):
                temp_frame = self._video_queue.next_frame()
                self._window_image_list.append(temp_frame)

                # judge state of the frame
                temp_state = self._discriminator.discriminate(temp_frame)
                self._window_state_list.append(temp_state)

            # calculate current stself._window_image_list[i]ate
            self._current_state = True
            for temp_state in self._window_state_list:
                self._current_state = self._current_state and temp_state

    def next_frame(self):
        
        """
        Return the first frame of sliding window.
        If the return value is none, it means this video track is used up.
        """

        # if no sliding window, straightly ouput the frame of video queue
        if self._window_size == 0:
            return self._video_queue.next_frame()
        
        # sliding window size is not 0
        else:
            temp_frame = self._video_queue.next_frame()
            self._update_window_image_list(temp_frame)
            
            # frame of video queue is not used up
            if temp_frame is not None:

                # discriminate state of the frame
                temp_state = self._discriminator.discriminate(temp_frame)
                self._update_window_state_list(temp_state)

                # calculate current state
                self._current_state = True
                for temp_state in self._window_state_list:
                    self._current_state = self._current_state and temp_state

            # Null frame has no state
            else:
                self._update_window_state_list(None)
                
            return self._window_image_list[0]

    def _update_window_image_list(self, frame):
        
        """
        Update the sliding window, move all images to the forward position.

        Input:
        frame: np.array, frame with opencv matrix format.
        """

        # count the number of None
        if frame is None:
            self._window_none_count += 1

        for i in range(self._window_size - 1):
            self._window_image_list[i] = self._window_image_list[i+1]
        self._window_image_list[self._window_size - 1] = frame

    def _update_window_state_list(self, state):
        
        """
        Update the sliding window state list.

        Input:
        state: boolean, state of current image.
        """

        for i in range(self._window_size - 1):
            self._window_state_list[i] = self._window_state_list[i+1]
        self._window_state_list[self._window_size - 1] = state

    def get_remainder_length(self):
        
        """
        Return remainder length of video track.
        """

        return self._video_queue.get_remainder_length() + self._window_size - self._window_none_count

    def get_state_list(self):

        """
        Return state list.
        """

        return self._window_state_list

    def get_first_state_list(self):
    # 函数作用：返回当前开关第一帧的状态
        return self._window_state_list[0]

    def get_current_state(self):

        """
        Return current state.
        """

        return self._current_state

    def __del__(self):
        """
        Release video track and memory.
        """
        if self._video_queue is not None:
            del self._video_queue
        




if __name__ == "__main__":

    video_filenames = [
                    "/media/wsn/N/sample_video/whole_short/test_whole_1.MP4",
                    "/media/wsn/N/sample_video/whole_short/test_whole_2.MP4"]
    video_queue = VideoQueue(video_filenames)
    # dis = YOLOv3_discriminator()
    # video_track = VideoTrack(video_queue, dis, 125)
    # frame = video_track.next_frame()
    # count = 1
    # print(video_track.get_state_list())
    # print(video_track.get_current_state())
    # print(count, video_track.get_remainder_length())
    # while frame is not None:
    #     frame = video_track.next_frame()
    #     count += 1
    #     print(video_track.get_state_list())
    #     print(video_track.get_current_state())
    #     print(count, video_track.get_remainder_length())
    #     cv2.imshow("test", frame)
    #     cv2.waitKey(5)



    print(video_queue.get_remainder_length())
    frame = video_queue.next_frame()
    count = 1
    while frame is not None:
        frame = video_queue.next_frame()
        count += 1
        print(count, video_queue.get_remainder_length())
        cv2.imshow("test", frame)
        cv2.waitKey(5)

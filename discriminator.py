import cv2
from YOLOv3 import utils
from YOLOv3.model.yolo_model import YOLO


class YOLOv3_discriminator:

    yolo_model = None
    confidence = None

    def __init__(self, yolov3_model_path = 'YOLOv3/data/yolo.h5',
                classes_file = 'YOLOv3/data/coco_classes.txt',
                yolo_object_threshold = 0.6,
                yolo_nms_threshold = 0.5, 
                confidence = 0.90):

        """
        YOLOv3 discriminator utilize YOLOv3 model to detect objects.
        
        Input:
        yolov3_model_path: str, model path of yolov3 model, default as 'YOLOv3/data/yolo.h5.
        classes_file: str, path of classes file, defualt as 'YOLOv3/data/coco_classes.txt'.
        yolo_object_threshold: float, default as 0.6. 
        yolo_nms_threshold = float, default as 0.5.
        confidence = float, default as 0.90
        """

        self.yolo_model = YOLO(yolov3_model_path, yolo_object_threshold, yolo_nms_threshold)
        self.confidence = confidence
        self.all_classes = utils.get_classes(classes_file)

    def discriminate(self, image):
    # 函数作用：判断当前帧是否可用
        if self.people_detection(image):
        # 如果当前帧 检测到人 and 不模糊 and 不抖动
            return True
        else:
            return False

    def people_detection(self, image):

        """
        Discriminate whether the input image has people with confidence higher than config.
        
        Input:
        image: np.array, frame with opencv matrix format. 

        Return:
        tag: boolean, whether the input image has people with confidence higher than config.
        """

        boxes_temp, classes_temp, scores_temp = utils.detect_image_4_results(image, self.yolo_model, self.all_classes)
        if classes_temp is not None and classes_temp[0] == 0 and scores_temp[0] >= self.confidence:
            return True
        else:
            return False
    
class FuzzyDetection():
    
    def __init__(self, fuzzy_score = 50):
        self.fuzzy_score = fuzzy_score
        
    def fuzzy_detection(self, image):
    # 函数作用：获取图片的 score 以判断是否为虚焦或模糊
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 将图片压缩为单通道的灰度图
        score = cv2.Laplacian(image_gray, cv2.CV_64F).var()  # 返回图片的 score
        if score > self.fuzzy_score:  # 如果 score 大于预定 score
            print('score:' + str(score))
            return True
        else:
            return False
        
class ShakeDetection():
    
    def __init__(self, min_feature_points = 70):
        self.min_feature_points = min_feature_points
        
    def shake_detection(self, previous_image, image):
    # 函数作用：检测镜头是否发生抖动
        img1 = cv2.cvtColor(previous_image, cv2.COLOR_BGR2GRAY)  # 把前一帧转换成灰度图像
        img2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 把当前帧转换成灰度图像

        orb = cv2.ORB_create()
        keypoints1, des1 = orb.detectAndCompute(img1, None)  # 获取上一帧的特征
        keypoints2, des2 = orb.detectAndCompute(img2, None)  # 获取当前帧的特征

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
        if not (des1 is None) and not (des2 is None):
        # 如果连续两帧都能提取到特征点
            matches = bf.match(des1, des2)  # 特征点匹配
            matches = sorted(matches, key = lambda x: x.distance)  # 匹配的特征点排序
            if len(matches) > self.min_feature_points:
            # 如果连续两帧的特征匹配点超过指定最小的特征点数，则视为无抖动
                print('matches:' + str(len(matches)))
                return True
            else:
            # 如果连续两帧的特征匹配点未超过指定最小的特征点数，则视为抖动或者当前图片不好
                return False
        else:
        # 如果从帧中提取不到特征值（当前图片不好）
            return False
        
if __name__ == "__main__":
    yolo = YOLOv3_discriminator('YOLOv3/data/yolo.h5', 'YOLOv3/data/coco_classes.txt')
    print(yolo.discriminate(cv2.imread("/home/wsn/Pictures/The_Gongga_Mountain_by_wangjinyu.jpg")))
import cv2
from YOLOv3 import utils
from YOLOv3.model.yolo_model import YOLO

class YOLOv3_discriminator():

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
        

if __name__ == "__main__":
    yolo = YOLOv3_discriminator('YOLOv3/data/yolo.h5', 'YOLOv3/data/coco_classes.txt')
    print(yolo.discriminate(cv2.imread("/home/wsn/Pictures/The_Gongga_Mountain_by_wangjinyu.jpg")))
    
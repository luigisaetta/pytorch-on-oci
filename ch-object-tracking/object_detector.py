#
# to incapsulate the Object Detector based on YOLO v8
# prepare detections as expected from DeepSort (see: https://github.com/levan92/deep_sort_realtime)
#
from ultralytics import YOLO


class ObjectDetector:
    def __init__(self, model_path):
        self.model_path = model_path

        print("Loading YOLO v8 model..")
        self.model = YOLO(model_path)

        # TODO check...
        self.model.overrides["iou"] = 0.45  # NMS IoU threshold

        print("Loaded YOLO v8 model..")
        print()

    def detect(self, frame, verbose=False):
        """
        get a frame from the video and returns a list of detections
        in the format expected from deep_sort
        [l, t, w, h], conf, v_cls
        """

        # apply yolo
        results = self.model.predict(frame, verbose=verbose)

        # these are passed to deepsort
        detections = []

        for result in results:
            # move to cpu
            result = result.cpu()

            # cast to int
            boxes = result.boxes.xyxy.numpy().astype(int)
            boxes_wh = result.boxes.xywh.numpy().astype(int)
            list_conf = result.boxes.conf.numpy()
            list_cls = result.boxes.cls.numpy().astype(int)

            for box, box_wh, conf, v_cls in zip(boxes, boxes_wh, list_conf, list_cls):
                # prepare format expected by Deepsort
                l, t = box[0], box[1]
                w, h = box_wh[2], box_wh[3]

                detections.append(([l, t, w, h], conf, v_cls))

        return detections

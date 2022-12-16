import cv2
import yaml
import torch
import numpy as np

from sort import *
from video_loader import VideoReader

class Detection:
    def __init__(self) -> None:
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

    def predict(self, img):
        pred = self.model(img)
        pred = pred.xyxy[0]
        pred = pred.numpy()
        return pred

if  __name__ == '__main__':
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    print(f"Config:\n{yaml.dump(config)}")

    vid_path = config['video_path']
    video_reader = VideoReader(vid_path)
    frame = next(video_reader)
    show = config['show']
    draw = config['draw']
    write = config['write']

    detector = Detection()
    mot_tracker = Sort(max_age=config['tracker_max_age'], min_hits=config['tracker_min_hits'])
    count = 0
    if write:
        video_writer = cv2.VideoWriter('out.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (1280,720))

    while frame is not False:
        pred = detector.predict(frame)
        # Get only car tracking
        pred = pred[np.where(pred[:,-1] == 2)]
        pred = pred[:, :5]     # Get only [x1, y1, x2, y2, score]

        # update SORT
        # track_bbs_ids is a np array where each row contains a valid bounding box and track_id (last column)
        track_bbs_ids = mot_tracker.update(pred)
        if draw:
            for box in track_bbs_ids:
                x1_y1 = box[:2].astype('int')
                x2_y2 = box[2:4].astype('int')
                track_id = box[4].astype('int')

                cv2.rectangle(frame, x1_y1, x2_y2, (0,0,200), 2)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, str(track_id), x1_y1, fontFace=font, fontScale=1, color=(0,0,200), thickness=2)

        if write:
            # cv2.imwrite(f'tmp/img-{count}.jpg', frame)
            video_writer.write(frame)

        if show:
            cv2.imshow('Tracker', frame)
            if cv2.waitKey(0) in [ord('q')]:
                break


        print(f"Frame num: {count} | Tracked objects num: {len(track_bbs_ids)}")
        count += 1
        frame = next(video_reader)

    video_writer.release()
    cv2.destroyAllWindows()
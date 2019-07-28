import argparse
import logging
import time
import cv2
import keras
from keras.models import load_model
from keras.models import Sequential
import numpy as np
import get_distance_normalized

from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

logger = logging.getLogger('TfPoseEstimator-WebCam')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

fps_time = 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tf-pose-estimation realtime webcam')
    parser.add_argument('--camera', type=str, default=0)
    parser.add_argument('--file_name', type=str, default=0)    
    parser.add_argument('--image', type=str, default=0)
    parser.add_argument('--web_camera', type=int, default=0)
    parser.add_argument('--resize', type=str, default='0x0',
                        help='if provided, resize images before they are processed. default=0x0, Recommends : 432x368 or 656x368 or 1312x736 ')
    parser.add_argument('--resize-out-ratio', type=float, default=4.0,
                        help='if provided, resize heatmaps before they are post-processed. default=1.0')
    parser.add_argument('--model', type=str, default='mobilenet_thin', help='cmu / mobilenet_thin / mobilenet_v2_large / mobilenet_v2_small')
    parser.add_argument('--show-process', type=bool, default=False,
                        help='for debug purpose, if enabled, speed for inference is dropped.')


    args = parser.parse_args()

    logger.debug('initialization %s : %s' % (args.model, get_graph_path(args.model)))

    w, h = model_wh(args.resize)
    if w > 0 and h > 0:
        e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h))
    else:
        e = TfPoseEstimator(get_graph_path(args.model), target_size=(928, 768))
    logger.debug('cam read+')

    
    if(args.camera):
        cam = cv2.VideoCapture(args.camera)
        ret_val, image = cam.read()
    if(args.web_camera):
        cam = cv2.VideoCapture(0)
        ret_val, image = cam.read()
    if(args.image):
        image = cv2.imread(args.image)
    logger.info('cam image=%dx%d' % (image.shape[1], image.shape[0]))
    count = 0
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi',fourcc, 20.0, (int(cam.get(3)), int(cam.get(4))))    
    while(cam.isOpened()):
        if(args.camera):
            ret_val, image = cam.read()
            # image = cv2.transpose(image)
            # image = cv2.flip(image, flipCode=1)
        if(args.web_camera):
            ret_val, image = cam.read()            
        logger.debug('image process+')
        humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=args.resize_out_ratio)
        logger.debug('postprocess+')
        image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
        image_h, image_w = image.shape[:2]
        people = len(humans)
        count += 1
        if(count == 5):
            count = 0
            for human in humans:
                print(' -----------------------####  Body parts #####---------------------------')
                body_parts_present = []
                for i in human.body_parts:
                    body_parts_present.append(int(i))

                bottom_left_corner_x = int((human.body_parts[body_parts_present[0]].x)*image_w)
                bottom_left_corner_y = int((human.body_parts[body_parts_present[0]].y)*image_h)
                bottom_left_corner = (bottom_left_corner_x, bottom_left_corner_y)
                
                x_y_body_parts = [0]*38
                x_y_body_parts[0] = image_w
                x_y_body_parts[1] = image_h                                    
                for i in body_parts_present:
                    body_part = human.body_parts[i]
                    index_x = i + 2 
                    index_y = i + 2 + 18     
                    x_y_body_parts[index_x] = body_part.x 
                    x_y_body_parts[index_y] = body_part.y
                    # print(i , " " , body_part.x, " ", body_part.y)
                # print(x_y_body_parts)
                dis = get_distance_normalized.compute_distance(x_y_body_parts, 'eul', 'list')
                if(dis != -1):
                    list_body = np.asarray(dis, dtype=float)
                    li = [list_body]
                    li = np.asarray( np.asarray(li) )
                    model_new = load_model('98_normalized.h5')
                    a = model_new.predict_classes(li)
                    if(a[0][0] == 1):
                        name = "sitting"
                    elif(a[0][0] == 0):
                        name = "standing"
                    cv2.putText(image, name,
                        bottom_left_corner,
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, 
                        (0,255,0), 
                        2
                        )    

            logger.debug('show+')
            cv2.putText(image,
                        "People: %d" % (people),
                        (10, 30),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255, 255, 255), 2)
                        
            cv2.putText(image,
                        "FPS: %f" % (1.0 / (time.time() - fps_time)),
                        (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 2)
            cv2.imshow('tf-pose-estimation result', image)
            out.write(image)        
            print("------------###written###---------------")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            logger.debug('finished+')
cam.release()
out.release()
cv2.destroyAllWindows()

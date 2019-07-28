import argparse
import logging
import time
import cv2
import os
import numpy as np

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
    parser.add_argument('--img_dir', type=str, default=0)    
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
        image = str(args.image)
    if(args.img_dir):
        image_folder = str(args.img_dir)
    
    
    cwd = os.getcwd()
    dir = str(cwd)+'/'+str(image_folder)
    list = os.listdir(dir)
    for i in range(len(list)):
        list[i] = dir+"/"+str(list[i])
    print(list)
    if(args.file_name):
        name = str(args.file_name)
        training_data_file = open(name, 'a+')
    else:
        training_data_file = open('training_data', 'a+')
    numbers = []
    for i in range(17):
        numbers.append(i+1)
    for i in list:
        print(" ---------------- ### image ### --------------------")
        print(i)
        image = cv2.imread(str(i))
        logger.debug('image process+')
        humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=args.resize_out_ratio)
        logger.debug('postprocess+')
        image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
        image_h, image_w = image.shape[:2]
        people = len(humans)
        
        for human in humans:
            print(' -----------------------####  Body parts #####---------------------------')
            body_parts_present = []
            for i in human.body_parts:
                body_parts_present.append(int(i))

            bottom_left_corner_x = int((human.body_parts[body_parts_present[0]].x)*image_w)
            bottom_left_corner_y = int((human.body_parts[body_parts_present[0]].y)*image_h)
            bottom_left_corner = (bottom_left_corner_x, bottom_left_corner_y)
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            fontColor = (255,255,255)
            lineType = 2
            logger.debug('show+')        
            
            
            x_y_body_parts = [0]*38
            x_y_body_parts[0] = image_w
            x_y_body_parts[1] = image_h

            cv2.putText(image, "Standing",
                bottom_left_corner,
                font,
                fontScale, 
                fontColor, 
                lineType)
                
            for i in body_parts_present:
                body_part = human.body_parts[i]
                index_x = i + 2 
                index_y = i + 2 + 18 
                
                x_y_body_parts[index_x] = body_part.x 
                x_y_body_parts[index_y] = body_part.y
                print(i , " " , body_part.x, " ", body_part.y)
            print(x_y_body_parts)
            for i in x_y_body_parts:
                training_data_file.write(str(i))
                training_data_file.write(" ")

            training_data_file.write('\n') 
        
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
        fps_time = time.time()
        if cv2.waitKey(1) == 27:
            break
        logger.debug('finished+')

cv2.destroyAllWindows()
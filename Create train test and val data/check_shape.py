import argparse
import os
import cv2
import moviepy.editor as mp

def change_shape(video, x, y):  
    clip = mp.VideoFileClip(video)
    clip_resized = clip.resize(height=y, width = x) # make the height 360px ( According to moviePy documenation The width is then computed so that the width/height ratio is conserved.)
    name = video.split()[0]+"_resized.mp4"  
    clip_resized.write_videofile(name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tf-pose-estimation realtime webcam')
    parser.add_argument('--camera', type=str, default=0)
    parser.add_argument('--file_name', type=str, default=0)    
    parser.add_argument('--image', type=str, default=0)

    args = parser.parse_args()

    if(args.camera):
        cam = cv2.VideoCapture(args.camera)
        rev, image = cam.read()
        print(image.shape[1], image.shape[0])
        # change_shape(args.camera, 640, 352)
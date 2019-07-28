# what about the points which are 0 should the distance be means median or just the distance from neck???
# sitting_1 means that instead of nose measurement is done from middle of chest 
# cos is using cos function

import math
import argparse


def compute_distance(keypoints, choice, list_or_string):
    if(list_or_string == 'list'):
        number = keypoints
    elif(list_or_string == 'string'):
        number = keypoints.split(' ')
    else:
        print("---Wrong input---")
        exit(0)
    # print(number[0], " ", number[1])
    # for i in range(2, 18+2):
    #     print(number[i]," ", number[i+18])
    
    image_w = float(number[0])
    image_h = float(number[1])
    print(image_w, image_h)
    # x = float(number[2])            # nose (0)
    # y = float(number[2+18])         # nose (0)
    x = float(number[3])          # neck (1)
    y = float(number[3+18])       # neck (1)
    
    if(x == 0 and y == 0):
        return -1
    # i = 3                           # (0)
    i = 2                         # (1)
    distances = []
    print("---------")
    while(i < 2+18):
        if(i == 3):               # (1)
            i+=1
            continue
        a = float(number[i])
        b = float(number[i+18])
        a = a*image_w
        b = b*image_h
        if(a==0 and b==0):
            i+=1
            distances.append(0)
            continue
        print(a, " ", b, end=" ")
        i+=1
        if(choice != 'cos'):
            distances.append( math.sqrt((x-a)**2 + (y-b)**2))
            print(math.sqrt((x-a)**2 + (y-b)**2))
        else:
            distances.append( 1 - ((a*x + b*y )/((math.sqrt(a**2 + b**2))*math.sqrt(x**2+y**2))) )
            print(1 - ((a*x + b*y )/((math.sqrt(a**2 + b**2))*math.sqrt(x**2+y**2))))
    return distances

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description = 'get-distance')
    parser.add_argument('--file_input', type=str, default=0)
    parser.add_argument('--file_output', type=str, default=0)
    parser.add_argument('--cos_or_eul', type=str, default='eul')
    args = parser.parse_args()
    
    if(args.file_input):
    	file = open(args.file_input, 'r')
    else:
    	print("No input file")
    	exit(0)
    	
    if(args.file_output):
    	file_output = open(args.file_output, 'w')
    else:
    	file_output = open('output.txt', 'w')
    
    if(args.cos_or_eul):
    	choice = args.cos_or_eul
    else:
    	choice = 'eul'
    	
    	
    lines = file.readlines()	
    for i in lines:
        dis = compute_distance(i, choice, 'string')
        if(dis != -1):
            for j in dis:
                file_output.write(str(j))
                file_output.write(' ')
            file_output.write('\n')













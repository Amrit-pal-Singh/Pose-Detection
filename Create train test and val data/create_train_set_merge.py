import os
from pathlib import Path
from random import randint
import argparse


parser =argparse.ArgumentParser(description="Create Train Set")
parser.add_argument('--file_output', type=str, default = 0)
parser.add_argument('--merge1', type=str, default = 0)
parser.add_argument('--merge2', type=str, default = 0)
args = parser.parse_args()

cwd = os.getcwd()
path = Path(cwd)
list = os.listdir(path)

file1 = open( path/args.merge1 , 'r')
file2 = open( path/args.merge2 , 'r')
file_out_sample = open(args.file_output, 'w')

lines1 = file1.readlines()
lines2 = file2.readlines()
lines = lines1 + lines2

label1 = [1]*(len(lines1))
label2 = [2]*(len(lines2))
label = label1 + label2
file_out_label = open('label_' + str(args.file_output), 'w')

for i in lines:
    file_out_sample.write(i)
for i in label:
    file_out_label.write(str(i))
    file_out_label.write('\n')
    
        

    

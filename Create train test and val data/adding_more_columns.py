import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='make_columns')
    parser.add_argument('--file_input', type=str, default=0)
    parser.add_argument('--file_output', type=str, default=0)
    args = parser.parse_args()
    if(args.file_input):
        file = open(args.file_input, 'r')
    else:
        print('No input file')
        exit(0)
    
    if(args.file_output):
        file_output = open(args.file_output, 'w')
    else:
        file_output = open('output.txt', 'w')

    lines = file.readlines()
    
    if(len(lines)%5 == 0):
        limit = len(lines)
    else:
        limit = len(lines) - (len(lines)%5)

    new_lines = []
    i = 0
    while(i < limit):
        s = ""
        for j in range(5):
            lines[i+j] = lines[i+j].rstrip()
            s += lines[i+j]
            s += " "
        new_lines.append(s)
        i += 5

    for i in new_lines:
        file_output.write(i)
        file_output.write('\n')





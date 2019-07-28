import os
from pathlib import Path
from random import randint

cwd = os.getcwd()
dir = cwd+"/"+'data/'
path = Path(dir)
list = os.listdir(path)

for i in range(len(list)):
    name_out = 'test_' + str(list[i])
    list[i] = dir+list[i]
    file = open(list[i], 'r')
    file_out = open(name_out, 'w')
    lines = file.readlines()
    for j in range(40):
        rand = randint(1, 500)
        



for i in range(30):
    a = randint(1, 500)
    print(a)
    

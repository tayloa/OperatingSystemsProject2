'''
This is the main.py file for Operating Systems Project 2 F17 by Aaron Taylor, John Fantell, and Samad Farooqui.
4 Placement algorithms:
Contiguous -- Next-Fit
Contiguous -- First-Fit
Contiguous -- Best-Fit
Non-contiguous
'''

from MainMemory import *
from Process import *
import sys

# This function will get all d the arguments in the filename.
def get_instructions(file_name):
    process_list = []
    with open(file_name) as f:
        for line in f:
            if line[0] == "#":
                continue
            else:
                split_line = line.split(' ')
                name = split_line[0]
                mem = int(split_line[1])
                arrivals = []
                for i in range(2,len(split_line)):
                    temp = split_line[i].split('/')
                    arrivals.append([int(temp[0]),int(temp[1])])
                process_list.append(Process(name,mem,arrivals))
    return process_list

if __name__ == '__main__':
    processes1 = get_instructions(sys.argv[1])
    main1 = MainMemory(processes1)
    main1.run("Next")
    print('')
    processes2 = get_instructions(sys.argv[1])
    main2 = MainMemory(processes2)
    main2.run("First")
    print('')
    processes3 = get_instructions(sys.argv[1])
    main3 = MainMemory(processes3)
    main3.run("Best")
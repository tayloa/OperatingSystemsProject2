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

def print_mem(mem):
    result = ("=" * 32) + '\n'
    for i in range(len(mem)):
        if (i % 32 == 0)  and (i != 0):
            result+= mem[i] + '\n'
        else:
            result += mem[i]
    result += '\n' + ("=" * 32)
    return result

def non_contiguous(p_list):
    t = 0

    print("time {}ms: Simulator started (Non-contiguous)".format(t))
    memory = list("." * 256)
    page_table = []
    running = []
    # for i in range(len(p_list)):
    #     page_table.append([]) # the first entry in this list will be the page, second
        # is its spot in the table.
    # might not be needed

    # can convert memory to string to string using join to help print and find
    # stuff
    while (1):
        t = 0
        string_mem = ''.join(memory)
        print(memory)
        #break
        for i in range(len(p_list)):
            print("At time", t, "This process", p_list[i], "has this status of arrived:", p_list[i].arrived(t))
            string_mem = ''.join(memory)
            full = (string_mem.find(".") == -1) # this is false if there are no open spots in memory
            if (p_list[i].arrived(t) and not full): # if a process has arrived and there is space for it
                # put the process in the running list, place it in memory, and then construct it's list and put
                # it in the page table. Or tuple so it can be sorted.
                running.append(p_list[i])
                print("time {}ms: Process {} arrived (requires {} frames)".format(t, p_list[i], p_list[i].frame))
                break

        t+=1
    return

if __name__ == '__main__':
    processes1 = get_instructions(sys.argv[1])
    processes3 = list(processes1)
    processes4 = list(processes1) # for the non-contiguous memory allocation
    main1 = MainMemory(processes1)
    main1.run("Next")
    # print('')
    # processes2 = get_instructions(sys.argv[1])
    # main2 = MainMemory(processes2)
    # main2.run("First")


    # non_contiguous(processes4)

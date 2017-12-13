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

def can_be_added(string_memory, frame_num):
    counter = 0 
    counter = string_memory.count('.')
    # print("counter is: ", counter, "with string_memory: ", string_memory, "and frame_num: ", frame_num)
    if frame_num <= counter:
        return True
    return False 


def print_mem(mem_to_print):
    result = ("=" * 32) + '\n'
    for i in range(len(mem_to_print)//32+1):
        result+= "".join(mem_to_print[i*32:(i+1)*32])
        if(((i+1)*32) != 288):
            result+='\n'
    result+= ("=" * 32)
    print(result)

def print_p_table(p_table):
    print("PAGE TABLE [page,frame]:")
    for i in range(len(p_table)): # for as many things in page
        ans = ""
        ans+= p_table[i][0] + ": " # the first letter
        for j in range(1, len(p_table[i])):
            counter = 0
            if(j%10 != 0):
                ans+= "[{},{}] ".format(p_table[i][j][0], p_table[i][j][1])
            else:
                ans+= "[{},{}] ".format(p_table[i][j][0], p_table[i][j][1])
                ans += "\n"
        print(ans)

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
        string_mem = ''.join(memory)
        # print(memory)
        #break 
        for i in range(len(p_list)):
            # print("At time", t, "This process", p_list[i], "has this status of arrived:", p_list[i].arrived(t))
            # print(p_list[i], "has these arrivals:", p_list[i].arrivals)
            string_mem = ''.join(memory)
            full = (string_mem.find(".") == -1) # this is false if there are no open spots in memory
            enough_space = can_be_added(string_mem, p_list[i].frame)
            # print(p_list[i], "produces this value for can_be_added:", can_be_added(string_mem, p_list[i].frame))
            # input("ASDF")
            # print(p_list[i], "has an arrival time of: ", p_list[i].arr_t)
            if (p_list[i].arrived(t)): # if a process has arrived and there is space for it 
                print("time {}ms: Process {} arrived (requires {} frames)".format(t, p_list[i], p_list[i].frame))
                if(not full and enough_space):
                    # put the process in the running list, place it in memory, and then construct it's list and put 
                    # it in the page table. Or tuple so it can be sorted. 
                    # have to count the number of '.' in the thing in order to see 
                    print("time {}ms: Placed Process {}:".format(t, p_list[i]))
                    running.append(p_list[i])
                    page_counter = 0 # i can be frame 
                    table_list_to_add = [str(p_list[i])] # list where the first entry is the name of the list, and entries after are the 
                    # [page, frame] a list. Convert to a table later? 
                    for j in range(len(memory)): 
                        if(memory[j] == '.'): 
                            memory[j] = p_list[i].name
                            page_frame = (page_counter, j) # i is the placement in the list 
                            table_list_to_add.append(page_frame)
                            page_counter += 1
                        if(page_counter == p_list[i].frame): 
                            # should be done now 
                            page_table.append(table_list_to_add)
                            page_table.sort() # to keep in alpha order 
                            break
                    # print the memory now to see it 
                    print_mem(memory)
                    # now print page_table 
                    print_p_table(page_table)
                    #input("memory should print")
                elif(full or not enough_space): # is the full needed? 
                    # if it's the arrival time but there's not enough space or it's full (maybe about the full)
                    # then it should skip the process. To get it moving into the next thing, 
                    # should it call finished, except on it's own end time instead of the real time 
                    # in order to "fake" a finish? that's what I'm thinking. 
                    print("time {}ms: Cannot place process".format(t), p_list[i],"-- skipped!")
                    print_mem(memory)
                    print_p_table(page_table)
                    # now to actually make it so the process is the next arrival time or nah. 
                    p_list[i].finished(p_list[i].end_t) # DEBUG this should.....work...Aaron puts it in a skipped array but meh. Should always be true too 
            elif(p_list[i].finished(t)): # DEBUG I guess if it's here, then we can assume it's already in memory. If not, then 
            # may need to put it in a running list(already have one)
                print("time {}ms: Process".format(t), p_list[i], "removed:")
                # now actually need to get rid of it in memory and in the 
                # page_table 
                for l in range(len(memory)):
                    if memory[l] == p_list[i].name:
                        memory[l] = '.'
                # page_table 
                for l in range(len(page_table)):
                    # print(page_table)
                    # print("l is currently", l, "page_table[l] is: ", page_table[l])
                    # print("p_list[i] is: ", p_list[i])
                    # print(p_list[i].name == page_table[l][0])
                    # input("before removal...")
                    if(page_table[l][0] == p_list[i].name):
                        page_table.remove(page_table[l])
                        # print("this is page_table now: ", page_table)
                        # input("take a look")
                        break
                print_mem(memory)
                print_p_table(page_table)
            # in order to see if simulation is done, can go through each process in p_list and check their arrivals..and if they're in running?
            # if it's empty and running is empty, then we good to go. or have a done array or remove from 

        # should go through running and see if anything is finished, or is that handled starting at the elif(p_list[i].finished(t)) statement? 
        # DEBUG or can run through each p_list[i] again and see if all arr_t == -1, if so then we good!! 
        all_done = True
        for i in range(len(p_list)):
            if p_list[i].arr_t != -1 or p_list[i].run_t != -1 or p_list[i].end_t != -1:
                all_done = False
        if(all_done):
            print("time {}ms: Simulator ended (Non-contiguous)".format(t))
            break

        t+=1
    return 

if __name__ == '__main__':
    processes1 = get_instructions(sys.argv[1])
    processes3 = get_instructions(sys.argv[1])
    processes4 = get_instructions(sys.argv[1]) # for the non-contiguous memory allocation

    main1 = MainMemory(processes1)
    main1.run("Next")
    # print('')
    # processes2 = get_instructions(sys.argv[1])
    # main2 = MainMemory(processes2)
    # main2.run("First")
    
    print()
    non_contiguous(processes4) 
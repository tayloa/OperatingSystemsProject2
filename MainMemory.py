class MainMemory():

    def __init__(self,process_list):
        '''
        process_list: all processes that need to be used in the simulation
        memory: string representation of physical memory
        algo: placement algorithm to be used
        running: list of running processes in the format [ process object ]
        '''
        self.process_list = process_list
        self.memory = list("." * 256)
        self.algo = ""
        self.running = []
        self.moved = [] #Processes moved in defrag

    def __str__(self):
        result = ("=" * 32) + '\n'
        for i in range(len(self.memory)//32+1):
            result+= "".join(self.memory[i*32:(i+1)*32])
            if(((i+1)*32) != 288):
                result+='\n'
        result+= ("=" * 32)
        return result

    # Placement algorithms for each process
    def next_fit(self,prev_process_end,process):

        # Start looking after the end of the last process starting index
        for i in range(prev_process_end, len(self.memory)):
            if ("".join(self.memory[i:(i + process.frame)])) == ("." * process.frame):
                self.memory[i:(i + process.frame)] = [str(process) for char in self.memory[i:(i + process.frame)]]
                self.running.append(process)
                return True

        # Start looking at the start of memory
        for i in range(0, prev_process_end):
            if ("".join(self.memory[i:(i + process.frame)])) == ("." * process.frame):
                self.memory[i:(i + process.frame)] = [str(process) for char in self.memory[i:(i + process.frame)]]
                self.running.append(process)
                return True
        return False

    def first_fit(self,process):
        #Convert self.memory (a list) to a string
        tmp = ''.join(self.memory)
        #Create string of '.' equal to the length of the process frames
        empty_string = '.'*process.frame
        #Find the first instance of this '.' string in memory
        #If one does not exist, no partition large enough to hold process
        if tmp.find(empty_string) == -1:
            return False
        #Otherwise, add process to memory and add it to list of running proccesses
        else:
            #Start index : Stop index
            self.memory[tmp.find(empty_string) : (tmp.find(empty_string)+process.frame)] = [str(process) for i in range(process.frame)]
            self.running.append(process)
            return True

    def best_fit(self,process):
        mincount = 100000000 #Arbitrarily large number at start; used to compare free memory partition sizes
        minposition = -1 #Starting index of the smallest free memory partition in memory

        count = 0 #Number of free frames in the current free memory partition
        position = 0 #Starting index of current free memory partiotion

        for i in range(len(self.memory)):
            if(self.memory[i] == '.'):
                if count == 0: #Start of new free memory partition
                    position = i #Save position
                # Case: *****...........
                # where * could be any character followed by all '.'
                count+=1
                if i == 255:
                    #print("Count: {} Mincount: {} Partition Size {}\n").format(count,mincount,process.frame)
                    if((count < mincount) and (count>=process.frame)): #If the current partition size is smaller than the smallest one seen thus far
                        mincount = count
                        minposition = position #Record the start index of this partition
                    count = 0
            else:
                if count > 0: #Meaning the last element was a '.'
                    #print("Count: {} Mincount: {} Partition Size {}\n").format(count,mincount,process.frame)
                    if((count < mincount) and (count>=process.frame)): #If the current partition size is smaller than the smallest one seen thus far
                        mincount = count
                        minposition = position #Record the start index of this partition
                    count = 0
        if(minposition == -1):
            return False
        #Otherwise, add process to memory and add it to list of running proccesses
        else:
            self.memory[minposition : minposition+process.frame] = [str(process) for i in range(process.frame)]
            self.running.append(process)
            return True

    def non_contiguous(self,process):
        return False

    # Returns a formatted string of all currently running processes
    def get_current_frames(self):
        result = ""
        processes = [str(p) for p in self.moved]
        processes.sort()
        for i in range(len(processes)):
            if i == len(processes) - 1:
                result+= processes[i]
            else:
                result+= processes[i] + ", "
        return result

    # Defrag memory to make space for a new process
    def defrag(self,t):
        self.moved = [] #Reset list of processes moved
        temp = "".join(self.memory)
        #Find all processes before '.'
        index = temp.find('.')
        unmoved = []
        for i in range(index):
            if str(self.memory[i]) not in unmoved:
                unmoved.append(str(self.memory[i]))
        for i in range(len(self.running)):
            if str(self.running[i]) not in unmoved:
                self.moved.append(str(self.running[i]))
        temp = temp.replace(".", "")
        free_space = len(self.memory) - len(temp)
        temp += ("." * free_space)
        self.memory = [c for c in temp]
        return len(self.memory) - free_space - index

    # Place the process based on the algorithm
    def place(self,prev_process_end,process):
        placed = False
        if self.algo == "Next":
            # Find the index where last process ended and prev_process_end searching for free memory after it
            placed = self.next_fit(prev_process_end, process)
        elif self.algo == "Best":
            placed = self.best_fit(process)
        elif self.algo == "First":
            placed = self.first_fit(process)
        # non_contiguous placement algorithms
        else:
            pass
        return placed

    # Run the simulation with a specific placement algorithm
    def run(self, algo):
        # Run the simulation unitl all processes are finished
        t = 0
        self.algo = algo
        print("time {}ms: Simulator started (Contiguous -- {}-Fit)".format(t,algo))
        skipped = []
        prev_process_end = 0 # Ending frame (index) of the last process we placed, used for Next-fir algorithm

        while (1):

            # Check if a process finished
            # If a process is finished we will "remove it" from running by not adding it to unfinished
            unfinished = [] # keep unfinished processes
            for process in self.running:
                if process.finished(t):

                    # Convert memory to string form for easy manipulation
                    temp = "".join(self.memory)

                    # Remove the process by replacing it with free space
                    temp = temp.replace(str(process), ".")

                    # Convert the string back to a list
                    self.memory = [c for c in temp]

                    print("time {}ms: Process {} removed:".format(t, process))
                    print(self)

                    # Save processes that still have cycles to complete
                    if process.arr_t != -1:
                        self.process_list.append(process)
                else:
                    unfinished.append(process)

            # Sort the lists based on process name and arrival time
            self.running = sorted(unfinished, key = lambda x: (x.end_t,x.name)) # Save the list of unfinished processes as the new running

            unarrived = [] # keep track of unarrived processes

            self.process_list.sort(key = lambda x: (x.arr_t,x.name))

            for process in self.process_list:

                # Check if a process arrived
                if process.arrived(t):

                    # Check if the process is in memory
                    if str(process) not in self.memory:
                        print("time {}ms: Process {} arrived (requires {} frames)".format(t, process, process.frame ))
                        placed = False

                        # Add the process to the prev_process_end if memory is empty
                        if "".join(self.memory) == len(self.memory) * ".":
                            # Check if the process was actually placed
                            if self.place(0, process) == True:
                                print("time {}ms: Placed process {}:".format(t, process))
                                print(self)
                                prev_process_end = (''.join(self.memory).rfind(str(process))) + 1
                                continue

                        # Check if there is enough space to add the process, then try adding it
                        if ("".join(self.memory)).count(".") >= process.frame:

                            if self.place(prev_process_end,process) == True:
                                print("time {}ms: Placed process {}:".format(t, process))
                                prev_process_end = (''.join(self.memory).rfind(str(process))) + 1
                                print(self)

                            # Defrag and then try adding the process
                            else:
                                print("time {}ms: Cannot place process {} -- starting defragmentation".format(t,process))
                                t_units = self.defrag(t)
                                t += t_units
                                current_frames = self.get_current_frames()

                                print("time {}ms: Defragmentation complete (moved {} frames: {})".format(t, t_units, current_frames))
                                prev_process_end = (''.join(self.memory).find("."))
                                print(self)
                                if self.place(prev_process_end,process) == True:
                                    print("time {}ms: Placed process {}:".format(t, process))
                                    prev_process_end = (''.join(self.memory).rfind(str(process)))
                                    print(self)

                                # Adjust all current and future times to account for defragmentation
                                for p in self.running:

                                    # Be careful not to adjust processes that are in both lists
                                    p.adjust_times(t_units)
                                for p in self.process_list:

                                    # Be careful not to adjust processes that are in both lists
                                    if p not in self.running:
                                        p.adjust_times(t_units)

                                prev_process_end = (''.join(self.memory).rfind(str(process)))
                        else:
                            print("time {}ms: Cannot place process {} -- skipped!".format(t,process))

                            # Move on to the process's next arrival time if it is skipped
                            process.next_arr_t()
                            if process.arr_t != -1:
                                unarrived.append(process)
                            print(self)
                else:
                    if process.arr_t != -1:
                        unarrived.append(process)

            # Sort the lists based on process name and arrival time
            self.process_list = sorted(unarrived, key = lambda x: (x.arr_t,x.name))
            self.running.sort(key = lambda x: (x.end_t,x.name))

            if len(self.process_list) == 0 and len(self.running) == 0:
                break
            t = t + 1
        print("time {}ms: Simulator ended (Contiguous -- {}-Fit)".format(t, algo))

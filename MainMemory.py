class MainMemory():

    def __init__(self,process_list):
        '''
        process_list: all processes that need to be used in the simulation
        memory: string representation of physical memory
        algo: placement algorithm to be used
        running: list of running processes in the format
            [
               process object,
               [frame range the process takes up]
            ]
        '''
        self.process_list = process_list
        self.memory = list("." * 256)
        self.algo = ""
        self.running = []

    def __str__(self):
        result = ("=" * 32) + '\n'
        for i in range(len(self.memory)):
            if (i % 32 == 0)  and (i != 0):
                result+= self.memory[i] + '\n'
            else:
                result += self.memory[i]
        result += '\n' + ("=" * 32)
        return result

    # Placement algorithms for each process
    def next_fit(self,start,process):

        # Find a free range after the end index of the most recently added process
        if ("".join(self.memory[start:(start + process.frame)])) == ("." * process.frame):
            self.memory[start:(start + process.frame)] = [str(process) for char in self.memory[start:(start + process.frame)]]
            self.running.append([process,[]])
            return True
        return False

    def best_fit(self,process):
        return False

    def first_fit(self,process):
        return False

    def non_contiguous(self,process):
        return False

    # Returns a formatted string of all currently running processes
    def get_current_frames(self):
        result = ""
        processes = [str(pair[0]) for pair in self.running]
        processes.sort()
        for i in range(len(processes)):
            if i == len(processes) - 1:
                result+= processes[i]
            else:
                result+= processes[i] + ", "
        return result

    # Defrag memory to make space for a new process
    def defrag(self,t):
        temp = "".join(self.memory)
        temp = temp.replace(".", "")
        free_space = len(self.memory) - len(temp)
        temp += ("." * free_space)
        self.memory = [c for c in temp]
        return len(self.memory) - free_space

    # Place the process based on the algorithm
    def place(self,start,process):
        placed = False
        if self.algo == "next":
            # Find the index where last process ended and start searching for free memory after it
            placed = self.next_fit(start, process)
        elif self.algo == "best":
            pass
        elif self.algo == "first":
            pass
        # non_contiguous placement algorithms
        else:
            pass
        return placed

    # Run the simulation with a specific placement algorithm
    def run(self, algo):
        # Run the simulation unitl all processes are finished
        t = 0
        self.algo = algo
        print("time {}ms: Simulator started (Contiguous -- Next-Fit)".format(t))
        skipped = []
        last_placed = "" # The last process we added or removed

        while (1):

            # Check if a process finished
            unfinished = [] # keep unfinished processes
            for pair in self.running:
                process = pair[0]
                if process.finished(t):
                    temp = "".join(self.memory)
                    temp = temp.replace(str(process), ".")
                    self.memory = [c for c in temp]
                    print("time {}ms: Process {} removed:".format(t, process))
                    print(self)
                    if process.arr_t != -1:
                        self.process_list.append(process)
                else:
                    unfinished.append(pair)
            self.running = unfinished

            # Check if a process arrived
            unarrived = [] # keep track of unarrived processes
            for process in self.process_list:
                if process.arrived(t):

                    # Place the processes in a frame depending on the algorithm
                    # Check if the process is in memory
                    if str(process) not in self.memory and str(process) not in skipped:
                        print("time {}ms: Process {} arrived (requires {} frames)".format(t, process, process.frame ))
                        placed = False
                        print(last_placed)

                        # Add the process to the start if memory is empty
                        if "".join(self.memory) == len(self.memory) * ".":
                            if self.place(0, process) == True:
                                print("time {}ms: Placed process {}:".format(t, process))
                                print(self)
                                continue

                        # Check if there is enough space to add the process, then try adding it
                        if ("".join(self.memory)).count(".") >= process.frame:

                            # Next-fit
                            # get end location of last placed process
                            start = (''.join(self.memory).rfind(last_placed)) + 1
                            # If there is not enough space for the process after this location, set the start to 0
                            if len(("".join(self.memory[start:len(self.memory)]))) < process.frame:
                                start = 0
                            if self.place(start,process) == True:
                                print("time {}ms: Placed process {}:".format(t, process))
                                last_placed = str(process)
                                print(self)

                            # Defrag and then try adding the process
                            else:
                                print("time {}ms: Cannot place process {} -- starting defragmentation".format(t,process))
                                t_units = self.defrag(t)
                                t += t_units
                                current_frames = self.get_current_frames()
                                print("time {}ms: Defragmentation complete (moved {} frames: {})".format(t, t_units, current_frames))
                                start = (''.join(self.memory).find("."))
                                if self.place(start,process) == True:
                                    print("time {}ms: Placed process {}:".format(t, process))
                                    last_placed = str(process)
                                    print(self)

                                # Adjust all current and future times to account for defragmentation
                                for pair in self.running:
                                    pair[0].adjust_times(t_units)
                                    pair[0].end_t += t_units # Adjust end times of currently running processes
                                for p in self.process_list:
                                    p.adjust_times(t_units)
                                    p.arr_t += t_units
                                    p.end_t += t_units

                                last_placed = str(process)
                        else:
                            print("time {}ms: Cannot place process {} -- skipped!".format(t,process))
                            skipped.append(str(process))
                            print(self)
                else:
                    unarrived.append(process)
            self.process_list = unarrived

            if (len(self.process_list) == 0 and len(self.running) == 0):
                break
            t = t + 1
        print("time {}ms: Simulator ended ({})".format(t, algo))

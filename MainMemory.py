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
            return True
        return False

    def best_fit(self,process):
        return False

    def first_fit(self,process):
        return False

    def non_contiguous(self,process):
        return False

    # Defrag memory to make space for a new process
    def defrag(self,t):
        temp = "".join(self.memory)
        temp = temp.replace(".", "")
        free_space = len(self.memory) - len(temp)
        temp += ("." * free_space)
        self.memory = [c for c in temp]
        # print("time {}ms: Defragmentation complete (moved {} frames: B, C, D, E, F)".format(t, free_space))
        return free_space

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
        last_placed = "" # The last process we added
        while (1):

            # Check if a process finished
            unfinished = []
            for pair in self.running:
                process = pair[0]
                if process.finished(t):
                    # print(self)
                    temp = "".join(self.memory)
                    temp = temp.replace(str(process), ".")
                    self.memory = [c for c in temp]
                    print("time {}ms: Process {} removed:".format(t, process))
                    if process.arr_t != -1:
                        self.process_list.append(process)
                else:
                    unfinished.append(pair)
            self.running = unfinished

            # Check if a process arrived
            unarrived = []
            for process in self.process_list:
                if process.arrived(t):
                    self.running.append([process,[]])
                    for p in self.running:
                        pro = p[0]
                else:
                    unarrived.append(process)
            self.process_list = unarrived

            # Place the processes in a frame depending on the algorithm
            for pair in self.running:
                process = pair[0]
                if str(process) not in self.memory:
                    print("time {}ms: Process {} arrived (requires {} frames)".format(t, process, process.frame ))
                    placed = False

                    # Check if memory is full
                    if '.' not in self.memory:
                        continue
                        print("time {}ms: Cannot place process {} -- skipped!".format(t,process))


                    # Add the process to the start if memory is empty
                    if "".join(self.memory) == len(self.memory) * ".":
                        self.memory[0:(process.frame)] = [str(process) for char in self.memory[0:(process.frame)]]
                        placed = True
                        print("time {}ms: Placed process {}:".format(t, process))
                        last_placed = str(process)
                    else:
                        start = (''.join(self.memory).rfind(last_placed)) + 1
                        if self.place(start,process) == True:
                            print("time {}ms: Placed process {}:".format(t, process))
                            last_placed = str(process)
                        else:
                            if ("".join(self.memory)).count(".") >= process.frame:
                                # print("time {}ms: Cannot place process {} -- starting defragmentation".format(t,process))
                                # print(self)
                                if self.defrag(t) > 0:
                                    self.place(start,process)
                            else:
                                # print("time {}ms: Cannot place process {} -- skipped!".format(t,process))
                                process.arr_t = t + 1
            if (len(self.process_list) == 0 and len(self.running) == 0):
                break
            t = t + 1
        print("time {}ms: Simulator ended ({})".format(t, algo))

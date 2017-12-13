class Process:

    def __init__(self, name, mem, arrivals):
        self.name = name
        self.frame = mem
        self.arrivals = arrivals
        self.arr_t = -1
        self.run_t = -1
        self.end_t = -1

        # Set the first arrival and run time for the process
        if len(arrivals) > 0:
            pair = arrivals.pop(0)
            self.arr_t = pair[0]
            self.run_t = pair[1]
            self.end_t = pair[0] + pair[1]

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    # Check if the process arrives at a given time
    def arrived(self,t):
        if self.arr_t != -1:
            if self.arr_t == t:
                return True
        return False

    # Adjust all future arrival times after defragmentation occurs
    def adjust_times(self,t):
        if len(self.arrivals) > 0:
            for pair in self.arrivals:
                pair[0] += t
        if self.arr_t != -1 and self.end_t != -1:
            self.arr_t += t
            self.end_t += t

    # Move on to the next arrival time if the process is skipped or finished
    def next_arr_t(self):
        if len(self.arrivals) > 0:
            pair = self.arrivals.pop(0)
            self.arr_t = pair[0]
            self.run_t = pair[1]
            self.end_t = pair[0] + pair[1]
        else:
            self.arr_t = -1
            self.run_t = -1
            self.end_t = -1
        return True

    def finished(self,t):
        if self.end_t != -1:
            if self.end_t == t:
                self.next_arr_t()
                return True
        return False

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

    # Check if the process arrives at a given time
    def arrived(self,t):
        if self.arr_t != -1:
            if self.arr_t == t:
                return True
        return False

    def finished(self,t):
        if self.end_t != -1:
            if self.end_t == t:
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
        return False

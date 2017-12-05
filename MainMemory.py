class MainMemory():

    def __init__(self,process_list):

        processes = {} #{} #Key = process name, value = process object
        self.Matrix = [["." for x in range(32)] for y in range(8)]


    def __str__(self):
        result = ("=" * 32) + '\n'
        for row in self.Matrix:
            result += (''.join(map(str,row))) + '\n'
        result += ("=" * 32)
        return result

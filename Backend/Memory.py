class Memory:

    def __init__(self):
        self.memoryCap = 100
        self.mainMemory = []      

        for i in range(self.memoryCap): #initialize memory with all 0's
            self.mainMemory.append(0)
            
    def mainmemory(self):
        return self.mainMemory
    
class Memory:

    def __init__(self):
        self.memory_cap = 100
        self.main_memory = []      

        for i in range(self.memory_cap): #initialize memory with all 0's
            self.main_memory.append(0)
            
    def main_memory(self):
        return self.main_memory
    
class Memory:

    def __init__(self):
        self.memory_cap = 100
        self._main_memory = []
        self.just_loaded = False

        for i in range(self.memory_cap): #initialize memory with all 0's
<<<<<<< Updated upstream
            self._main_memory.append(0)
=======
            self._main_memory.append(None)
>>>>>>> Stashed changes
            
    def main_memory(self):
        return self._main_memory
    
    def expand(self, operand):
        while len(self._main_memory)-1 < operand:
            self._main_memory.append(0)

    def insert(self, operand, input):
        self.expand(operand)
        self._main_memory[operand] = input
    
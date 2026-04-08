class Memory:

    def __init__(self):
        self.memory_cap = 250
        self._main_memory = [0] * self.memory_cap
            
    def main_memory(self):
        return self._main_memory
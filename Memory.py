class Memory():
    def __init__(self):
        self.mainMemory = []
        self.memoryCap = 100

    def initialize(self):
        for i in range(self.memoryCap):
            self.mainMemory[i] = 0
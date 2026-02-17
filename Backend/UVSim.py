from UserProgram import UserProgram
from Memory import Memory
from cpu import CPU

class UVSim:
    def __init__(self):
        self.memory = Memory()
        self.cpu = CPU(self.memory)
        self.userProgram = UserProgram()

    def loadProgram(self, userProgram):
        for i, word in enumerate(userProgram.program):
            self.memory.mainMemory[i] = int(word)

    def runProgram(self):
        while True:
            if self.cpu.fetch() is False:
                self.cpu.dump()
                break
            else:
                self.cpu.decode()
                self.cpu.execute()


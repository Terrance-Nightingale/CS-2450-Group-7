import copy
from Memory import Memory
from cpu import CPU

class UVSim:
    def __init__(self):
        self.memory = Memory()
        self.cpu = CPU()

    def loadProgram(self, userProgram):
        self.memory.mainMemory = copy.deepcopy(userProgram.program)

    def runProgram(self):
        while True:
            if self.cpu.fetch() is False:
                self.cpu.dump()
                break
            else:
                self.cpu.decode()
                self.cpu.execute()


from Backend.UserProgram import UserProgram
from Backend.Memory import Memory
from Backend.cpu import CPU

class UVSim:
    def __init__(self):
        self.memory = Memory()
        self.cpu = CPU(self.memory)
        self.userProgram = UserProgram()

    def loadProgram(self, userProgram):
        '''
        Loads the user's program into memory.
        '''
        for i, word in enumerate(userProgram.program):
            self.memory.mainMemory[i] = int(word)

    def runProgram(self):
        '''
        Decodes and runs the user's program.
        '''
        while self.cpu.fetch():
                self.cpu.decode()
                self.cpu.execute()

    def resetProgram(self):    
        '''
        Excecute's the CPU's reset function.
        '''    
        self.cpu.reset()

from Backend.UserProgram import UserProgram
from Backend.Memory import Memory
from Backend.cpu import CPU
from Backend.BasicML import BasicML

class UVSim:
    def __init__(self, inputPanel = None, inputInfoPanel = None):
        self.memory = Memory()
        self.cpu = CPU(self.memory)
        self.userProgram = UserProgram()
        self.cpu.basicml = BasicML(inputInfoPanel)

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

                # Check if this is a READ instruction
                if self.cpu.opcode == 10:
                    return  # Pause and exit loop, GUI will handle READ
                self.cpu.execute()

    def resetProgram(self):    
        '''
        Excecute's the CPU's reset function.
        '''    
        self.cpu.reset()

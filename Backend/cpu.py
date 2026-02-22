from Backend.BasicML import BasicML
from Backend.Memory import Memory

class CPU:
    def __init__(self, memory):
        self.memory = memory
        self.basicml = BasicML()
        self.instructionCounter = 0
        self.instructionRegister = 0
        self.opcode = 0
        self.operand = 0
        self.accumulator = 0
        self.running = True
        self.errorMessage = ""

    def fetch(self):
        if not self.running:
            return False
        
        if self.instructionCounter >= len(self.memory.mainMemory):
            return False

        self.instructionRegister = self.memory.mainMemory[self.instructionCounter]
        self.instructionCounter += 1
        return True

    def decode(self):
        self.opcode = self.instructionRegister // 100
        self.operand = self.instructionRegister % 100

    def execute(self):
        match(self.opcode):
            case 0:
                pass
            case 10: #READ
                self.basicml.read(self.memory.mainMemory, self.operand)
                return
            case 11: #WRITE
                self.basicml.write(self.memory.mainMemory, self.operand)
            case 20: #LOAD
                self.accumulator = self.basicml.load(self.memory.mainMemory, self.operand)
            case 21: #STORE
                self.basicml.store(self.memory.mainMemory, self.operand, self.accumulator)
            case 30: #ADD
                self.accumulator = self.basicml.add(self.memory.mainMemory, self.operand, self.accumulator)
            case 31: #SUBTRACT
                self.accumulator = self.basicml.subtract(self.memory.mainMemory, self.operand, self.accumulator)
            case 32: #DIVIDE
                self.accumulator = self.basicml.divide(self.memory.mainMemory, self.operand, self.accumulator)
            case 33: #MULTIPLY
                self.accumulator = self.basicml.multiply(self.memory.mainMemory, self.operand, self.accumulator)
            case 40: #BRANCH
                self.instructionCounter = self.basicml.branch(self.operand)
            case 41: #BRANCHNEG
                self.instructionCounter = self.basicml.branchNeg(self.operand, self.instructionCounter, self.accumulator)
            case 42: #BRANCHZERO
                self.instructionCounter = self.basicml.branchZero(self.operand, self.instructionCounter, self.accumulator)
            case 43: #HALT
                self.running = self.basicml.halt()
            case _:
                self.errorMessage = f"Invalid opcode: {self.opcode}"
                self.running = False

    def dump(self):
        '''
        Prints contents of CPU to console. Useful for debugging.
        '''
        print("CPU DUMP")
        print(f"Accumulator: {self.accumulator}")
        print(f"Instr Reg: {self.instructionRegister}")
        print(f"Instr Counter: {self.instructionCounter}")
        print(f"Running: {self.running}")
        print(f"Opcode: {self.opcode}")
        print(f"Operand: {self.operand}")
        # print("--MEMORY CONTENTS--")
        # for i in range(100):
        #     print(self.memory.mainMemory[i])
        
    def reset(self):
        '''
        Resets the contents of the CPU to 0.
        '''
        for i in range(len(self.memory.mainMemory) - 1):
            self.memory.mainMemory[i] = 0

        self.instructionCounter = 0
        self.instructionRegister = 0
        self.opcode = 0
        self.operand = 0
        self.accumulator = 0
        self.running = True
        self.errorMessage = ""

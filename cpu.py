from BasicML import BasicML
from Memory import Memory

class CPU:
    def __init__(self, memory):
        self.memory = memory
        self.basicml = BasicML()
        self.memoryCap = 100
        self.instructionCounter = 0
        self.instructionRegister = 0
        self.opcode = 0
        self.operand = 0
        self.accumulator = 0
        self.running = True

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
            case 10:
                self.basicml.read(self.memory.mainMemory, self.operand)
            case 11:
                self.basicml.write(self.memory.mainMemory, self.operand)
            case 20:
                self.basicml.load(self.memory.mainMemory, self.operand, self.accumulator)
            case 21:
                self.basicml.store(self.memory.mainMemory, self.operand, self.accumulator)
            case 30:
                self.accumulator = self.basicml.add(self.memory.mainMemory, self.operand, self.accumulator)
            case 31:
                self.basicml.subtract(self.memory.mainMemory, self.operand, self.accumulator)
            case 32:
                self.basicml.divide(self.memory.mainMemory, self.operand, self.accumulator)
            case 33:
                self.basicml.multiply(self.memory.mainMemory, self.operand, self.accumulator)
            case 40:
                self.basicml.branch(self.memory.mainMemory, self.operand)
            case 41:
                self.basicml.branchNeg(self.memory.mainMemory, self.operand, self.accumulator)
            case 42:
                self.basicml.branchZero(self.memory.mainMemory, self.operand, self.accumulator)
            case 43:
                self.basicml.halt(self.running)
            case _:
                print("Invalid")

    def dump(self):
        print("CPU DUMP")
        print(f"Accumulator: {self.accumulator}")
        print(f"Instr Reg: {self.instructionRegister}")
        print(f"Instr Counter: {self.instructionCounter}")
        print(f"Running: {self.running}")
        print(f"Opcode: {self.opcode}")
        print(f"Operand: {self.operand}")

        for i in range(100):
            print(self.memory.mainMemory[i])
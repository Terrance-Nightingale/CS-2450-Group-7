from Backend.BasicML import BasicML
from Backend.Memory import Memory

class CPU:
    def __init__(self, memory):
        self.memory = memory
        self.basicml = BasicML()
        self.instruction_counter = 0
        self.instruction_register = 0
        self.opcode = 0
        self.operand = 0
        self.accumulator = 0
        self.running = True
        self.error_message = ""

    def fetch(self):
        if not self.running:
            return False
        
        if self.instruction_counter >= len(self.memory.main_memory):
            return False

        self.instruction_register = self.memory.main_memory[self.instruction_counter]
        self.instruction_counter += 1
        return True

    def decode(self):
        self.opcode = self.instruction_register // 100
        self.operand = self.instruction_register % 100

    def execute(self):
        match(self.opcode):
            case 0:
                pass
            case 10: #READ
                self.basicml.read(self.memory.main_memory, self.operand)
                return
            case 11: #WRITE
                self.basicml.write(self.memory.main_memory, self.operand)
            case 20: #LOAD
                self.accumulator = self.basicml.load(self.memory.main_memory, self.operand)
            case 21: #STORE
                self.basicml.store(self.memory.main_memory, self.operand, self.accumulator)
            case 30: #ADD
                self.accumulator = self.basicml.add(self.memory.main_memory, self.operand, self.accumulator)
            case 31: #SUBTRACT
                self.accumulator = self.basicml.subtract(self.memory.main_memory, self.operand, self.accumulator)
            case 32: #DIVIDE
                self.accumulator = self.basicml.divide(self.memory.main_memory, self.operand, self.accumulator)
            case 33: #MULTIPLY
                self.accumulator = self.basicml.multiply(self.memory.main_memory, self.operand, self.accumulator)
            case 40: #BRANCH
                self.instruction_counter = self.basicml.branch(self.operand)
            case 41: #BRANCHNEG
                self.instruction_counter = self.basicml.branch_neg(self.operand, self.instruction_counter, self.accumulator)
            case 42: #BRANCHZERO
                self.instruction_counter = self.basicml.branch_zero(self.operand, self.instruction_counter, self.accumulator)
            case 43: #HALT
                self.running = self.basicml.halt()
            case _:
                self.error_message = f"Invalid opcode: {self.opcode}"
                self.running = False
        if self.basicml.error_message:
            self.error_message = self.basicml.error_message
            self.running = False

    def dump(self):
        '''
        Prints contents of CPU to console. Useful for debugging.
        '''
        print("CPU DUMP")
        print(f"Accumulator: {self.accumulator}")
        print(f"Instr Reg: {self.instruction_register}")
        print(f"Instr Counter: {self.instruction_counter}")
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
        for i in range(len(self.memory.main_memory) - 1):
            self.memory.main_memory[i] = 0

        self.instruction_counter = 0
        self.instruction_register = 0
        self.opcode = 0
        self.operand = 0
        self.accumulator = 0
        self.running = True
        self.error_message = ""

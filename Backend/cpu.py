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
        
        if self.instruction_counter >= len(self.memory.main_memory()):
            self.running = False
            return False

        self.instruction_register = self.memory.main_memory()[self.instruction_counter]
        self.instruction_counter += 1
        return True

    def decode(self):
        """Parses BasicML code for the next instruction, and sets 
        the opcode and the memory address of the operand if valid"""
        code_length = len(str(abs(self.instruction_register)))
        if code_length <= 4:
            opcode = self.instruction_register // 100
            operand = self.instruction_register % 100
        elif code_length == 5:
            opcode = self.instruction_register // 1000
            operand = self.instruction_register % 1000
        if self.validate_code(opcode) and self.validate_address(operand):
            self.opcode = opcode
            self.operand = operand
        else: raise ValueError("code or address invalid")

    def validate_code(self, ml_code):
        """checks code is a valid BasicML code"""
        if ml_code in (0, 10, 11, 20, 21, 30, 31, 32, 33, 40, 41, 42, 43):
            return True
        else: raise ValueError("Code must be a valid BasicML code")

    def validate_address(self, a):
        """checks address/opcode is a valid memory address"""
        if 0 < a or a < self.memory.memory_cap-1:
            return True
        else:
            raise ValueError("memory address must be between 0-249")


    def execute(self):
        match(self.opcode):
            case 0:
                pass
            case 10: #READ
                self.basicml.read(self.memory.main_memory(), self.operand)
                return
            case 11: #WRITE
                self.basicml.write(self.memory.main_memory(), self.operand)
            case 20: #LOAD
                self.accumulator = self.basicml.load(self.memory.main_memory(), self.operand)
            case 21: #STORE
                self.basicml.store(self.memory.main_memory(), self.operand, self.accumulator)
            case 30: #ADD
                self.accumulator = self.basicml.add(self.memory.main_memory(), self.operand, self.accumulator)
            case 31: #SUBTRACT
                self.accumulator = self.basicml.subtract(self.memory.main_memory(), self.operand, self.accumulator)
            case 32: #DIVIDE
                self.accumulator = self.basicml.divide(self.memory.main_memory(), self.operand, self.accumulator)
            case 33: #MULTIPLY
                self.accumulator = self.basicml.multiply(self.memory.main_memory(), self.operand, self.accumulator)
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
        if self.basicml.error_message: # TODO: Error messages for the InputInfoPanel would be pulled from here perhaps?
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
        #for i in range(len(self.memory.main_memory()) - 1):
        #    self.memory.main_memory()[i] = 0
        self.memory.main_memory().clear()

        self.basicml.console_panel.reset_outputs() # Reset's the console's display.
                                                 # Added by: Josh 3/18/2026

        self.instruction_counter = 0
        self.instruction_register = 0
        self.opcode = 0
        self.operand = 0
        self.accumulator = 0
        self.running = True
        self.error_message = ""

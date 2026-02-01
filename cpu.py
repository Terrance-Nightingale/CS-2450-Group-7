class CPU:
    def __init__(self, memory):
        self.memory = memory
        self.memoryCap = 100
        self.instructionCounter = 0
        self.instructionRegister = 0
        self.opcode = 0
        self.operand = 0
        self.accumulator = 0

    def execute(self):
        while True:
            self.instructionRegister = self.memory[self.instructionCounter]
            self.instructionCounter += 1

            self.opcode = self.instructionRegister // 100
            self.operand = self.instructionRegister % 100

            #Currently filled with placeholder values - We have to add to this
            match(self.opcode):
                case 10:
                    print("READ")
                case 11:
                    print("WRITE")
                case 20:
                    print("LOAD")
                case 21:
                    print("STORE")
                case 30:
                    print("ADD")
                case 31:
                    print("SUBTRACT")
                case 32:
                    print("DIVIDE")
                case 33:
                    print("MULTIPLY")
                case 40:
                    print("BRANCH")
                case 41:
                    print("BRANCHNEG")
                case 42:
                    print("BRANCHZERO")
                case 43:
                    self.dump()
                    break
                case _:
                    print("Invalid")

    def dump(self):
        print(self.instructionRegister)
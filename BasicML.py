class BasicML:
    def __init__(self):
        pass

    
    def read(self, memory, operand):
        '''
        Reads a word from the keyboard into a location in memory specified by the operand.
        '''
        while True:
            read_input = input("Enter a 4-digit word: ") # Receives input from user.
            inputInt = int(read_input) # Converts from string to int.
            if(-9999 <= inputInt <= 9999):
                memory[operand] = inputInt
                break
            else:
                print("Number must be between -9999 and 9999.")
        
        

    def write(self, memory, operand):
        '''
        Writes a word from a location in memory specified by the operand to screen.
        '''
        output = memory[operand] # Pulls the word from memory.
        print(output) # Prints the word as the output.


    def load(self, memory, operand):
        '''
        Returns a word from a location in memory specified by the operand.
        This value is intended to be stored in the accumulator.
        '''
        return memory[operand]


    def store(self, memory, operand, accumulator):
        '''
        Store a word from the accumulator into a location in memory specified by the operand.
        '''
        memory[operand] = accumulator
        

    def add(self, memory, operand, accumulator):
        '''
        Adds a word from a location in memory specified by the operand to the word in the accumulator
        and returns the result.
        '''
        return accumulator + memory[operand]


    def subtract(self, memory, operand, accumulator):
        '''
        Subtracts a word from a location in memory specified by the operand from the word in the accumulator
        and returns the result.
        '''
        return accumulator - memory[operand]

    
    def divide(self, memory, operand, accumulator):
        '''
        Divides the word in the accumulator by a word from a location specified by the operand in memory.
        Returns the result.
        '''
        if memory[operand] == 0: # Checks memory value to prevent division by zero.
            print("Error: Division by zero.")
        else:
            return accumulator / memory[operand]

    def multiply(self, memory, operand, accumulator):
        '''
        Multiplies a word from a location in memory specified by the operand to the word in the accumulator.
        Returns the result.
        '''
        return accumulator * memory[operand]


    def branch(self, operand):
        '''
        Returns the location to be branched to in memory specified by the operand.
        '''
        return operand


    def branchNeg(self, operand, instructionCounter, accumulator):
        '''
        Returns the location to be branched to in memory specified by the operand if the accumulator is negative.
        '''
        if accumulator < 0:
            return operand
        else:
            return instructionCounter


    def branchZero(self, operand, instructionCounter, accumulator):
        '''
        Returns the location to be branched to in memory specified by the operand if the accumulator is zero.
        '''
        if accumulator == 0:
            return operand
        else:
            return instructionCounter


    def halt(self):
        '''
        Pauses the program.
        '''
        return False
    
class BasicML:
    def __init__(self):
        pass

    #TODO: Need to determine if we will "return accumulator" where the accumulator is required
        # and assign that returned value to the int in CPU, or if we will use a list
        # (which is auto-passed by reference).

    
    def read(self, memory, operand):
        '''
        Reads a word from the keyboard into a location in memory specified by the operand.
        '''
        read_input = input("Enter a 4-digit word: ") # Receives input from user.
        memory[operand] = read_input # Stores input in memory.
        

    def write(self, memory, operand):
        '''
        Writes a word from a location in memory specified by the operand to screen.
        '''
        output = memory[operand] # Pulls the word from memory.
        print(output) # Prints the word as the output.


    def load(self, memory, operand, accumulator): #TODO: Accumulator fix
        '''
        Loads a word from a location in memory specified by the operand into the accumulator.
        '''
        loadValue = memory.mainMemory[operand] # Loads the value from memory.
        accumulator = loadValue # Assigns the loaded value to the accumulator.


    def store(self, memory, operand, accumulator): #TODO: Accumulator fix
        '''
        Store a word from the accumulator into a location in memory specified by the operand.
        '''
        memory[operand] = accumulator_value


    def add(self, memory, operand, accumulator): #TODO: Accumulator fix
        '''
        Adds a word from a location in memory specified by the operand to the word in the accumulator
        (leaves the result in the accumulator).
        '''
        return accumulator + memory[operand]


    def subtract(self, memory, operand, accumulator): #TODO: Accumulator fix
        '''
        Subtracts a word from a location in memory specified by the operand from the word in the accumulator.
        Returns the result.
        '''
        return accumulator - memory[operand]

    
    def divide(self, memory, operand, accumulator): #TODO: Accumulator fix
        '''
        Divides the word in the accumulator by a word from a location specified by the operand in memory.
        Returns the result.
        '''
        if memory[operand] == 0:
            print("Error: Dvision by zero.")
        else:
            return accumulator / memory[operand]

    def multiply(self, memory, operand, accumulator): #TODO: Accumulator fix
        '''
        Multiplies a word from a location in memory specified by the operand to the word in the accumulator.
        Returns the result.
        '''
        return accumulator * memory[operand]

    def branch(self, memory, operand): #TODO: Needs ability to set location/register.
        '''
        Branches to a location in memory specified by the operand.
        '''
        branch_location = operand


    def branchNeg(self, memory, operand, accumulator): #TODO: Accumulator fix
                                                 #TODO: Needs ability to set location/register.
        '''
        Branches to a location in memory specified by the operand if the accumulator is negative.
        '''
        if accumulator < 0:
            branch_location = operand


    def branchZero(self, memory, operand, accumulator): #TODO: Accumulator fix
                                                  #TODO: Needs ability to set location/register.
        '''
        Branches to a location in memory specified by the operand if the accumulator is zero.
        '''
        if accumulator == 0:
            branch_location = operand


    def halt(self, running): #TODO: Needs ability to set "running" to False
        '''
        Pauses the program.
        '''
        running = False
        return running
    
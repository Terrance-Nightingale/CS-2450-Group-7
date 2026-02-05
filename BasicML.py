class BasicML:
    def __init__(self):
        pass

    #TODO: Need to determine if we will "return accumulator" where the accumulator is required
        # and assign that returned value to the int in CPU, or if we will use a list
        # (which is auto-passed by reference).

    
    def read(memory, operand):
        '''
        Reads a word from the keyboard into a location in memory specified by the operand.
        '''
        read_input = input("Enter a 4-digit word: ") # Receives input from user.
        memory[operand] = read_input # Stores input in memory.
        

    def write(memory, operand):
        '''
        Writes a word from a location in memory specified by the operand to screen.
        '''
        output = memory[operand] # Pulls the word from memory.
        print(output) # Prints the word as the output.


    def load(memory, operand, accumulator): #TODO: Accumulator fix
        '''
        Loads a word from a location in memory specified by the operand into the accumulator.
        '''
        load_value = memory[operand] # Loads the value from memory.
        accumulator = load_value # Assigns the loaded value to the accumulator.


    def store(memory, operand, accumulator_value):
        '''
        Store a word from the accumulator into a location in memory specified by the operand.
        '''
        memory[operand] = accumulator_value


    def add(memory, operand, accumulator):
        '''
        Adds a word from a location in memory specified by the operand to the word in the accumulator
        (leaves the result in the accumulator).
        '''
        return accumulator + memory[operand]


    def subtract(memory, operand, accumulator):
        '''
        Subtracts a word from a location in memory specified by the operand from the word in the accumulator.
        Returns the result.
        '''
        return accumulator - memory[operand]

    
    def divide(memory, operand, accumulator):
        '''
        Divides the word in the accumulator by a word from a location specified by the operand in memory.
        Returns the result.
        '''
        return accumulator / memory[operand]

    def multiply(memory, operand, accumulator):
        '''
        Multiplies a word from a location in memory specified by the operand to the word in the accumulator.
        Returns the result.
        '''
        return accumulator * memory[operand]

    def branch(memory, operand): #TODO: Needs ability to set location/register.
        '''
        Branches to a location in memory specified by the operand.
        '''
        branch_location = operand


    def branchNeg(memory, operand, accumulator): #TODO: Needs ability to set location/register.
        '''
        Branches to a location in memory specified by the operand if the accumulator is negative.
        '''
        if accumulator < 0:
            branch_location = operand


    def branchZero(memory, operand, accumulator): #TODO: Needs ability to set location/register.
        '''
        Branches to a location in memory specified by the operand if the accumulator is zero.
        '''
        if accumulator == 0:
            branch_location = operand


    def halt(running): #TODO: Needs ability to set "running" to False
        '''
        Pauses the program.
        '''
        running = False
        return running
    
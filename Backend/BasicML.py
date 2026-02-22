from tkinter import simpledialog

class BasicML:
    def __init__(self, inputPanel=None, inputInfoPanel=None):
        self.inputPanel = inputPanel
        self.inputInfoPanel = inputInfoPanel
        self.read_value = None
        self.errorMessage = ""
    
    def read(self, memory, operand):
        if self.inputPanel:
            read_input = simpledialog.askstring("Input", "Enter a word")
            try:
                inputInt = int(read_input)
            except ValueError:
                self.errorMessage = "Invalid input: not an integer"
                return

            if -9999 <= inputInt <= 9999:
                memory[operand] = inputInt
                #self.inputPanel.word_entry.delete(0, tk.END)  # clear entry

                if self.inputInfoPanel:
                    self.inputInfoPanel.update_prev_inputs(f"READ {inputInt}")
            else:
                self.errorMessage = "Number must be between -9999 and 9999"
        
        

    def write(self, memory, operand):
        '''
        Writes a word from a location in memory specified by the operand to screen.
        '''
        output = memory[operand]
        if self.inputInfoPanel:
            self.inputInfoPanel.update_prev_inputs(f"WRITE {output}")


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
        result = accumulator + memory[operand]
        if result > 9999 or result < -9999:
            self.errorMessage = "Accumulator overflow!"
            return None
        return result


    def subtract(self, memory, operand, accumulator):
        '''
        Subtracts a word from a location in memory specified by the operand from the word in the accumulator
        and returns the result.
        '''
        result = accumulator - memory[operand]
        if result > 9999 or result < -9999:
            self.errorMessage = "Accumulator overflow!"
            return None
        return result

    
    def divide(self, memory, operand, accumulator):
        '''
        Divides the word in the accumulator by a word from a location specified by the operand in memory.
        Returns the result.
        '''
        if memory[operand] == 0:
            self.errorMessage = "Error: Division by zero."
        else:
            return accumulator // memory[operand]

    def multiply(self, memory, operand, accumulator):
        '''
        Multiplies a word from a location in memory specified by the operand to the word in the accumulator.
        Returns the result.
        '''
        result = accumulator * memory[operand]
        if result > 9999 or result < -9999:
            self.errorMessage = "Accumulator overflow!"
            return None
        return result


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
    
from tkinter import simpledialog

class BasicML:
    def __init__(self, input_info_panel=None):
        self.input_info_panel = input_info_panel
        self.read_value = None
        self.error_message = ""
    
    def read(self, memory, operand, user_input): # Last edited by: Josh 3/11/2026
            '''Reads a word from the keyboard and stores it into a location specified by the operand.'''
            memory[operand] = user_input
            # self.inputInfoPanel.update_prev_inputs(f"READ {userInput}")
            # self.inputPanel.word_entry.delete(0, tk.END)  # clear entry
        
    def write(self, memory, operand):
        '''
        Writes a word from a location in memory specified by the operand to screen.
        '''
        # TODO: Output portion should be handled by GUI
        output = memory[operand]
        if self.input_info_panel:
            self.input_info_panel.update_prev_inputs(f"WRITE {output}")


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
            self.error_message = "Accumulator overflow!"
            return 0

        return result


    def subtract(self, memory, operand, accumulator):
        '''
        Subtracts a word from a location in memory specified by the operand from the word in the accumulator
        and returns the result.
        '''
        result = accumulator - memory[operand]

        if result > 9999 or result < -9999:
            self.error_message = "Accumulator overflow!"
            return 0

        return result

    
    def divide(self, memory, operand, accumulator):
        '''
        Divides the word in the accumulator by a word from a location specified by the operand in memory.
        Returns the result.
        '''
        result = accumulator // memory[operand]
        if memory[operand] == 0:
            self.error_message = "Error: Division by zero."
        if result > 9999 or result < -9999:
            self.error_message = "Accumulator overflow!"
            return 0

        return result

    def multiply(self, memory, operand, accumulator):
        '''
        Multiplies a word from a location in memory specified by the operand to the word in the accumulator.
        Returns the result.
        '''
        result = accumulator * memory[operand]

        if result > 9999 or result < -9999:
            self.error_message = "Accumulator overflow!"
            return 0

        return result


    def branch(self, operand):
        '''
        Returns the location to be branched to in memory specified by the operand.
        '''
        return operand


    def branch_neg(self, operand, instruction_counter, accumulator):
        '''
        Returns the location to be branched to in memory specified by the operand if the accumulator is negative.
        '''
        if accumulator < 0:
            return operand
        else:
            return instruction_counter


    def branch_zero(self, operand, instruction_counter, accumulator):
        '''
        Returns the location to be branched to in memory specified by the operand if the accumulator is zero.
        '''
        if accumulator == 0:
            return operand
        else:
            return instruction_counter


    def halt(self):
        '''
        Pauses the program.
        '''
        return False
    
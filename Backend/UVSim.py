from Backend.UserProgram import UserProgram
from Backend.Memory import Memory
from Backend.cpu import CPU
from Backend.BasicML import BasicML
from tkinter import filedialog

class UVSim:
    def __init__(self, input_info_panel = None):
        self.memory = Memory()
        self.cpu = CPU(self.memory)
        self.user_program = UserProgram()
        self.cpu.basicml = BasicML(input_info_panel)
        self.format = "4digit"

    def check_program_format(self, values):
        '''
        Checks that a program isn't using 4 and 6 digit instructions at the same time
        '''
        four_digit = False
        six_digit = False
 
        for value in values:
            if value is None or value == 0:
                continue
            abs_val = abs(value)
            if abs_val <= 9999:
                four_digit = True
            elif abs_val <= 99999:
                six_digit = True
                self.format = "6digit"
 
        if four_digit and six_digit:
            return ("Program cannot contain 4 and 6 digit words, please use one or the other")
        return None
        
    def load_program(self, user_program):
        '''
        Loads the user's program into memory.
        '''
        for i, word in enumerate(user_program.program):
            if i >= 250:
                #This error will trigger the error_message check in InputPanel.py
                return "File is longer than 250 words. Only 250 Loaded"
            self.memory.main_memory()[i] = int(word)

    def run_program(self):
        '''
        Decodes and runs the user's program.
        '''
        if not self.cpu.running:
            format_error = self.check_program_format(self.memory.main_memory())
            if format_error:
                self.cpu.error_message = format_error
                return
            self.cpu.soft_reset()

        try:
            while self.cpu.fetch():
                self.cpu.decode()
                # Check if this is a READ instruction (OP code "10")
                if self.cpu.opcode == 10:
                    return  # Pause and exit loop, GUI will handle READ
                self.cpu.execute()
        except ValueError as e: # Unlocks Control Panel even if ValueError is thrown.
            # Sets the CPU error_message to the thrown ValueError.
            self.cpu.error_message = f"{e} (line: {self.cpu.instruction_counter - 1}) (instruction: {self.cpu.instruction_register})"
            self.cpu.running = False

        # If no HALT command, will set running to False (to unlock Control Panel again).
        self.cpu.running = False

    def reset_program(self):    
        '''
        Excecute's the CPU's reset function.
        '''    
        self.cpu.reset()

        mem = self.memory.main_memory()
        for i in range(len(mem)):
            mem[i] = 0

    def save_program(self):
        file_path = filedialog.asksaveasfilename(
            title="Save File As",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
         )
        
        # Return None if the user cancelled the Save.
        if not file_path:
            return None
        
        self.check_program_format(self.memory.main_memory())
        current_memory = self.memory.main_memory()
        with open(file_path, "w", encoding="utf-8") as file:
            for value in current_memory:
                if value == None:
                    pass
                elif self.format == "6digit" and value != 0:
                    sign = "-" if value < 0 else ""
                    file.write(f"{sign}0{abs(value)}\n")
                else:
                    file.write(f"{value}\n")
        return file_path

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

    def load_program(self, user_program):
        '''
        Loads the user's program into memory.
        '''
<<<<<<< Updated upstream
        for i, word in enumerate(user_program.program):
            self.memory.main_memory()[i] = int(word)
=======
        #for i, word in enumerate(user_program.program):
        #    self.memory.main_memory()[i] = int(word)
        for word in user_program.program:
            self.memory.main_memory().append(int(word))
        self.memory.just_loaded = True
>>>>>>> Stashed changes

    def run_program(self):
        '''
        Decodes and runs the user's program.
        '''
        while self.cpu.fetch():
                self.cpu.decode()

                # Check if this is a READ instruction
                if self.cpu.opcode == 10:
                    return  # Pause and exit loop, GUI will handle READ
                self.cpu.execute()

    def reset_program(self):    
        '''
        Excecute's the CPU's reset function.
        '''    
        self.cpu.reset()

    def save_program(self):
         file_path = filedialog.asksaveasfilename(
              title="Save File As",
              defaultextension=".txt",
              filetypes=[("Text Files", "*.txt")]
         )
         current_memory = self.memory.main_memory()
         with open(file_path, "w", encoding="utf-8") as file:
              for value in current_memory:
                   if value == 0:
                        pass
                   else:
                        file.write(f"{value}\n")

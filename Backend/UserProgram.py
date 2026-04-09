class UserProgram():
    def __init__(self):
        self.program_size = 0
        self.program = []
        self.error_message = ""

    def input_program(self, filepath):
        try: 
            with open(filepath, "r") as f:
                for line in f:
                    word = line.strip()
                    if word == "-99999":
                        break
                    self.program.append(word)
        except FileNotFoundError:
            self.error_message = "File not found."


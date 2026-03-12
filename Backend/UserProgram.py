class UserProgram():
    def __init__(self):
        self.program_size = 0
        self.program = []
        self.error_message = ""

    '''    def inputProgram(self):
            while True:
                while True:
                    try:
                        programInput = int(input("Please input a word between -9999 and +9999, input -99999 to stop: "))
                        break
                    except ValueError:
                        print("Invalid input")
                if programInput == -99999:
                    print("Program entered")
                    break
                if programInput > 9999 or programInput < -9999:
                    print("Invalid input")
                else:
                    if self.programSize < 100:
                        self.program.append(programInput)
                        self.programSize += 1
                        print("Word input successfully")
                    else:
                        print("Maximum program size reached, please enter -99999 to finish inputting your program: ")
    '''
    def inputProgram(self, filepath):
        try: 
            with open(filepath, "r") as f:
                for line in f:
                    word = line.strip()
                    if word == "-99999":
                        break
                    self.program.append(word)
        except FileNotFoundError:
            self.error_message = "File not found."


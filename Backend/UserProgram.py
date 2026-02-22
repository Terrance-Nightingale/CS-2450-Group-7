class UserProgram():
    def __init__(self):
        self.programSize = 0
        self.program = []

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
    def inputProgram(self, file_from_gui=None):
        if file_from_gui:
            file_path = file_from_gui
        else:
            print("Please enter the file path for the program you'd like to run: ")
        
        with open(file_path, "r") as file:
            for word in file:
                if word == "-99999":
                    break
                self.program.append(word.rstrip("\n"))

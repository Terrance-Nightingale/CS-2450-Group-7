class AppController:
    def __init__(self, app, user_program):
        self.app = app
        self.program = user_program
        self.busy = False

    def inputProgram(self, file_path):
        self.program.inputProgram(file_from_gui=file_path)

    def loadProgram(self):
        self.app.loadProgram(self.program)

    def read_word_from_gui(self, word):
        try:
            inputInt = int(word)
            if(-9999 <= inputInt <= 9999):
                self.app.cpu.basicml.new_word = inputInt
        except:
            print("Number must be between -9999 and 9999.")

    def runProgram(self):
        '''
        Calls the app's runProgram method.
        '''
        if not self.busy:
            self.busy = True
            self.app.runProgram()
            self.busy = False
        

    def resetProgram(self):
        '''
        Calls the app's resetProgram method.
        '''
        if not self.busy:
            self.app.resetProgram()

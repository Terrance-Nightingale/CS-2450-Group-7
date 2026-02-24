class AppController:
    def __init__(self, app):
        self.app = app
        self.busy = False

    def runProgram(self):
        '''
        Calls the app's runProgram method.
        '''
        if not self.busy:
            self.busy = True
            self.app.loadProgram(self.app.userProgram)
            self.app.runProgram()
            self.busy = False
        

    def resetProgram(self):
        '''
        Calls the app's resetProgram method.
        '''
        if not self.busy:
            self.app.resetProgram()

class AppController:
    def __init__(self, app):
        self.app = app
        self.busy = False

    def runProgram(self):
        if not self.busy:
            self.busy = True
            self.app.runProgram()
            self.busy = False
        

    def resetProgram(self):
        if not self.busy:
            self.app.resetProgram()

import tkinter as tk

class AppController:
    def __init__(self, app):
        self.app = app
        self.busy = False

    '''
    Calls the app's runProgram method.
    '''
    def runProgram(self):
        if not self.busy:
            self.busy = True
            self.app.runProgram()
            self.busy = False
        
    '''
    Calls the app's resetProgram method.
    '''
    def resetProgram(self):
       
        if not self.busy:
            self.app.resetProgram()

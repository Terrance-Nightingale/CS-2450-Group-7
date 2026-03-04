class AppController:
    def __init__(self, app, gui_component=None):
        self.app = app
        self.gui_component = gui_component
        self.busy = False

    @property
    def guiComponent(self):
        return self.gui_component

    @guiComponent.setter
    def guiComponent(self, a):
        self.gui_component = a
    
    def runProgram(self):
        '''Calls the app's runProgram method.'''
        if not self.busy:
            self.busy = True
            self.app.runProgram()
            self.app.loadProgram(self.app.userProgram)
            self.busy = False
        
    def resetProgram(self):
        '''Calls the app's resetProgram method.'''
        if not self.busy:
            self.app.resetProgram()

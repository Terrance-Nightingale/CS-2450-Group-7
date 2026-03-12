class AppController:
    def __init__(self, app, root, gui_component=None):
        self.app = app
        self.root = root
        self.gui_component = gui_component
        self.busy = False

    # region Getter/Setters
    @property
    def guiComponent(self):
        return self.gui_component

    @guiComponent.setter
    def guiComponent(self, a):
        self.gui_component = a
    
    @property
    def rootUI(self):
        return self.root
    
    @rootUI.setter
    def rootUI(self, a):
        self.root = a
    # endregion
    
    # region Program Methods
    def runProgram(self): # Last edited by: Josh 3/11/2026
        '''Calls the app's runProgram method.'''
        if not self.busy:
            self.busy = True
            self.gui_component.setButtonState('RUN', 'disabled')  # Gray out RUN button
            self.app.loadProgram(self.app.userProgram)
            self.app.runProgram()

            # If current opcode is READ, creates a popup that prompts the user for their input.
                # Will continue the program from where it left off after receiving/processing user input.
            if self.app.cpu.opcode == 10:
                self.root.create_input_popup()
    
    def continueProgram(self, userInput):
        '''Executes Read command, then continues program execution.'''
        # Pass input to READ, then continue execution
        self.app.cpu.basicml.read(self.app.memory.mainMemory, self.app.cpu.operand, userInput)
        self.app.runProgram() # Resume program from last opcode

        # Check for READ opcode again
        if self.app.cpu.opcode == 10:
            self.root.create_input_popup()
        else:
            # Re-enable only when fully done
            self.busy = False
            self.gui_component.setButtonState('RUN', 'normal')
        
    def resetProgram(self):
        '''Calls the app's resetProgram method.'''
        if not self.busy:
            self.app.resetProgram()
    # endregion

    def validate_user_input(self, popup_box, user_input): # Last edited by: Josh 3/11/2026
        '''
        Validates the user's input and throws an error if validation conditions are not met.
        '''
        # If user input is not an integer, display "Not an integer" error message.
        try:
            inputInt = int(user_input)
        except ValueError:
            error_message = "Invalid input: not an integer."
            self.root.create_error_popup(error_message)
            return
    
        # If user input not in valid range, display "invalid range" error message.
        if not -9999 <= int(user_input) <= 9999:
            error_message = "Number must be between -9999 and 9999."
            self.root.create_error_popup(error_message)
            return
    
        popup_box.destroy() # Destroys popup box.
        self.continueProgram(inputInt) # Continues the program from where it left off.
    
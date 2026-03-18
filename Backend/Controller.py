class AppController:
    def __init__(self, app, root, gui_component=None):
        self.app = app
        self.root = root
        self._gui_component = gui_component
        self.busy = False

    # region Getter/Setters
    @property
    def gui_component(self):
        return self._gui_component

    @gui_component.setter
    def gui_component(self, a):
        self._gui_component = a
    
    @property
    def root_ui(self):
        return self.root
    
    @root_ui.setter
    def root_ui(self, a):
        self.root = a
    # endregion
    
    # region Program Methods
    def run_program(self): # Last edited by: Josh 3/11/2026
        '''Calls the app's runProgram method.'''
        if not self.busy:
            self.busy = True
            self.gui_component.set_button_state('RUN', 'disabled') # Gray out Control buttons
            self.gui_component.set_button_state('RESET', 'disabled')
            self.app.load_program(self.app.user_program)
            self.app.run_program()

            # If current opcode is READ, creates a popup that prompts the user for their input.
                # Will continue the program from where it left off after receiving/processing user input.
            if self.app.cpu.opcode == 10:
                self.root.create_input_popup()
    
    def continue_program(self, user_input):
        '''Executes Read command, then continues program execution.'''
        # Pass input to READ, then continue execution
        self.app.cpu.basicml.read(self.app.memory.main_memory(), self.app.cpu.operand, user_input)
        self.app.run_program() # Resume program from last opcode

        # Check for READ opcode again
        if self.app.cpu.opcode == 10:
            self.root.create_input_popup()
        else:
            # Re-enable only when fully done
            self.busy = False
            self.gui_component.set_button_state('RUN', 'normal')
            self.gui_component.set_button_state('RESET', 'normal')
        
    def reset_program(self):
        '''Calls the app's resetProgram method.'''
        if not self.busy:
            self.app.reset_program()
    # endregion

    def save_program(self):
        if not self.busy:
            self.app.save_program()
            

    def validate_user_input(self, popup_box, user_input): # Last edited by: Josh 3/11/2026
        '''
        Validates the user's input and throws an error if validation conditions are not met.
        '''
        # If user input is not an integer, display "Not an integer" error message.
        try:
            input_int = int(user_input)
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
        self.continue_program(input_int) # Continues the program from where it left off.
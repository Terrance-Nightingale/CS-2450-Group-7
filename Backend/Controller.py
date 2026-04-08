class AppController:
    def __init__(self, sim, root, gui_component=None):
        self.sim = sim
        self.root = root
        self._gui_component = gui_component
        self.busy = False
        self.console = None

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
    def run_program(self):
        if not self.busy:
            self.disable_control_buttons()

            result = self.sim.run_program()

            if result and self.console:
                self.console.update_prev_outputs(result)

            self.handle_program_state()
    
    def continue_program(self, user_input):
        self.sim.cpu.basicml.read(self.sim.memory.main_memory(), self.sim.cpu.operand, user_input)

        result = self.sim.run_program()

        if result and self.console:
            self.console.update_prev_outputs(result)

        self.handle_program_state()

    def load_program(self, program):
        result = self.sim.load_program(program)

        if result and self.console:
            self.console.update_prev_outputs(result)
        elif self.console:
            self.console.update_prev_outputs("Program loaded successfully")

    def handle_program_state(self):
                # Check for READ opcode again
        if self.sim.cpu.opcode == 10:
            self.root.create_input_popup()
        # Re-enable only when fully done
        elif not self.sim.cpu.running:
            self.enable_control_buttons()
        
    def reset_program(self):
        '''Calls the app's resetProgram method.'''
        if not self.busy:
            self.sim.reset_program()
    
    def save_program(self):
        if not self.busy:
            self.sim.save_program()
    # endregion

    def enable_control_buttons(self): # Last edited by: Josh 3/18/2026
        '''Enables the Control buttons.'''
        self.busy = False
        self.gui_component.set_button_state('RUN', 'normal')
        self.gui_component.set_button_state('RESET', 'normal')
        self.gui_component.set_button_state('SAVE', 'normal')
    
    def disable_control_buttons(self): # Last edited by: Josh 3/18/2026
        '''Disables the Control buttons.'''
        self.busy = True
        self.gui_component.set_button_state('RUN', 'disabled')
        self.gui_component.set_button_state('RESET', 'disabled')
        self.gui_component.set_button_state('SAVE', 'disabled')
            
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
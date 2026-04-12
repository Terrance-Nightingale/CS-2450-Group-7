class AppController:
    def __init__(self, sim, root, gui_component=None):
        self.sim = sim
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
    def run_program(self, uvsim=None): # Last edited by: Josh 3/18/2026
        '''Calls the app's runProgram method. Runs the program as it currently exists in memory.'''
        sim = uvsim or self.sim
        if not self.busy:
            self.disable_control_buttons()
            sim.run_program()
            self.check_for_error_or_read(sim)

    def continue_program(self, user_input, uvsim=None):
        '''Executes Read command, then continues program execution.'''
        sim = uvsim or self.sim

        # Pass input to READ, then continue execution
        sim.cpu.basicml.read(sim.memory.main_memory(), sim.cpu.operand, user_input)
        sim.run_program() # Resume program from last opcode
        self.check_for_error_or_read(sim)

    def check_for_error_or_read(self, uvsim):
        sim = uvsim or self.sim
        # If an error was thrown, display the error in a popup.
        if sim.cpu.error_message:
            self.enable_control_buttons()
            self.root.create_error_popup(sim.cpu.error_message)
            sim.cpu.error_message = ""
        # Re-enable only when fully done
        elif not sim.cpu.running:
            self.enable_control_buttons()
        # Check for READ opcode again
        elif sim.cpu.opcode == 10:
            self.root.create_input_popup()

    def reset_program(self, uvsim=None):
        '''Calls the app's resetProgram method.'''
        sim = uvsim or self.sim
        if not self.busy:
            sim.reset_program()
    
    def save_program(self, uvsim=None):
        '''
        Saves the user's program to a *.txt file.
        Renames the current tab to the filename.
        '''
        sim = uvsim or self.sim
        if not self.busy:
            file_name = sim.save_program()
            if file_name:
                # Calls the AppUI's TabContainer to get the currently selected tab
                # and change the tab's name to the filename (i.e. "MyProgram.txt")
                tab = self.root.tabs_container.get_current_tab()
                self.root.tabs_container.set_tab_name(tab, file_name)
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
            
    def validate_user_input(self, popup_box, user_input, uvsim=None): # Last edited by: Josh 3/11/2026
        '''
        Validates the user's input and throws an error if validation conditions are not met.
        '''
        sim = uvsim or self.sim

        # If user input is not an integer, display "Not an integer" error message.
        try:
            input_int = int(user_input)
        except ValueError:
            self.root.create_error_popup("Invalid input: not an integer.")
            return
    
        # If user input not in valid range, display "invalid range" error message.
        if not -9999 <= int(user_input) <= 9999:
            self.root.create_error_popup("Number must be between -9999 and 9999.")
            return
    
        popup_box.destroy() # Destroys popup box.
        self.continue_program(input_int, sim) # Continues the program from where it left off.

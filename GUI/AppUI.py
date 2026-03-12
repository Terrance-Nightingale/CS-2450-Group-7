import tkinter as tk
from GUI.TitlePanel import TitlePanel
from GUI.ContentPanel import ContentPanel
from GUI.CPUStatePanel import CPUStatePanel
from GUI.InputPanel import InputPanel
from GUI.InputInfoPanel import InputInfoPanel
from GUI.Memorypanel import MemoryPanel
from GUI.ErrorPanel import ErrorPanel
from GUI.ControlPanel import ControlPanel
from GUI.MenuBar import MenuBar

class AppUI:
    def __init__(self, window, controller, uvsim):
        self.uvsim = uvsim
        self.window = window
        self.window.title("UVSim")
        self.window.configure(bg = "darkgrey")
        self.panels = {}
        self.error_popup = None

        self.controller = controller

        self.sub_panel_names = ["Input", "CPU State", "Error Reports", "Input Info", "Memory", "Controls"]

        #self.titlePanel = TitlePanel(window)

        self.container = tk.Frame(window)
        self.container.pack(expand = True, fill = "both")

        for i in range(2):
            self.container.rowconfigure(i, weight = 1)

        for i in range(3):
            self.container.columnconfigure(i, weight = 1)

        self.create_grid_panels()

        menu = MenuBar(self.window, self)
        menu.create_file_menu()
        menu.create_theme_menu()
        menu.create_help_menu()

    def create_grid_panels(self):
        for index, name in enumerate(self.sub_panel_names):
            row = index // 3
            col = index % 3
            buttons = None

            if name == "Controls":
                buttons = [
                    {
                        'name': 'RUN',
                        'command': self.controller.run_program
                    },

                    {
                        'name': 'RESET',
                        'command': self.controller.reset_program
                    }
                ]

            panel = ContentPanel(self.container, name, buttons)
            panel.grid(row, col)

            self.panels[name] = panel.sub_panel
            
            if name == "CPU State":
                panel.sub_panel.status_label.destroy()
                self.cup_state_panel = CPUStatePanel(panel.sub_panel.content_panel, self.uvsim.cpu)
        
            if name == "Controls":
                panel.sub_panel.status_label.destroy()
                self.control_panel = ControlPanel(panel.sub_panel.content_panel, buttons)
                self.controller.gui_component = self.control_panel # Allow the controller access to the Controls panel gui component.

            if name == "Input":
                panel.sub_panel.status_label.destroy()
                InputPanel(panel.sub_panel.content_panel, self.uvsim)

            if name == "Input Info":
                panel.sub_panel.status_label.destroy()
                InputInfoPanel(panel.sub_panel.content_panel, self.uvsim)

            if name == "Memory":
                panel.sub_panel.status_label.destroy()
                MemoryPanel(panel.sub_panel.content_panel, self.uvsim.cpu)

            if name == "Error Reports":
                panel.sub_panel.status_label.destroy()
    

    def create_input_popup(self): # Last edited by: Josh 3/11/2026
        '''
        Creates a popup window with an input box to receive user input.
        '''
        read_popup = tk.Toplevel(self.window) # Create popup window.
        read_popup.title('User Input Required') # Set popup title

        width = 380
        height = 80
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)

        read_popup.geometry(f'{width}x{height}+{x}+{y}') # Set width, height, and location to center of window.
        read_popup.resizable(False, False) # Prevent resizing of popup window.
        read_popup.protocol("WM_DELETE_WINDOW", lambda: (read_popup.bell(), read_popup.focus_force())) # Disables 'X' button to close out of popup.
        read_popup.attributes('-topmost', True) # Ensure that popup appears on top of main window.

        tk.Label(read_popup, text='Input: ').grid(column=0, row=0, pady=5, padx=5) # Add input box label to row 0.
        input_box = tk.Entry(read_popup, width=40) # Add input box after Label.
        input_box.grid(column=1, row=0, pady=5, padx=5) # Set orientation to left.
        input_box.focus_set() # Auto-focus input box when popup opens.

        # Create submit button and set orientation to left. Also allow the user to press 'Enter' to submit.
        input_box.bind('<Return>', lambda event: self.controller.validate_user_input(read_popup, input_box.get()))
        submit_button = tk.Button(read_popup, text='Submit', command=lambda: self.controller.validate_user_input(read_popup, input_box.get()))
        submit_button.grid(column=2, row=0, pady=5, padx=5)
    

    def create_error_popup(self, error_message):
        '''Creates a popup that displays an error if user input was invalid.'''
        # Check if an error window exists first. If it does, destroy it before creating a new one.
        if self.error_popup and self.error_popup.winfo_exists():
            self.error_popup.destroy()
        error_popup = tk.Toplevel(self.window) # Create error window.
        error_popup.title('Error') # Set popup title

        width = 300
        height = 50
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)

        error_popup.geometry(f'+{x}+{y}') # Set width, height, and location to center of window.
        error_popup.attributes('-topmost', True) # Ensure that popup appears on top of main window.
        tk.Label(error_popup, text=f'{error_message}', padx=20, pady=20).grid(column=0, row=0, pady=5, padx=5) # Add input box label to row 0.

        error_popup.bell() # Play error sound effect.
                

    '''
    This will create an exit prompt upon clicking the "Exit" option in the File menu selection
    '''
    def exit_prompt(self): # Last edited by: Josh 3/11/2026
        self.window.attributes('-topmost', True) # Set window priority to appear above all other windows.
        are_you_sure = tk.messagebox.askyesno("Exiting UVSim", "Are you sure you want to exit?")

        if are_you_sure:
            self.window.destroy()
        else:
            self.window.attributes('-topmost', False) # Reset window priority to appear behind popups.

            

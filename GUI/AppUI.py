import tkinter as tk
from GUI.ContentPanel import ContentPanel
from GUI.CPUStatePanel import CPUStatePanel
from GUI.InputPanel import InputPanel
from GUI.ConsolePanel import ConsolePanel
from GUI.Memorypanel import MemoryPanel
from GUI.ControlPanel import ControlPanel
from GUI.MenuBar import MenuBar
from GUI.TabContainer import TabContainer

class AppUI:
    def __init__(self, window, controller, uvsim):
        self.uvsim = uvsim
        self.window = window
        self.window.title("UVSim")
        self.window.configure(bg = "darkgrey")
        self.panels = {}
        self.error_popup = None
        self.menu = None
        self.controller = controller
        self.tabs_container = None

        self.sub_panel_names = ["Input", "CPU State", "Console", "Controls", "Memory"]

        # Pass create_grid_panels as the callback for the TabContainer so each new tab builds its own panel grid.
        self.tabs_container = TabContainer(
            self.window,
            self.create_grid_panels,
            on_tab_switch=self._on_tab_switched
        )

        # Ensures that initial tab exists.
        self.tabs_container.register_initial_tab()

        # Initialize the MenuBar
        self.menu = MenuBar(self.window, self)
        self.menu.create_file_menu()
        self.menu.create_theme_menu()
        self.menu.create_help_menu()


    def _on_tab_switched(self, tab):
        '''Updates active references (CPU, Memory, etc) to the current tab's when the user switches tabs.'''
        components = self.tabs_container.get_tab_components(tab)

        # Return if no components were found.
        if not components:
            print("No components found for tab.")
            return

        # Update all AppUI components to reference the current tab's components.
        self.panels = components["panels"]
        self.cpu_state_panel = components["cpu_state_panel"]
        self.console = components["console"]
        self.control_panel = components["control_panel"]
        self.uvsim = components["uvsim"]
        self.controller.gui_component = self.control_panel
        self.controller.sim = self.uvsim
        self.uvsim.cpu.basicml.console_panel = self.console


    def create_grid_panels(self, parent):
        '''Creates the main GUI panels for the program.'''
        container = tk.Frame(parent)
        container.pack(expand=True, fill="both")

        for i in range(2):
            container.rowconfigure(i, weight=1)
        for i in range(3):
            container.columnconfigure(i, weight=1)

        # Each tab gets its own UVSim instance
        from Backend.UVSim import UVSim
        tab_uvsim = UVSim()
        
        # Components to be added to the tab.
        tab_panels = {}
        tab_cpu_state_panel = None
        tab_control_panel = None
        tab_console = None

        for index, name in enumerate(self.sub_panel_names):
            row = index // 3
            col = index % 3
            buttons = None

            if name == "Controls":
                buttons = [
                    {'name': 'RUN', 'command': lambda sim=tab_uvsim: self.controller.run_program(sim)},
                    {'name': 'RESET', 'command': lambda sim=tab_uvsim: self.controller.reset_program(sim)},
                    {'name': 'SAVE', 'command' : lambda sim=tab_uvsim: self.controller.save_program(sim)},
                ]

            panel = ContentPanel(container, name, buttons)
            panel.grid(row, col)
            tab_panels[name] = panel.sub_panel
            
            if name == "CPU State":
                panel.sub_panel.status_label.destroy()
                tab_cpu_state_panel = CPUStatePanel(panel.sub_panel.content_panel, tab_uvsim.cpu)
        
            if name == "Controls":
                panel.sub_panel.status_label.destroy()
                tab_control_panel = ControlPanel(panel.sub_panel.content_panel, buttons)
                self.controller.gui_component = tab_control_panel # Allow the controller access to the Controls panel gui component.

            if name == "Input":
                panel.sub_panel.status_label.destroy()
                InputPanel(self.tabs_container, panel.sub_panel.content_panel, tab_uvsim)

            if name == "Console":
                panel.sub_panel.status_label.destroy()
                panel.container.grid(row = 0, column = 2, rowspan = 2, sticky = "nsew")
                tab_console = ConsolePanel(panel.sub_panel.content_panel, tab_uvsim)
                tab_uvsim.cpu.basicml.console_panel = tab_console

            if name == "Memory":
                panel.sub_panel.status_label.destroy()
                MemoryPanel(panel.sub_panel.content_panel, tab_uvsim.cpu)

        if self.tabs_container:       
            self.tabs_container.register_tab_components(parent, {
                "panels": tab_panels,
                "cpu_state_panel": tab_cpu_state_panel,
                "control_panel": tab_control_panel,
                "console": tab_console,
                "uvsim": tab_uvsim
            })

            # Make the initial components active immediately
            self._on_tab_switched(parent)

            # Apply the current theme to the new tab if menu is ready
            if self.menu:
                self.menu.apply_theme_on_new_tab(parent)
    

    def create_input_popup(self):
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
        input_box.bind('<Return>', lambda event: self.controller.validate_user_input(read_popup, input_box.get(), self.uvsim))
        submit_button = tk.Button(read_popup, text='Submit', command=lambda: self.controller.validate_user_input(read_popup, input_box.get(), self.uvsim))
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
        self.window.focus_force()
        are_you_sure = tk.messagebox.askyesno("Exiting UVSim", "Are you sure you want to exit?")

        if are_you_sure:
            self.window.destroy()
        else:
            self.window.attributes('-topmost', False) # Reset window priority to appear behind popups.

            

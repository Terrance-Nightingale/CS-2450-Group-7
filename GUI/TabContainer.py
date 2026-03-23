import tkinter as tk

class TabContainer:
    def __init__(self, parent, content_callback=None, on_tab_switch=None):
        self._content_callback = content_callback # Checks for content to put into tabs.
        self._on_tab_switch = on_tab_switch # Actions to take place on tab switch.
        self._initial_tab = None

        self.tab_components = {}  # Dict that maps each tab's specific data to the tab itself. { tab: AppUI data }
        self.tabs_container = tk.ttk.Notebook(parent) # The primary container holding all of the tab windows.
        self.tabs_container.pack(expand=True, fill="both")

        self.initialize_tab_style() # Sets the initial tab styling that all tabs will use.
        self.create_default_buttons() # Creates the TabContainer's starting buttons.

        # Bind clicks on the "+" tab to add a new tab
            # _on_tab_changed is invoked whenever the Notebook raises a <<NotebookTabChanged>> event.
        self.tabs_container.bind("<<NotebookTabChanged>>", self._on_tab_changed)
    

    def _on_tab_changed(self, event):
        '''Listens for tab changes and triggers a new tab if "+" is selected.'''
        selected = self.tabs_container.select()

        # If the selected tab was the "+" tab, create a new tab.
        if selected == str(self._plus_tab):
            self.add_new_tab("New Tab")
            return
        
        # Notify AppUI that the tab has switched
        if self._on_tab_switch:
            selected_tab = self.tabs_container.nametowidget(selected)
            self._on_tab_switch(selected_tab)


    def add_new_tab(self, name, content_callback=None):
        '''Adds a new tab before the "+" tab and selects it.'''
        callback = content_callback or self._content_callback

        new_tab = tk.Frame(self.tabs_container)
        plus_index = self.tabs_container.index(str(self._plus_tab)) # Grabs the index of the "+" tab.

        # Insert the new tab just before "+".
        self.tabs_container.insert(plus_index, new_tab, text=name)

        # Select the newly created tab.
        self.tabs_container.select(new_tab)

        # First tab defers its callback until register_initial_tab is called
        if self._initial_tab is None:
            self._initial_tab = new_tab
            return

        if callback:
            callback(new_tab)


    def _remove_current_tab(self):
        '''Removes the currently selected tab.'''
        # Grabs the currently selected tab.
        selected = self.tabs_container.select()

        # Prevents removal of the "+" tab.
        if selected == str(self._plus_tab):
            return

        # Selects the previous tab before removing the current one.
        current_index = self.tabs_container.index(selected)
        self.tabs_container.select(max(0, current_index - 1))

        selected_tab = self.tabs_container.nametowidget(selected)
        self.tab_components.pop(selected_tab, None)

        # Removes the current tab.
        self.tabs_container.forget(selected)
    
    def register_initial_tab(self):
        '''Triggers the content callback for the first tab after AppUI is fully initialized.'''
        if self._initial_tab and self._content_callback:
            self._content_callback(self._initial_tab)

    def register_tab_components(self, tab, components):
        '''Stores a tab's components after creation.'''
        self.tab_components[tab] = components


    def get_tab_components(self, tab):
        '''Returns the stored components for a given tab.'''
        return self.tab_components.get(tab)
    
    
    def set_tab_name(self, tab, filepath):
        '''Sets the name for the specified tab.'''
        filename = filepath.split("/")[-1] # Extract just the filename from the full path.
        self.main_container.tab(tab, text=filename) # Sets the tab's name to the filename.
    

    def initialize_tab_style(self):
        '''Initializes the styling that will be used by tabs.'''
        style = tk.ttk.Style()
        style.theme_use("default")

        # Styling for unselected tabs (and margins for all tabs).
        style.configure("TNotebook", tabmargins=[2, 3, 0, 0]) # Tab margins
        style.configure("TNotebook.Tab",
            padding=[5, 2], # Tab padding
            background="#b0b0b0" # bg color
        )

        # Styling for when a tab is selected.
        style.map("TNotebook.Tab",
            background=[("selected", "#ffffff")], # bg color
            focuscolor="#ffffff", # The color of the dotted lines that appear when the tab is selected
            expand=[("selected", [1, 1, 1, 0])] # Selected tab slightly expands
        )
    
    def create_default_buttons(self):
        '''Creates the default buttons that the TabContainer always starts with.'''
        # Place a "Close Current Tab" button on the far right of the tab bar.
        self._close_btn = tk.Button(
            self.tabs_container,
            text="✕ Close Current Tab",
            command=self._remove_current_tab,
            relief="flat",
            bg="#7E7B7B",
            fg="white",
            padx=6,
            pady=0
        )
        self._close_btn.place(relx=1.0, y=0, anchor="ne") # Pins to top-right corner

        # Adds two default tabs upon initialization ("New Tab", and "+").
        self._plus_tab = tk.Frame(self.tabs_container)
        self.tabs_container.add(self._plus_tab, text="+")
        self.add_new_tab("New Tab")


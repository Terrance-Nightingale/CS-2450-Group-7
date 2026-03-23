import tkinter as tk

class TabContainer:
    def __init__(self, parent, content_callback=None):
        self._content_callback = content_callback # Checks for content to put into tabs.
        self.tabs_container = tk.ttk.Notebook(parent) # The primary container holding all of the tab windows.
        self.tabs_container.pack(expand=True, fill="both")

        # Adds two default tabs upon initialization ("New Tab", and "+").
        self._plus_tab = tk.Frame(self.tabs_container)
        self.tabs_container.add(self._plus_tab, text="+")

        self.add_new_tab("New Tab")

        # Bind clicks on the "+" tab to add a new tab
            # _on_tab_changed is invoked whenever the Notebook raises a <<NotebookTabChanged>> event.
        self.tabs_container.bind("<<NotebookTabChanged>>", self._on_tab_changed)
    

    def _on_tab_changed(self, event):
        '''Listens for tab changes and triggers a new tab if "+" is selected.'''
        selected = self.tabs_container.select()

        # If the selected tab was the "+" tab, create a new tab.
        if selected == str(self._plus_tab):
            self.add_new_tab("New Tab")


    def add_new_tab(self, name, content_callback=None):
        '''Adds a new tab before the "+" tab and selects it.'''
        callback = content_callback or self._content_callback

        new_tab = tk.Frame(self.tabs_container)
        plus_index = self.tabs_container.index(str(self._plus_tab)) # Grabs the index of the "+" tab.

        # Insert the new tab just before "+".
        self.tabs_container.insert(plus_index, new_tab, text=name)

        # Select the newly created tab.
        self.tabs_container.select(new_tab)

        if callback:
            callback(new_tab)


    def remove_tab(self, tab):
        '''Removes a tab from the Notebook.'''
        self.main_container.forget(tab)
    
    
    # All tabs will have the loaded file's name (if none, defaults to "New Tab") and an "X" on the upper right
        # (this will be a button to delete the tab). When the file is saved on that tab, the tab will be renamed
        # to the file's name.
    
    def set_tab_name(self, tab, filepath):
        '''Sets the name for the specified tab.'''
        filename = filepath.split("/")[-1] # Extract just the filename from the full path.
        self.main_container.tab(tab, text=filename) # Sets the tab's name to the filename.
        

import tkinter as tk

class ControlPanel:
    def __init__(self, parent_container, buttons=None):
        self.parent_container = parent_container

        # Configure parent container so that buttons will fill container
        self.parent_container.columnconfigure(0, weight=1)
        self.parent_container.columnconfigure(1, weight=2)
        self.parent_container.columnconfigure(2, weight=1)


        # Dynamically creates rows depending on the number of buttons needed.
        if buttons:
            for index, button in enumerate(buttons):
                tk.Button(self.parent_container, command=button['command'], text=button['name'] , font = ("Arial", 16)).grid(
                    row=index, column=1, sticky="nsew", pady = 5
                )
    
    def set_button_state(self, button_name, state):
        '''Sets the button state for any buttons'''
        for widget in self.parent_container.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget('text') == button_name:
                if state == 'disabled':
                    widget.config(state=state, bg='#acb3bd')
                else:
                    widget.config(state=state, bg='#F0F0F0')


    # This setup will allow the controller to interact with the buttons and change button color/style if necessary.
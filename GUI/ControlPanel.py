import tkinter as tk

class ControlPanel:
    def __init__(self, parent_container, color_theme_id, buttons=None):
        self.parent_container = parent_container
        self.color_theme_id = color_theme_id
        self.color1 = ""
        self.color2 = ""

        self.buttons = []

        self.setColor(self.color_theme_id)

        # Configure parent container so that buttons will fill container
        self.parent_container.columnconfigure(0, weight=1)
        self.parent_container.columnconfigure(1, weight=2)
        self.parent_container.columnconfigure(2, weight=1)

        self.parent_container.rowconfigure(0, weight=1)
        # Dynamically creates rows depending on the number of buttons needed.
        if buttons:
            for index, button in enumerate(buttons):
                btn = tk.Button(self.parent_container, 
                command=button['command'], 
                text=button['name'] , 
                font = ("Segoe UI", 16, "bold")
                )
                btn.grid(
                    row=index + 1, column=1, sticky = "ew", pady = 35
                )

                self.buttons.append(btn)

        self.parent_container.rowconfigure(len(buttons) + 1, weight=1)
    
    def set_button_state(self, button_name, state):
        '''Sets the button state for any buttons'''
        self.setColor(self.color_theme_id)
        
        for button in self.buttons:
            if button.cget('text') == button_name:
                if state == 'disabled':
                    button.config(state=state, bg=self.color2)
                else:
                    button.config(state=state, bg=self.color1)

    def setColor(self, color_theme_id):
        self.color_theme_id = color_theme_id
        match(color_theme_id):
            case 0:
                self.color1 = "#2F4880"
                self.color2 = "#203156"
            case 1:
                self.color1 = "#591303"
                self.color2 = "#6E1804"
            case 2:
                self.color1 = "#106511"
                self.color2 = "#0A3E0B"
        
        for button in self.buttons:
            if button.cget('state') == 'disabled':
                button.config(bg=self.color2, fg="white")
            else:
                button.config(bg=self.color1, fg="white")


    # This setup will allow the controller to interact with the buttons and change button color/style if necessary.
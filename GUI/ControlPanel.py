import tkinter as tk

class ControlPanel:
    def __init__(self, parent_container, buttons=None):
        self.parent_container = parent_container

        # Set parent container so that ControlPanel will fill parent
        # self.parent_container.columnconfigure(0, weight=1)
        # self.parent_container.rowconfigure(1, weight=1)

        # Set ControlPanel so that buttons will fill container
        self.parent_container.columnconfigure(0, weight=1)
        self.parent_container.columnconfigure(1, weight=2)
        self.parent_container.columnconfigure(2, weight=1)


        # Dynamically creates rows depending on the number of buttons needed.
        if buttons:
            for index, button in enumerate(buttons):
                tk.Button(self.parent_container, command=button['command'], text=button['name'] , font = ("Arial", 16)).grid(
                    row=index, column=1, sticky="nsew", pady = 5
                )


    # This setup will allow the controller to interact with the buttons and change color/style if necessary.
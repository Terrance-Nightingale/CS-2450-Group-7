import tkinter as tk

# Creates the title panel that goes over the top of the window. This has a button on it to open a small user guide.

class TitlePanel:
    def __init__(self, window):
        self.titlePanel = tk.Frame(window, borderwidth = 2, relief = "solid", bg = "black", height = 80)
        self.titlePanel.pack(fill = "x", padx = 10, pady = 10)
        self.titlePanel.pack_propagate(False)

        tk.Label(self.titlePanel, text = f"UVSimulator", font = ("Arial", 16), bg = "black", fg = "white").pack(side = "left", padx = 10, pady = 10)

        # When this is pressed, it should create a new window popup with a small guide of how to use the sim.
        tk.Button(self.titlePanel, text = "UVSim Guide", font = ("Arial", 16)).pack(side = "right", padx = 10, pady = 10)
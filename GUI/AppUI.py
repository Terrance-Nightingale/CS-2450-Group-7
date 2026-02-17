import tkinter as tk
from TitlePanel import TitlePanel
from ContentPanel import ContentPanel

class AppUI:
    def __init__(self, window):
        self.window = window
        self.window.title("UVSim")
        self.window.configure(bg = "darkgrey")
        self.subPanelNames = ["Input", "CPU State", "Error Reports", "Input Info", "Memory", "Controls"]

        self.titlePanel = TitlePanel(window)

        self.container = tk.Frame(window)
        self.container.pack(expand = True, fill = "both")

        for i in range(2):
            self.container.rowconfigure(i, weight = 1)

        for i in range(3):
            self.container.columnconfigure(i, weight = 1)

        self.createGridPanels()


    # Creates a set of rows and columns to place content panels within the window.
    def createGridPanels(self):
        for index, name in enumerate(self.subPanelNames):
            row = index // 3
            col = index % 3

            buttons = None

            if name == "Controls":
                buttons = ["RUN", "RESET"]

            panel = ContentPanel(self.container, name, buttons)
            panel.grid(row, col)

# Test output. We can change the size of this window, but I am thinking about locking it to 1500x1200
if __name__ == "__main__":
    window = tk.Tk()
    window.geometry("1500x1200")
    app = AppUI(window)
    window.mainloop()

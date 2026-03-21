import tkinter as tk
from Backend.UVSim import UVSim
from Backend.Controller import AppController
from GUI.AppUI import AppUI

if __name__ == "__main__":
    window = tk.Tk()

    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()
    window.geometry(f"{width}x{height}+0+0")

    uvsim = UVSim()

    controller = AppController(uvsim, window)

    app = AppUI(window, controller, uvsim)
    uvsim.cpu.basicml.console_panel = app.console # <- This is a temporary fix for the input_info_panel.
                                                     # Should honestly be tied to a ConsoleController or something when refactored.
                                                     # Added by: Josh 3/18/2026
    controller.root = app

    #This will intercept the "x" on the window object itself and call a function within the appui class to close and destroy.
    window.protocol("WM_DELETE_WINDOW", app.exit_prompt)

    window.mainloop()


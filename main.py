import tkinter as tk
from tkinter import messagebox
from Backend.cpu import CPU
from Backend.UserProgram import UserProgram
from Backend.UVSim import UVSim
from Backend.Controller import AppController
from GUI.AppUI import AppUI

if __name__ == "__main__":
    window = tk.Tk()
    window.geometry("1500x900")

    uvsim = UVSim()

    controller = AppController(uvsim)

    app = AppUI(window, controller, uvsim)

    #This will intercept the "x" on the window object itself and call a function within the appui class to close and destroy.
    window.protocol("WM_DELETE_WINDOW", app.exitPrompt)

    window.mainloop()

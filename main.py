from Backend.cpu import CPU
from Backend.UserProgram import UserProgram
from Backend.UVSim import UVSim
from GUI.AppUI import AppUI
from Backend.Controller import AppController
import tkinter as tk

if __name__ == "__main__":
    window = tk.Tk()
    window.geometry("1500x900")

    uvsim = UVSim()

    controller = AppController(uvsim)

    app = AppUI(window, controller, uvsim)

    window.mainloop()

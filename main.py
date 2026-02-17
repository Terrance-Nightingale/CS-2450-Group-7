from Backend.cpu import CPU
from Backend.UserProgram import UserProgram
from Backend.UVSim import UVSim
from GUI.AppUI import AppUI
from Backend.Controller import AppController
import tkinter as tk

if __name__ == "__main__":
    uvsim = UVSim()
    test = UserProgram()
    controller = AppController(uvsim)

    window = tk.Tk()
    window.geometry("1500x900")
    app = AppUI(window, controller)
    
    test.inputProgram()

    uvsim.loadProgram(test)
    # uvsim.runProgram()

    window.mainloop()

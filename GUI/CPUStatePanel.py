import tkinter as tk

class CPUStatePanel:
    def __init__(self, master, cpu):
        self.cpu = cpu
        self.master = master
        self.color = "#106511"

        self.accLabel = tk.Label(self.master, text = "", font = ("Arial", 16))
        self.accLabel.pack(side = "left", padx = 10, pady = 5)
        self.icLabel = tk.Label(self.master, text = "", font = ("Arial", 16))
        self.icLabel.pack(side = "left", padx = 10, pady = 5)
        self.irLabel = tk.Label(self.master, text = "", font = ("Arial", 16))
        self.irLabel.pack(side = "left", padx = 10, pady = 5)
        self.opcodeLabel = tk.Label(self.master, text = "", font = ("Arial", 16))
        self.opcodeLabel.pack(side = "left", padx = 10, pady = 5)
        self.operandLabel = tk.Label(self.master, text = "", font = ("Arial", 16))
        self.operandLabel.pack(side = "left", padx = 10, pady = 5)
        self.update()

    def update(self):
        self.accLabel.config(bg = self.color, fg = "white", text=f"Accumulator: {self.cpu.accumulator}")
        self.icLabel.config(bg = self.color, fg = "white",text=f"Instruction Counter: {self.cpu.instructionCounter}")
        self.irLabel.config(bg = self.color, fg = "white",text=f"Instruction Register: {self.cpu.instructionRegister}")
        self.opcodeLabel.config(bg = self.color, fg = "white",text=f"Opcode: {self.cpu.opcode}")
        self.operandLabel.config(bg = self.color, fg = "white",text=f"Operand: {self.cpu.operand}")
        self.master.after(100, self.update)

    def setColor(self, newColor):
        self.color = newColor
        self.update()
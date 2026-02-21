import tkinter as tk

class CPUStatePanel:
    def __init__(self, master, cpu):
        self.cpu = cpu
        self.master = master
        self.accLabel = tk.Label(self.master, text = "", bg = "darkgrey", font = ("Arial", 16))
        self.accLabel.pack(padx = 10, pady = 5)
        self.icLabel = tk.Label(self.master, text = "", bg = "darkgrey", font = ("Arial", 16))
        self.icLabel.pack(padx = 10, pady = 5)
        self.irLabel = tk.Label(self.master, text = "", bg = "darkgrey", font = ("Arial", 16))
        self.irLabel.pack(padx = 10, pady = 5)
        self.opcodeLabel = tk.Label(self.master, text = "", bg = "darkgrey", font = ("Arial", 16))
        self.opcodeLabel.pack(padx = 10, pady = 5)
        self.operandLabel = tk.Label(self.master, text = "", bg = "darkgrey", font = ("Arial", 16))
        self.operandLabel.pack(padx = 10, pady = 5)
        self.update()

    def update(self):
        self.accLabel.config(text=f"Accumulator: {self.cpu.accumulator}")
        self.icLabel.config(text=f"Instruction Counter: {self.cpu.instructionCounter}")
        self.irLabel.config(text=f"Instruction Register: {self.cpu.instructionRegister}")
        self.opcodeLabel.config(text=f"Opcode: {self.cpu.opcode}")
        self.operandLabel.config(text=f"Operand: {self.cpu.operand}")
        self.master.after(100, self.update)
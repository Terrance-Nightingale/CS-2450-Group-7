import tkinter as tk

class CPUStatePanel:
    def __init__(self, master, cpu):
        self.cpu = cpu
        self.master = master
        self.color = "#106511"

        self.acc_label = tk.Label(self.master, text = "", font = ("Arial", 16))
        self.acc_label.pack(side = "left", padx = 10, pady = 5)
        self.ic_label = tk.Label(self.master, text = "", font = ("Arial", 16))
        self.ic_label.pack(side = "left", padx = 10, pady = 5)
        self.ir_label = tk.Label(self.master, text = "", font = ("Arial", 16))
        self.ir_label.pack(side = "left", padx = 10, pady = 5)
        self.opcode_label = tk.Label(self.master, text = "", font = ("Arial", 16))
        self.opcode_label.pack(side = "left", padx = 10, pady = 5)
        self.operand_label = tk.Label(self.master, text = "", font = ("Arial", 16))
        self.operand_label.pack(side = "left", padx = 10, pady = 5)
        self.update()

    def update(self):
        self.acc_label.config(bg = self.color, fg = "white", text=f"Accumulator: {self.cpu.accumulator}")
        self.ic_label.config(bg = self.color, fg = "white",text=f"Instruction Counter: {self.cpu.instruction_counter}")
        self.ir_label.config(bg = self.color, fg = "white",text=f"Instruction Register: {self.cpu.instruction_register}")
        self.opcode_label.config(bg = self.color, fg = "white",text=f"Opcode: {self.cpu.opcode}")
        self.operand_label.config(bg = self.color, fg = "white",text=f"Operand: {self.cpu.operand}")
        self.master.after(100, self.update)

    def setColor(self, newColor):
        self.color = newColor
        self.update()
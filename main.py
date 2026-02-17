from Backend.cpu import CPU
from Backend.UserProgram import UserProgram
from Backend.UVSim import UVSim

if __name__ == "__main__":
    uvsim = UVSim()
    test = UserProgram()

    test.inputProgram()

    uvsim.loadProgram(test)
    uvsim.runProgram()
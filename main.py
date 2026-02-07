from cpu import CPU
from UserProgram import UserProgram
from UVSim import UVSim

if __name__ == "__main__":
    uvsim = UVSim()
    test = UserProgram()

    test.inputProgram()

    uvsim.loadProgram(test)
    uvsim.runProgram()
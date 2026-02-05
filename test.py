from cpu import CPU
from UserProgram import UserProgram
from UVSim import UVSim

uvsim = UVSim()
test = UserProgram()

test.inputProgram()

uvsim.loadProgram(test)
uvsim.runProgram()
#test.inputProgram()

#print(test.program)
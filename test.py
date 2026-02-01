from cpu import CPU

memory = [100] * 100

memory[0] = 2005
memory[1] = 1045

cpu = CPU(memory)

cpu.execute()

cpu.dump()
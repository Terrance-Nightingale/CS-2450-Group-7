import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import pytest
from unittest.mock import patch, Mock
from Backend.BasicML import BasicML
from Backend.cpu import CPU
from Backend.Memory import Memory
from Backend.UVSim import UVSim
from Backend.UserProgram import UserProgram

@pytest.fixture
def testUVSim():
    testuvsim = UVSim()
    return testuvsim

@pytest.fixture
def testProgramValid1():
    upv1 = UserProgram()
    upv1.program = [1007,1008,2007,3008,2109,1109,4300] #Test1.txt preloaded into a program ready for testing
    return upv1

# ────────────────────────────────────────────────
# Use Case 1: Enter a word when prompted (READ = 10)
# ────────────────────────────────────────────────
@pytest.mark.uc1
def test_read_stores_valid_input(monkeypatch, testUVSim):
    monkeypatch.setattr("builtins.input", lambda _: 1234)
    testUVSim.cpu.basicml.read(testUVSim.cpu.memory.mainMemory, 42)
    assert testUVSim.cpu.memory.mainMemory[42] == 1234

@pytest.mark.uc1
def test_read_repeated_until_valid_range(monkeypatch, testUVSim):
    inputs = [10000, -12345, 5678]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    testUVSim.cpu.basicml.read(testUVSim.cpu.memory.mainMemory, 19)
    assert testUVSim.cpu.memory.mainMemory[19] == 5678

# ────────────────────────────────────────────────
# Use Case 2: Inspect memory dump for debugging purposes
# ────────────────────────────────────────────────

@pytest.mark.uc2
def test_dump_shows_accumulator_and_ic(capsys, testUVSim):
    testUVSim.cpu.accumulator = -880
    testUVSim.cpu.instructionCounter = 17
    testUVSim.cpu.dump()
    captured = capsys.readouterr().out
    assert "-880" in captured
    assert "17" in captured

@pytest.mark.uc1
def test_dump_called_after_invalid_opcode(testUVSim, capsys):
    testUVSim.cpu.instructionRegister = 9900  # invalid
    testUVSim.cpu.opcode = 99
    testUVSim.cpu.execute()  # prints "Invalid"
    testUVSim.cpu.dump()
    captured = capsys.readouterr().out
    assert "Invalid" in captured
    assert "CPU DUMP" in captured

# ────────────────────────────────────────────────
# Use Case 3: Perform READ and WRITE operations properly
# ────────────────────────────────────────────────
@pytest.mark.uc3
def test_read_write_echo_program(testUVSim, monkeypatch, capsys):
    program = [1025, 1125, 4300]           # READ 25 → WRITE 25 → HALT
    testUVSim.loadProgram(Mock(program=program))
    monkeypatch.setattr("builtins.input", lambda _: "4242")
    testUVSim.runProgram()
    assert "4242" in capsys.readouterr().out

@pytest.mark.uc3
def test_write_uninitialized_location_prints_zero(testUVSim, capsys):
    testUVSim.cpu.execute()  # dummy to set opcode/operand if needed
    # simulate WRITE 88 where memory[88] = 0
    testUVSim.cpu.opcode = 11
    testUVSim.cpu.operand = 88
    testUVSim.cpu.execute()
    assert "0" in capsys.readouterr().out

@pytest.mark.uc3
def test_read_negative_number_stored_correctly(testUVSim, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: -777)
    testUVSim.cpu.basicml.read(testUVSim.cpu.memory.mainMemory, 33)
    assert testUVSim.cpu.memory.mainMemory[33] == -777

# ────────────────────────────────────────────────
# Use Case 4: Perform proper STORE operation
# ────────────────────────────────────────────────
@pytest.mark.uc4
def test_store_saves_accumulator_value(testUVSim):
    testUVSim.cpu.operand = 61
    testUVSim.cpu.opcode = 21
    testUVSim.cpu.accumulator = 5500
    testUVSim.cpu.execute()
    assert testUVSim.cpu.memory.mainMemory[testUVSim.cpu.operand] == 5500

@pytest.mark.uc4
def test_store_negative_value(testUVSim):
    testUVSim.cpu.accumulator = -2200
    testUVSim.cpu.operand = 12
    testUVSim.cpu.opcode = 21
    testUVSim.cpu.execute()
    assert testUVSim.cpu.memory.mainMemory[testUVSim.cpu.operand] == -2200

# ────────────────────────────────────────────────
# Use Case 5: Perform proper LOAD operation
# ────────────────────────────────────────────────
@pytest.mark.uc5
def test_load_sets_accumulator_from_memory(testUVSim):
    testUVSim.cpu.memory.mainMemory[44] = 9100
    testUVSim.cpu.opcode = 20
    testUVSim.cpu.operand = 44
    testUVSim.cpu.execute()
    assert testUVSim.cpu.accumulator == 9100

@pytest.mark.uc5
def test_load_negative_value(testUVSim):
    testUVSim.cpu.memory.mainMemory[77] = -400
    testUVSim.cpu.opcode = 20
    testUVSim.cpu.operand = 77
    testUVSim.cpu.execute()
    assert testUVSim.cpu.accumulator == -400

# ────────────────────────────────────────────────
# Use Case 6: Performs proper BRANCH operations
# ────────────────────────────────────────────────
@pytest.mark.uc6
def test_unconditional_branch_does_not_change_ic(testUVSim):
    testUVSim.cpu.opcode = 40
    testUVSim.cpu.operand = 37
    testUVSim.cpu.execute()
    assert testUVSim.cpu.instructionCounter == 37

@pytest.mark.uc6
def test_branchneg_taken_on_negative(testUVSim):
    testUVSim.cpu.accumulator = -1
    testUVSim.cpu.opcode = 41
    testUVSim.cpu.operand = 80
    testUVSim.cpu.execute()
    assert testUVSim.cpu.instructionCounter == 80

@pytest.mark.uc6
def test_branchzero_taken_on_zero(testUVSim):
    testUVSim.cpu.accumulator = 0
    testUVSim.cpu.opcode = 42
    testUVSim.cpu.operand = 15
    testUVSim.cpu.execute()
    assert testUVSim.cpu.instructionCounter == 15

@pytest.mark.uc6
def test_branchneg_not_taken_on_positive(testUVSim):
    testUVSim.cpu.accumulator = 5
    testUVSim.cpu.opcode = 41
    testUVSim.cpu.operand = 99
    old = testUVSim.cpu.instructionCounter
    testUVSim.cpu.execute()
    assert testUVSim.cpu.instructionCounter == old

# ────────────────────────────────────────────────
# Use Case 7: Perform proper ADD operation
# ────────────────────────────────────────────────
@pytest.mark.uc7
def test_add_positive_numbers(testUVSim):
    testUVSim.cpu.operand = 10
    testUVSim.cpu.memory.mainMemory[testUVSim.cpu.operand] = 2300
    testUVSim.cpu.accumulator = 1400
    testUVSim.cpu.opcode = 30
    testUVSim.cpu.execute()
    assert testUVSim.cpu.accumulator == 3700
    assert testUVSim.cpu.memory.mainMemory[testUVSim.cpu.operand] == 2300

# ────────────────────────────────────────────────
# Use Case 8: Perform proper SUB operation
# ────────────────────────────────────────────────
@pytest.mark.uc8
def test_subtract_to_negative(testUVSim):
    testUVSim.cpu.memory.mainMemory[20] = 6000
    testUVSim.cpu.accumulator = 1800
    testUVSim.cpu.opcode = 31
    testUVSim.cpu.operand = 20
    testUVSim.cpu.execute()
    assert testUVSim.cpu.accumulator == -4200
    assert testUVSim.cpu.memory.mainMemory[testUVSim.cpu.operand] == 6000   # fails

# ────────────────────────────────────────────────
# Use Case 9: Perform proper MUL operation
# ────────────────────────────────────────────────
@pytest.mark.uc9
def test_multiply_positive(testUVSim):
    testUVSim.cpu.operand = 30
    testUVSim.cpu.opcode = 33
    testUVSim.cpu.memory.mainMemory[testUVSim.cpu.operand] = 25
    testUVSim.cpu.accumulator = 48
    testUVSim.cpu.execute()
    assert testUVSim.cpu.accumulator == 1200
    assert testUVSim.memory.mainMemory[testUVSim.cpu.operand] == 25

@pytest.mark.uc9
def test_multiply_negative(testUVSim):
    testUVSim.cpu.operand = 31
    testUVSim.cpu.opcode = 33
    testUVSim.cpu.memory.mainMemory[testUVSim.cpu.operand] = -12
    testUVSim.cpu.accumulator = 50
    testUVSim.cpu.execute()
    assert testUVSim.cpu.accumulator == -600
    assert testUVSim.cpu.memory.mainMemory[testUVSim.cpu.operand] == -12

# ────────────────────────────────────────────────
# Use Case 10: Perform proper DIV operation
# ────────────────────────────────────────────────
@pytest.mark.uc10
def test_divide_normal(testUVSim):
    testUVSim.cpu.operand = 40
    testUVSim.cpu.opcode = 32
    testUVSim.cpu.memory.mainMemory[testUVSim.cpu.operand] = 5
    testUVSim.cpu.accumulator = 850
    testUVSim.cpu.execute()
    assert testUVSim.cpu.accumulator == 170.0 #test result is correct and in the accumulator
    assert testUVSim.cpu.memory.mainMemory[testUVSim.cpu.operand] == 5 #test memory wasn't altered

@pytest.mark.uc10
def test_divide_by_zero_error(testUVSim, capsys):
    testUVSim.cpu.operand = 41
    testUVSim.cpu.opcode = 32
    testUVSim.cpu.memory.mainMemory[testUVSim.cpu.operand] = 0
    testUVSim.cpu.accumulator = 9999
    testUVSim.cpu.execute()
    assert "Error: Division by zero" in capsys.readouterr().out

@pytest.mark.uc10
def test_divide_negative(testUVSim):
    testUVSim.cpu.operand = 42
    testUVSim.cpu.opcode = 32
    testUVSim.cpu.memory.mainMemory[testUVSim.cpu.operand] = 4
    testUVSim.cpu.accumulator = -800
    testUVSim.cpu.execute()
    assert testUVSim.cpu.accumulator == -200.0 #test result is correct and in the accumulator
    assert testUVSim.cpu.memory.mainMemory[testUVSim.cpu.operand] == 4 #test memory wasn't altered

# ────────────────────────────────────────────────
# Use Case 11: Perform proper HALT operation
# ────────────────────────────────────────────────
@pytest.mark.uc11
def test_halt_sets_running_false(testUVSim):
    testUVSim.cpu.opcode = 43
    testUVSim.cpu.running = True
    testUVSim.cpu.execute()
    assert testUVSim.cpu.running is False

@pytest.mark.uc11
def test_halt_stops_fetch_loop(testUVSim, capsys):
    program = [4300]
    testUVSim.loadProgram(Mock(program=program))
    testUVSim.runProgram()
    assert "CPU DUMP" in capsys.readouterr().out
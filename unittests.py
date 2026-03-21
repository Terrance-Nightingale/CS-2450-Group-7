import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import pytest
from unittest.mock import MagicMock
from Backend.UVSim import UVSim
from Backend.UserProgram import UserProgram

# Last updated by Jordan 3/18/26

@pytest.fixture
def testUVSim():
    testuvsim = UVSim()
    return testuvsim

# --------------------------
# Use case 01: READ command
# --------------------------
@pytest.mark.uc01
def test_read_stores_valid_input(testUVSim):
    """
    Bypass user input, just check if read will put the desired input into the specified memory location
    """
    user_input = 1234
    testUVSim.cpu.basicml.read(testUVSim.cpu.memory.main_memory(), 67, user_input)
    assert testUVSim.cpu.memory.main_memory()[67] == 1234


@pytest.mark.uc01
def test_read_overwrites_existing_value(testUVSim):
    """
    Bypass actual user input, just check if READ properly overwrites contents of specified memory location
    """
    testUVSim.cpu.memory.main_memory()[67] = 1234
    testUVSim.cpu.basicml.read(testUVSim.cpu.memory.main_memory(), 67, 5678)
    assert testUVSim.cpu.memory.main_memory()[67] == 5678

# --------------------------
# Use Case 02: WRITE command
# --------------------------
@pytest.mark.uc02
def test_write_echoes(testUVSim):
    """
    Preload a value into memory, then mock the console panel, then test if write echoes the contents of the specified memory location
    """
    testUVSim.cpu.memory.main_memory()[67] = 1234
    mock_panel = MagicMock()
    testUVSim.cpu.basicml.console_panel = mock_panel
    testUVSim.cpu.basicml.write(testUVSim.cpu.memory.main_memory(), 67)
    mock_panel.update_prev_outputs.assert_called_once_with("WRITE 1234")

@pytest.mark.uc02
def test_write_no_panel(testUVSim):
    """
    Preload a value into memory, then check that the write command doesn't crash if an output panel isn't present
    """
    testUVSim.cpu.memory.main_memory()[67] = 1234
    testUVSim.cpu.basicml.console_panel = None
    testUVSim.cpu.basicml.write(testUVSim.cpu.memory.main_memory(), 67)

# --------------------------
# Use Case 03: LOAD Commmand
# --------------------------
@pytest.mark.uc03
def test_load_sets_accumulator_from_memory(testUVSim):
    """
    Check that the LOAD command properly copies the value from a specified memory location to the accumulator
    """
    testUVSim.cpu.memory.main_memory()[67] = 1234
    testUVSim.cpu.opcode = 20
    testUVSim.cpu.operand = 67
    testUVSim.cpu.execute()
    assert testUVSim.cpu.accumulator == 1234

@pytest.mark.uc03
def test_load_negative_value(testUVSim):
    """
    Check that the LOAD command properly copies a negative value from a specified memory location to the accumulator
    """
    testUVSim.cpu.memory.main_memory()[67] = -1234
    testUVSim.cpu.opcode = 20
    testUVSim.cpu.operand = 67
    testUVSim.cpu.execute()
    assert testUVSim.cpu.accumulator == -1234

# ────────────────────────────────────────────────
# Use Case 04: STORE Command
# ────────────────────────────────────────────────
@pytest.mark.uc04
def test_store_saves_accumulator_value(testUVSim):
    """
    Check that STORE command properly saves value in accumulator to specified memory location
    """
    testUVSim.cpu.operand = 67
    testUVSim.cpu.opcode = 21
    testUVSim.cpu.accumulator = 1234
    testUVSim.cpu.execute()
    assert testUVSim.cpu.memory.main_memory()[testUVSim.cpu.operand] == 1234

@pytest.mark.uc04
def test_store_negative_value(testUVSim):
    """
    Check that STORE works with negative values too
    """
    testUVSim.cpu.accumulator = -1234
    testUVSim.cpu.operand = 67
    testUVSim.cpu.opcode = 21
    testUVSim.cpu.execute()
    assert testUVSim.cpu.memory.main_memory()[testUVSim.cpu.operand] == -1234

# ────────────────────────────────────────────────
# Use Case 05: ADD Command
# ────────────────────────────────────────────────
@pytest.mark.uc05
def test_add_positive_numbers(testUVSim):
    """
    Check that ADD command properly adds value in accumulator and value in specified memory location and stores result in the accumulator
    Also check that it doesn't change the value in the specified memory location
    """
    testUVSim.cpu.operand = 67
    testUVSim.cpu.memory.main_memory()[testUVSim.cpu.operand] = 2300
    testUVSim.cpu.accumulator = 1400
    testUVSim.cpu.opcode = 30
    testUVSim.cpu.execute()
    assert testUVSim.cpu.accumulator == 3700
    assert testUVSim.cpu.memory.main_memory()[testUVSim.cpu.operand] == 2300

@pytest.mark.uc05
def test_add_negative_numbers(testUVSim):
    """
    Check that ADD command properly adds a negative value in accumulator and a negative value in specified memory location and stores result in the accumulator
    Also check that it doesn't change the value in the specified memory location
    """
    testUVSim.cpu.operand = 67
    testUVSim.cpu.memory.main_memory()[testUVSim.cpu.operand] = -2300
    testUVSim.cpu.accumulator = -1400
    testUVSim.cpu.opcode = 30
    testUVSim.cpu.execute()
    assert testUVSim.cpu.accumulator == -3700
    assert testUVSim.cpu.memory.main_memory()[testUVSim.cpu.operand] == -2300

# ────────────────────────────────────────────────
# Use Case 06: SUBTRACT Command
# ────────────────────────────────────────────────
@pytest.mark.uc06
def test_subtract_from_positive(testUVSim):
    """
    Check that SUBTRACT command properly subtracts the value in a specified memory location from the value in the accumulator
    Also check that the result is stored in the accumulator
    Also check that the contents of the specified memory location haven't been changed
    """
    testUVSim.cpu.memory.main_memory()[67] = 6000
    testUVSim.cpu.accumulator = 1800
    testUVSim.cpu.opcode = 31
    testUVSim.cpu.operand = 67
    testUVSim.cpu.execute()
    assert testUVSim.cpu.accumulator == -4200
    assert testUVSim.cpu.memory.main_memory()[testUVSim.cpu.operand] == 6000

@pytest.mark.uc06
def test_subtract_from_negative(testUVSim):
    """
    Check that SUBTRACT command properly subtracts the value in a specified memory location from the negative value in the accumulator
    Also check that the result is stored in the accumulator
    Also check that the contents of the specified memory location haven't been changed
    """
    testUVSim.cpu.memory.main_memory()[67] = 6000
    testUVSim.cpu.accumulator = -1800
    testUVSim.cpu.opcode = 31
    testUVSim.cpu.operand = 67
    testUVSim.cpu.execute()
    assert testUVSim.cpu.accumulator == -7800
    assert testUVSim.cpu.memory.main_memory()[testUVSim.cpu.operand] == 6000

# ────────────────────────────────────────────────
# Use Case 07: DIVIDE Command
# ────────────────────────────────────────────────
@pytest.mark.uc07
def test_divide_normal(testUVSim):
    """
    Check that the DIVIDE command properly divides the value in the accumulator by the value in the specified memory location
    Also check that the result is stored in the accumulator
    Also check that the contents of the specified memory location haven't been changed
    """
    testUVSim.cpu.operand = 67
    testUVSim.cpu.opcode = 32
    testUVSim.cpu.memory.main_memory()[testUVSim.cpu.operand] = 5
    testUVSim.cpu.accumulator = 850
    testUVSim.cpu.execute()
    assert testUVSim.cpu.accumulator == 170.0
    assert testUVSim.cpu.memory.main_memory()[testUVSim.cpu.operand] == 5

@pytest.mark.uc07
def test_divide_by_zero_error(testUVSim):
    """
    Check that the DIVIDE command properly checks that the divisor is 0 and raises an error without crashing
    """
    testUVSim.cpu.operand = 67
    testUVSim.cpu.opcode = 32
    testUVSim.cpu.memory.main_memory()[67] = 0
    testUVSim.cpu.accumulator = 9999
    testUVSim.cpu.execute()
    assert "Error: Division by zero" in testUVSim.cpu.basicml.error_message

@pytest.mark.uc07
def test_divide_negative(testUVSim):
    """
    Check that the DIVIDE command properly divides the negative value in the accumulator by the value in the specified memory location
    Also check that the result is stored in the accumulator
    Also check that the contents of the specified memory location haven't been changed
    """
    testUVSim.cpu.operand = 67
    testUVSim.cpu.opcode = 32
    testUVSim.cpu.memory.main_memory()[testUVSim.cpu.operand] = 4
    testUVSim.cpu.accumulator = -800
    testUVSim.cpu.execute()
    assert testUVSim.cpu.accumulator == -200.0
    assert testUVSim.cpu.memory.main_memory()[testUVSim.cpu.operand] == 4

# ────────────────────────────────────────────────
# Use Case 08: MULTIPLY Command
# ────────────────────────────────────────────────
@pytest.mark.uc08
def test_multiply_positive(testUVSim):
    """
    Check that the MULTIPLY Command properly multiplies the value of the accumulator by the value in the specified memory location
    Also check that the result is stored in the accumulator
    Also check that the contents of the specified memory location haven't been changed
    """
    testUVSim.cpu.operand = 67
    testUVSim.cpu.opcode = 33
    testUVSim.cpu.memory.main_memory()[testUVSim.cpu.operand] = 25
    testUVSim.cpu.accumulator = 48
    testUVSim.cpu.execute()
    assert testUVSim.cpu.accumulator == 1200
    assert testUVSim.memory.main_memory()[testUVSim.cpu.operand] == 25

@pytest.mark.uc08
def test_multiply_negative(testUVSim):
    """
    Check that the MULTIPLY Command properly multiplies the value of the accumulator by the negative value in the specified memory location
    Also check that the result is stored in the accumulator
    Also check that the contents of the specified memory location haven't been changed
    """
    testUVSim.cpu.operand = 31
    testUVSim.cpu.opcode = 33
    testUVSim.cpu.memory.main_memory()[testUVSim.cpu.operand] = -12
    testUVSim.cpu.accumulator = 50
    testUVSim.cpu.execute()
    assert testUVSim.cpu.accumulator == -600
    assert testUVSim.cpu.memory.main_memory()[testUVSim.cpu.operand] == -12

# ────────────────────────────────────────────────
# Use Case 09: BRANCH Command
# ────────────────────────────────────────────────
@pytest.mark.uc09
def test_branch_changes_instruction_counter(testUVSim):
    """
    Check that the BRANCH command properly changes the instruction counter to the specified memory location
    """
    testUVSim.cpu.opcode = 40
    testUVSim.cpu.operand = 67
    testUVSim.cpu.execute()
    assert testUVSim.cpu.instruction_counter == 67

@pytest.mark.uc09
def test_branch_unconditionally(testUVSim):
    """
    Check that the BRANCH command properly changes the instruction counter to the specified memory location regardless of accumulator value
    """
    testUVSim.cpu.opcode = 40
    testUVSim.cpu.operand = 67
    testUVSim.cpu.accumulator = 1234
    testUVSim.cpu.execute()
    assert testUVSim.cpu.instruction_counter == 67
    testUVSim.cpu.opcode = 40
    testUVSim.cpu.operand = 67
    testUVSim.cpu.accumulator = -1234
    testUVSim.cpu.execute()
    assert testUVSim.cpu.instruction_counter == 67

# ────────────────────────────────────────────────
# Use Case 10: BRANCHNEG Command
# ────────────────────────────────────────────────
@pytest.mark.uc10
def test_branchneg_on_negative(testUVSim):
    """
    Check that BRANCHNEG command properly sets instruction counter equal to the specified memory location when accumulator value is negative
    """
    testUVSim.cpu.accumulator = -1
    testUVSim.cpu.opcode = 41
    testUVSim.cpu.operand = 67
    testUVSim.cpu.instruction_counter = 89
    testUVSim.cpu.execute()
    assert testUVSim.cpu.instruction_counter == 67

@pytest.mark.uc10
def test_no_branchneg_on_zero(testUVSim):
    """
    Check that BRANCHNEG command doesn't branch when the accumulator value is zero
    """
    testUVSim.cpu.accumulator = 0
    testUVSim.cpu.opcode = 41
    testUVSim.cpu.operand = 67
    testUVSim.cpu.instruction_counter = 89
    testUVSim.cpu.execute()
    assert testUVSim.cpu.instruction_counter == 89

@pytest.mark.uc10
def test_no_branchneg_on_positive(testUVSim):
    """
    Check that BRANCHNEG command doesn't branch when the accumulator value is positive
    """
    testUVSim.cpu.accumulator = 1234
    testUVSim.cpu.opcode = 41
    testUVSim.cpu.operand = 67
    testUVSim.cpu.instruction_counter = 89
    testUVSim.cpu.execute()
    assert testUVSim.cpu.instruction_counter == 89

# ────────────────────────────────────────────────
# Use Case 11: BRANCHZERO Command
# ────────────────────────────────────────────────
@pytest.mark.uc11
def test_branchzero_on_zero(testUVSim):
    """
    Check that BRANCH command properly sets instruction counter equal to the specified memory location when accumulator value is zero
    """
    testUVSim.cpu.accumulator = 0
    testUVSim.cpu.opcode = 42
    testUVSim.cpu.operand = 67
    testUVSim.cpu.instruction_counter = 89
    testUVSim.cpu.execute()
    assert testUVSim.cpu.instruction_counter == 67

@pytest.mark.uc11
def test_branchzero_not_on_negative(testUVSim):
    """
    Check that BRANCHZERO command doesn't branch when the accumulator value is negative
    """
    testUVSim.cpu.accumulator = -1234
    testUVSim.cpu.opcode = 42
    testUVSim.cpu.operand = 67
    testUVSim.cpu.instruction_counter = 89
    testUVSim.cpu.execute()
    assert testUVSim.cpu.instruction_counter == 89

@pytest.mark.uc11
def test_branchzero_not_on_positive(testUVSim):
    """
    Check that BRANCHZERO command doesn't branch when the accumulator value is positive
    """
    testUVSim.cpu.accumulator = 1234
    testUVSim.cpu.opcode = 42
    testUVSim.cpu.operand = 67
    testUVSim.cpu.instruction_counter = 89
    testUVSim.cpu.execute()
    assert testUVSim.cpu.instruction_counter == 89

# ────────────────────────────────────────────────
# Use Case 12: HALT Command
# ────────────────────────────────────────────────
@pytest.mark.uc12
def test_halt_sets_running_false(testUVSim):
    """
    Check that the HALT command properly stops the CPU cycle by setting cpu.running to False
    """
    testUVSim.cpu.opcode = 43
    testUVSim.cpu.running = True
    testUVSim.cpu.execute()
    assert testUVSim.cpu.running is False

@pytest.mark.uc12
def test_halt_stops_execution(testUVSim):
    """
    Check that the HALT command actually stops program execution
    LOAD command shouldn't be executed
    """
    testUVSim.cpu.memory.main_memory()[0] = 4300 
    testUVSim.cpu.memory.main_memory()[1] = 2099
    testUVSim.run_program()
    assert testUVSim.cpu.accumulator == 0
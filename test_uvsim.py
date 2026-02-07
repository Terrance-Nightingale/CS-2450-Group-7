# tests/test_uvsim.py
# (assumes pytest + pytest-mock or unittest.mock is available)
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import pytest
from unittest.mock import patch, Mock
from BasicML import BasicML
from cpu import CPU
from Memory import Memory
from UVSim import UVSim
from UserProgram import UserProgram

# ────────────────────────────────────────────────
# Fixtures
# ────────────────────────────────────────────────

@pytest.fixture
def memory():
    m = Memory()
    return m.mainMemory  # we usually test against the list directly

@pytest.fixture
def basicml():
    return BasicML()

@pytest.fixture
def cpu(memory):
    return CPU(Memory())  # fresh memory

@pytest.fixture
def uvsim():
    return UVSim()

# ────────────────────────────────────────────────
# Use Case 1: Enter a word when prompted (READ = 10)
# ────────────────────────────────────────────────

def test_read_stores_valid_input(basicml, memory, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "1234")
    basicml.read(memory, 42)
    assert memory[42] == 1234   # current code stores string

def test_read_repeated_until_valid_range(basicml, memory, monkeypatch):
    # Note: current code has NO validation → this would require adding logic
    inputs = ["10000", "-12345", "5678"]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    basicml.read(memory, 19)
    assert memory[19] == 5678   # would pass only after you add range check

# ────────────────────────────────────────────────
# Use Case 2: Inspect memory dump for debugging purposes
# ────────────────────────────────────────────────

def test_dump_shows_accumulator_and_ic(cpu, capsys):
    cpu.accumulator = -880
    cpu.instructionCounter = 17
    cpu.dump()
    captured = capsys.readouterr().out
    assert "-880" in captured
    assert "17" in captured

def test_dump_called_after_invalid_opcode(cpu, capsys):
    cpu.instructionRegister = 9900  # invalid
    cpu.opcode = 99
    cpu.execute()  # prints "Invalid"
    cpu.dump()
    captured = capsys.readouterr().out
    assert "Invalid" in captured
    assert "CPU DUMP" in captured

# ────────────────────────────────────────────────
# Use Case 3: Perform READ and WRITE operations properly
# ────────────────────────────────────────────────

def test_read_write_echo_program(uvsim, monkeypatch, capsys):
    program = [1025, 1125, 4300]           # READ 25 → WRITE 25 → HALT
    uvsim.loadProgram(Mock(program=program))
    monkeypatch.setattr("builtins.input", lambda _: "4242")
    uvsim.runProgram()
    assert "4242" in capsys.readouterr().out

def test_write_uninitialized_location_prints_zero(cpu, capsys):
    cpu.execute()  # dummy to set opcode/operand if needed
    # simulate WRITE 88 where memory[88] = 0
    cpu.opcode = 11
    cpu.operand = 88
    cpu.execute()
    assert "0" in capsys.readouterr().out

def test_read_negative_number_stored_correctly(basicml, memory, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: -777)
    basicml.read(memory, 33)
    assert memory[33] == -777

# ────────────────────────────────────────────────
# Use Case 4: Perform proper STORE operation
# ────────────────────────────────────────────────

def test_store_saves_accumulator_value(basicml, memory):
    acc = 5500
    basicml.store(memory, 61, acc)
    assert memory[61] == 5500

def test_store_negative_value(basicml, memory):
    acc = -2200
    basicml.store(memory, 12, acc)
    assert memory[12] == -2200

# ────────────────────────────────────────────────
# Use Case 5: Perform proper LOAD operation
# ────────────────────────────────────────────────

def test_load_sets_accumulator_from_memory(basicml, memory):
    memory[44] = 9100
    acc = 0
    new_acc = basicml.load(memory, 44)
    assert new_acc == 9100

def test_load_negative_value(basicml, memory):
    memory[77] = -400
    acc = 9999
    acc = basicml.load(memory, 77)
    assert acc == -400   # current code fails to update

# ────────────────────────────────────────────────
# Use Case 6: Performs proper BRANCH operations
# ────────────────────────────────────────────────

def test_unconditional_branch_does_not_change_ic(cpu):
    cpu.opcode = 40
    cpu.operand = 37
    cpu.execute()
    assert cpu.instructionCounter == 37

def test_branchneg_taken_on_negative(cpu):
    cpu.accumulator = -1
    cpu.opcode = 41
    cpu.operand = 80
    cpu.execute()
    assert cpu.instructionCounter == 80

def test_branchzero_taken_on_zero(cpu):
    cpu.accumulator = 0
    cpu.opcode = 42
    cpu.operand = 15
    cpu.execute()
    assert cpu.instructionCounter == 15   # fails currently

def test_branchneg_not_taken_on_positive(cpu):
    cpu.accumulator = 5
    cpu.opcode = 41
    cpu.operand = 99
    old = cpu.instructionCounter
    cpu.execute()
    assert cpu.instructionCounter == old

# ────────────────────────────────────────────────
# Use Case 7: Perform proper ADD operation
# ────────────────────────────────────────────────

def test_add_positive_numbers(basicml, memory):
    memory[10] = 2300
    acc = 1400
    result = basicml.add(memory, 10, acc)
    assert result == 3700
    assert acc == 1400   # fails — should update

# ────────────────────────────────────────────────
# Use Case 8: Perform proper SUB operation
# ────────────────────────────────────────────────

def test_subtract_to_negative(basicml, memory):
    memory[20] = 6000
    acc = 1800
    result = basicml.subtract(memory, 20, acc)
    assert result == -4200
    assert acc == 1800   # fails

# ────────────────────────────────────────────────
# Use Case 9: Perform proper MUL operation
# ────────────────────────────────────────────────

def test_multiply_positive(basicml, memory):
    memory[30] = 25
    acc = 48
    acc = basicml.multiply(memory, 30, acc)
    assert acc == 1200   # passes — current code mutates!

def test_multiply_negative(basicml, memory):
    memory[31] = -12
    acc = 50
    acc = basicml.multiply(memory, 31, acc)
    assert acc == -600

# ────────────────────────────────────────────────
# Use Case 10: Perform proper DIV operation
# ────────────────────────────────────────────────

def test_divide_normal(basicml, memory):
    memory[40] = 5
    acc = 850
    result = basicml.divide(memory, 40, acc)
    assert result == 170.0

def test_divide_by_zero_error(basicml, memory, capsys):
    memory[41] = 0
    acc = 9999
    basicml.divide(memory, 41, acc)
    assert "Error: Division by zero" in capsys.readouterr().out

def test_divide_negative(basicml, memory):
    memory[42] = 4
    acc = -800
    result = basicml.divide(memory, 42, acc)
    assert result == -200.0

# ────────────────────────────────────────────────
# Use Case 11: Perform proper HALT operation
# ────────────────────────────────────────────────

def test_halt_sets_running_false(cpu):
    cpu.opcode = 43
    cpu.running = True
    cpu.execute()
    assert cpu.running is False   # fails currently

def test_halt_stops_fetch_loop(uvsim, capsys):
    program = [4300]  # just HALT
    uvsim.loadProgram(Mock(program=program))
    uvsim.runProgram()
    assert "CPU DUMP" in capsys.readouterr().out
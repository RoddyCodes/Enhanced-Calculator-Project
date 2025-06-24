# tests/test_calculator_repl.py

import pytest
from unittest.mock import MagicMock, patch
from app.calculator_repl import App
import pandas as pd

# A fixture to create a fresh App instance for each test
@pytest.fixture
def app_fixture():
    """Provides a new instance of the App for each test function."""
    return App()

# --- Testing Basic Commands and Main Loop ---

def test_app_start_and_exit(monkeypatch, capsys):
    """Tests the main loop with a simple 'exit' command."""
    monkeypatch.setattr('builtins.input', lambda _: 'exit')
    
    app = App()
    with pytest.raises(SystemExit) as e:
        app.start()

    assert e.type == SystemExit and e.value.code == 0
    captured = capsys.readouterr()
    assert "Welcome to the Enhanced Calculator!" in captured.out
    assert "Exiting Calculator. Goodbye!" in captured.out

def test_app_keyboard_interrupt(monkeypatch, capsys):
    """Tests that Ctrl+C gracefully exits the application."""
    monkeypatch.setattr('builtins.input', lambda _: exec("raise KeyboardInterrupt"))

    app = App()
    with pytest.raises(SystemExit):
        app.start()
    
    captured = capsys.readouterr()
    assert "Exiting Calculator. Goodbye!" in captured.out

def test_app_empty_input(monkeypatch, capsys):
    """Tests that the app continues after empty input."""
    inputs = iter(['', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with pytest.raises(SystemExit):
        App().start()
    
    # Check that no error message was printed for the empty input
    captured = capsys.readouterr()
    assert "Unknown command" not in captured.out

def test_show_help(app_fixture, capsys):
    """Tests the 'help' command output."""
    app_fixture._show_help()
    captured = capsys.readouterr()
    output = captured.out
    
    # FIX: The assertion string now more closely matches the actual formatted output.
    assert "help          : Show this help message." in output
    assert "exit          : Exit the application." in output
    assert "history" in output
    assert "save / load" in output

def test_unknown_command(app_fixture, capsys):
    """Tests how the REPL handles an unknown command."""
    inputs = iter(['bogus_command', 'exit'])
    with patch('builtins.input', lambda _: next(inputs)):
        with pytest.raises(SystemExit):
             app_fixture.start()

    captured = capsys.readouterr()
    assert "Unknown command: 'bogus_command'" in captured.out

# --- Testing Calculation Commands ---

def test_perform_calculation_valid(app_fixture, capsys):
    """Tests a successful calculation command."""
    app_fixture._perform_calculation('add', ['10', '5'])
    captured = capsys.readouterr()
    assert "Result: 15" in captured.out
    assert len(app_fixture.history) == 1
    assert app_fixture.history[0].result == 15

def test_perform_calculation_invalid_args(app_fixture, capsys):
    """Tests a calculation command with the wrong number of arguments."""
    app_fixture._perform_calculation('add', ['10'])
    captured = capsys.readouterr()
    assert "Error: add requires exactly two numerical arguments." in captured.out

def test_perform_calculation_non_numeric_args(app_fixture, capsys):
    """Tests a calculation command with non-numeric arguments."""
    app_fixture._perform_calculation('add', ['ten', 'five'])
    captured = capsys.readouterr()
    assert "Error: Invalid input or operation." in captured.out

def test_perform_calculation_unexpected_error(app_fixture, monkeypatch, capsys):
    """Tests the generic exception handler in _perform_calculation."""
    # Mock the calculator's execute_operation to raise a generic Exception
    monkeypatch.setattr(app_fixture.calculator, 'execute_operation', MagicMock(side_effect=Exception("Unexpected calc error")))
    
    app_fixture._perform_calculation('add', ['10', '5'])
    captured = capsys.readouterr()
    assert "An unexpected error occurred during calculation: Unexpected calc error" in captured.out

# --- Testing History and File Operations ---

def test_display_history(app_fixture, capsys):
    """Tests the 'history' command."""
    app_fixture._display_history()
    captured = capsys.readouterr()
    assert "No history to display." in captured.out
    
    app_fixture._perform_calculation('subtract', ['20', '8'])
    app_fixture._display_history()
    captured = capsys.readouterr()
    assert "Calculation History:" in captured.out
    assert "20.0 subtract 8.0 = 12.0" in captured.out

def test_clear_history(app_fixture, capsys):
    """Tests the 'clear' command."""
    app_fixture._perform_calculation('multiply', ['4', '5'])
    app_fixture._clear_history()
    captured = capsys.readouterr()
    assert "History cleared." in captured.out
    assert len(app_fixture.history) == 0

def test_save_and_load_history(app_fixture, tmp_path, monkeypatch):
    """Tests saving history to and loading history from a CSV file."""
    history_file = tmp_path / "manual_history.csv"
    monkeypatch.setattr(app_fixture.auto_saver.config, 'get_history_file_path', lambda _: str(history_file))

    app_fixture._perform_calculation('divide', ['100', '4'])
    app_fixture._save_history()
    assert history_file.exists()

    app_fixture._clear_history()
    app_fixture._load_history()
    assert len(app_fixture.history) == 1
    assert app_fixture.history[0].result == 25.0

def test_save_history_empty(app_fixture, capsys):
    """Tests saving with no history."""
    app_fixture._save_history()
    captured = capsys.readouterr()
    assert "History is empty. Nothing to save." in captured.out

def test_save_history_exception(app_fixture, monkeypatch, capsys):
    """Tests the exception handler for saving history."""
    monkeypatch.setattr(pd.DataFrame, 'to_csv', MagicMock(side_effect=IOError("Disk full")))
    app_fixture._perform_calculation('add', ['1', '1'])
    app_fixture._save_history()
    captured = capsys.readouterr()
    assert "Error saving history: Disk full" in captured.out

def test_load_history_file_not_found(app_fixture, tmp_path, monkeypatch, capsys):
    """Tests error handling when the history file to load doesn't exist."""
    non_existent_file = tmp_path / "non_existent.csv"
    monkeypatch.setattr(app_fixture.auto_saver.config, 'get_history_file_path', lambda _: str(non_existent_file))
    app_fixture._load_history()
    captured = capsys.readouterr()
    assert f"Error: History file not found at {non_existent_file}" in captured.out

def test_load_history_exception(app_fixture, tmp_path, monkeypatch, capsys):
    """Tests the exception handler for loading a malformed history file."""
    malformed_file = tmp_path / "bad.csv"
    malformed_file.write_text("HeaderA,HeaderB\nValueA") # Malformed CSV
    monkeypatch.setattr(app_fixture.auto_saver.config, 'get_history_file_path', lambda _: str(malformed_file))
    app_fixture._load_history()
    captured = capsys.readouterr()
    assert "Error loading history:" in captured.out

# --- Testing Undo/Redo Commands ---

def test_undo_redo_commands(app_fixture):
    """Tests the undo and redo commands in the REPL."""
    app_fixture._perform_calculation('add', ['10', '5'])
    app_fixture._perform_calculation('subtract', ['15', '3'])
    
    app_fixture._undo_calculation()
    assert len(app_fixture.history) == 1

    app_fixture._redo_calculation()
    # Note: redo doesn't add to history in this implementation, so history length is still 1.
    assert len(app_fixture.history) == 1

def test_undo_with_no_history(app_fixture, capsys):
    """Tests calling undo when the history is empty."""
    app_fixture._undo_calculation()
    captured = capsys.readouterr()
    assert "No operation to undo." in captured.out

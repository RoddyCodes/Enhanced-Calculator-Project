
import pytest
from unittest.mock import MagicMock, patch
from app.calculator_repl import App
import pandas as pd
from app.calculator_config import config # Import the config singleton

@pytest.fixture
def app_fixture():
    """Provides a fresh, initialized App instance for each test function."""
    return App()

# --- Main REPL Loop and Command Dispatching Tests ---

def test_app_start_and_exit(monkeypatch, capsys):
    """Tests the main loop starts, prints a welcome, and exits cleanly."""
    monkeypatch.setattr('builtins.input', lambda _: 'exit')
    
    with pytest.raises(SystemExit) as e:
        App().start()

    assert e.value.code == 0
    captured = capsys.readouterr()
    assert "Welcome to the Enhanced Calculator!" in captured.out
    assert "Exiting Calculator. Goodbye!" in captured.out

def test_app_keyboard_interrupt(monkeypatch, capsys):
    """Tests that Ctrl+C (KeyboardInterrupt) exits the application gracefully."""
    monkeypatch.setattr('builtins.input', lambda _: exec("raise KeyboardInterrupt"))

    with pytest.raises(SystemExit):
        App().start()
    
    captured = capsys.readouterr()
    assert "Exiting Calculator. Goodbye!" in captured.out

def test_app_main_loop_generic_exception(monkeypatch, capsys):
    """Tests the main loop's generic exception handler."""
    # Simulate a generic error, followed by a KeyboardInterrupt to exit the loop
    monkeypatch.setattr('builtins.input', MagicMock(side_effect=[Exception("A generic error"), KeyboardInterrupt]))

    with pytest.raises(SystemExit):
        App().start()

    captured = capsys.readouterr()
    assert "An unexpected error occurred: A generic error" in captured.out

# --- Command-Specific Tests (testing internal logic for edge cases) ---

def test_perform_calculation_unexpected_error(app_fixture, monkeypatch, capsys):
    """Tests the generic exception handler in _perform_calculation."""
    monkeypatch.setattr(app_fixture.calculator, 'execute_operation', MagicMock(side_effect=Exception("Calc error")))
    
    app_fixture._perform_calculation('add', ['10', '5'])
    captured = capsys.readouterr()
    assert "An unexpected error occurred during calculation: Calc error" in captured.out

def test_save_history_exception(app_fixture, monkeypatch, capsys):
    """Tests the exception handler for the 'save' command."""
    monkeypatch.setattr(pd.DataFrame, 'to_csv', MagicMock(side_effect=IOError("Permission denied")))
    app_fixture._perform_calculation('add', ['1', '1'])
    app_fixture._save_history()
    captured = capsys.readouterr()
    assert "Error saving history: Permission denied" in captured.out

def test_load_history_exception(app_fixture, tmp_path, monkeypatch, capsys):
    """Tests the exception handler for loading a malformed history file."""
    malformed_file = tmp_path / "bad.csv"
    malformed_file.write_text("HeaderA,HeaderB\nValueA")
    monkeypatch.setattr(config, 'get_history_file_path', lambda _, filename="manual_history.csv": str(malformed_file))
    app_fixture._load_history()
    captured = capsys.readouterr()
    assert "Error loading history:" in captured.out

# --- Full User Session Simulation Test ---

def test_full_user_session_simulation(monkeypatch, capsys, tmp_path):
    """
    Simulates a full user session to test command dispatching, calculations,
    history management, file operations, and error handling through the main loop.
    """
    history_file = tmp_path / "manual_history.csv"
    
    inputs = iter([
        '', 'add 10 5', 'history', 'save', 'clear', 'history',
        'undo', 'load', 'history', 'undo', 'redo',
        'bogus', 'add 10', 'divide 10 0', 'exit'
    ])
    
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    # FIX: This lambda is now more flexible, accepting any arguments and always returning the temp path.
    monkeypatch.setattr(config, 'get_history_file_path', lambda *args, **kwargs: str(history_file))

    with pytest.raises(SystemExit):
        App().start()

    output = capsys.readouterr().out
    
    assert "Result: 15.0" in output
    assert "10.0 add 5.0 = 15.0" in output
    assert f"History successfully saved to {history_file}" in output
    assert "History cleared." in output
    assert "No history to display." in output
    assert "No operation to undo." in output
    assert f"History successfully loaded from {history_file}" in output
    assert "Undoing last operation..." in output
    assert "Redoing last operation..." in output
    assert "Unknown command: 'bogus'" in output
    assert "Error: Exactly two numerical arguments are required." in output
    assert "Error: Cannot divide by zero." in output
    assert "Exiting Calculator. Goodbye!" in output

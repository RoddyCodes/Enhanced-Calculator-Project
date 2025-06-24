import os
import importlib
import pytest
import pandas as pd
from unittest.mock import MagicMock
from app.calculator import Calculator
from app.logger import LoggingObserver, AutoSaveObserver
from app import calculator_config
from app.calculator_config import setup_logging

def setup_test_environment(monkeypatch, settings):
    """
    A pytest helper to set env vars, reload the config, and set up logging.
    """
    for key, value in settings.items():
        monkeypatch.setenv(key, value)
    
    importlib.reload(calculator_config)
    setup_logging()
    return calculator_config.config

def test_observer_update_before_calculation(monkeypatch, tmp_path, caplog):
    """
    Tests that observers don't log calculations before one has occurred.
    This covers the 'if not subject.last_calculation: return' lines.
    """
    # 1. Setup
    log_dir = tmp_path / "test_logs"
    history_dir = tmp_path / "test_history"
    config = setup_test_environment(monkeypatch, {
        'CALCULATOR_LOG_DIR': str(log_dir),
        'CALCULATOR_HISTORY_DIR': str(history_dir)
    })

    calculator = Calculator()
    logger = LoggingObserver(config)
    
    # 2. Action: Manually call the update method without a calculation
    caplog.clear() # Clear logs from app startup
    logger.update(calculator)

    # 3. Assert: Check that no new log records were captured by this action.
    assert len(caplog.records) == 0, "Logger should not produce a log if no calculation was performed."

def test_load_initial_history_empty_file(monkeypatch, tmp_path):
    """
    Tests that AutoSaveObserver handles an empty history file gracefully on init.
    This covers the `except pd.errors.EmptyDataError` block.
    """
    history_dir = tmp_path / "test_history"
    history_dir.mkdir()
    history_file = history_dir / "calculation_history.csv"
    history_file.touch() # Create an empty file

    config = setup_test_environment(monkeypatch, {
        'CALCULATOR_HISTORY_DIR': str(history_dir)
    })

    auto_saver = AutoSaveObserver(config)
    
    assert auto_saver.history == []

def test_load_initial_history_exception(monkeypatch, tmp_path):
    """
    Tests that AutoSaveObserver handles a generic error when reading the CSV.
    This covers the generic `except Exception` block by checking the log file.
    """
    # 1. Setup
    history_dir = tmp_path / "test_history"
    history_dir.mkdir()
    history_file = history_dir / "calculation_history.csv"
    history_file.touch()

    log_dir = tmp_path / "error_logs"
    log_filename = "error.log"

    config = setup_test_environment(monkeypatch, {
        'CALCULATOR_HISTORY_DIR': str(history_dir),
        'CALCULATOR_LOG_DIR': str(log_dir),
        'CALCULATOR_LOG_FILE': log_filename
    })

    #  Use monkeypatch to force pd.read_csv to raise an error.
    monkeypatch.setattr(pd, "read_csv", MagicMock(side_effect=Exception("Mocked pandas error")))

    # 2. Action: The exception is triggered during the observer's initialization
    auto_saver = AutoSaveObserver(config)

    # 3. Assert
    log_file = log_dir / log_filename
    assert auto_saver.history == []
    assert log_file.exists(), "Error log file should have been created."
    log_content = log_file.read_text()
    assert "Failed to load initial auto-save history" in log_content
    assert "Mocked pandas error" in log_content

def test_observers_respect_configured_paths(monkeypatch, tmp_path):
    """
    Tests if observers write files to the dynamically configured directories.
    """
    log_dir = tmp_path / "test_logs"
    history_dir = tmp_path / "test_history"
    log_filename = "test_run.log"
    
    config = setup_test_environment(monkeypatch, {
        'CALCULATOR_LOG_DIR': str(log_dir),
        'CALCULATOR_HISTORY_DIR': str(history_dir),
        'CALCULATOR_LOG_FILE': log_filename
    })
    
    calculator = Calculator()
    logger = LoggingObserver(config)
    auto_saver = AutoSaveObserver(config)
    
    calculator.register_observer(logger)
    calculator.register_observer(auto_saver)
    
    calculator.execute_operation('add', 10, 5)
    
    log_file = log_dir / log_filename
    history_file = history_dir / "calculation_history.csv"

    assert log_file.exists(), "Log file was not created in the configured directory."
    assert history_file.exists(), "History file was not created in the configured directory."

def test_autosave_observer_respects_false_setting(monkeypatch, tmp_path):
    """
    Tests that AutoSaveObserver does NOT write a file when auto-save is false.
    """
    history_dir = tmp_path / "test_history"
    
    config = setup_test_environment(monkeypatch, {
        'CALCULATOR_HISTORY_DIR': str(history_dir),
        'CALCULATOR_AUTO_SAVE': 'false'
    })

    calculator = Calculator()
    auto_saver = AutoSaveObserver(config)
    calculator.register_observer(auto_saver)
    
    calculator.execute_operation('multiply', 6, 7)
    
    history_file = history_dir / "calculation_history.csv"
    assert not history_file.exists()

def test_logging_respects_precision_setting(monkeypatch, tmp_path):
    """
    Tests that the LoggingObserver formats the result with correct precision.
    """
    log_dir = tmp_path / "test_logs"
    log_filename = "precision_test.log"
    
    config = setup_test_environment(monkeypatch, {
        'CALCULATOR_LOG_DIR': str(log_dir),
        'CALCULATOR_LOG_FILE': log_filename,
    })

    calculator = Calculator()
    logger = LoggingObserver(config)
    calculator.register_observer(logger)
    
    calculator.execute_operation('divide', 10, 3)
    
    log_file = log_dir / log_filename
    assert log_file.exists()
    
    log_content = log_file.read_text()
    assert "Result: 3.3333" in log_content

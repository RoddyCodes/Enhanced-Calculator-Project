import os
import importlib
import pytest
import pandas as pd
from app.calculator import Calculator
from app.logger import LoggingObserver, AutoSaveObserver
# Import the module so we can reload it
from app import calculator_config

def setup_test_environment(monkeypatch, settings):
    """
    A pytest helper function to set environment variables for a test
    and then reload the config module to apply the changes.
    """
    for key, value in settings.items():
        monkeypatch.setenv(key, value)
    
    importlib.reload(calculator_config)
    return calculator_config.config

def test_observer_update_before_calculation(monkeypatch, tmp_path):
    """
    Tests that observers handle being updated before any calculation has occurred.
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
    auto_saver = AutoSaveObserver(config)
    
    # 2. Action: Manually call the update method without a calculation
    # The calculator's last_calculation property is still None at this point.
    logger.update(calculator)
    auto_saver.update(calculator)

    # 3. Assert: No files should be created because the methods should exit early
    log_file = log_dir / "calculations.log"
    history_file = history_dir / "calculation_history.csv"
    assert not log_file.exists()
    assert not history_file.exists()

def test_observers_respect_configured_paths(monkeypatch, tmp_path):
    """
    Tests if observers write files to the dynamically configured directories.
    """
    log_dir = tmp_path / "test_logs"
    history_dir = tmp_path / "test_history"
    
    config = setup_test_environment(monkeypatch, {
        'CALCULATOR_LOG_DIR': str(log_dir),
        'CALCULATOR_HISTORY_DIR': str(history_dir)
    })
    
    calculator = Calculator()
    logger = LoggingObserver(config)
    auto_saver = AutoSaveObserver(config)
    
    calculator.register_observer(logger)
    calculator.register_observer(auto_saver)
    
    calculator.execute_operation('add', 10, 5)
    
    log_file = log_dir / "calculations.log"
    history_file = history_dir / "calculation_history.csv"

    assert log_file.exists(), "Log file was not created in the configured directory."
    assert history_file.exists(), "History file was not created in the configured directory."

def test_autosave_observer_respects_false_setting(monkeypatch, tmp_path):
    """
    Tests that the AutoSaveObserver does NOT write a file when
    CALCULATOR_AUTO_SAVE is configured to be 'false'.
    This covers the 'if not self.config.auto_save: return' line.
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
    assert not history_file.exists(), "History file should not have been created when auto-save is false."

def test_logging_respects_precision_setting(monkeypatch, tmp_path):
    """
    Tests that the LoggingObserver formats the calculation result using
    the precision specified in the configuration.
    """
    log_dir = tmp_path / "test_logs"
    log_file = log_dir / "calculations.log"
    
    config = setup_test_environment(monkeypatch, {
        'CALCULATOR_LOG_DIR': str(log_dir),
        'CALCULATOR_PRECISION': '4'
    })

    calculator = Calculator()
    logger = LoggingObserver(config)
    calculator.register_observer(logger)
    
    calculator.execute_operation('divide', 10, 3)
    
    assert log_file.exists()
    with open(log_file, 'r') as f:
        log_content = f.read()
        assert "Result: 3.3333" in log_content, "Log file did not respect the precision setting."

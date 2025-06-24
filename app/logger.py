import pandas as pd
from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING
import logging
import os 

if TYPE_CHECKING: # pragma: no cover
    from .calculator import Calculator 
    from .calculator_config import CalculatorConfig

class Observer(ABC):
    """The Observer interface declares the update method."""
    @abstractmethod
    def update(self, subject: 'Calculator') -> None:
        pass # pragma: no cover

class LoggingObserver(Observer):
    """Logs calculation details using Python's logging module."""
    def __init__(self, config: 'CalculatorConfig'):
        self.config = config

    def update(self, subject: 'Calculator') -> None:
        """Pulls the last calculation and logs it as an info message."""
        if not subject.last_calculation:
            return 

        calc = subject.last_calculation
        
        log_message = (
            f"Calculation - "
            f"Operation: {calc.operation.__class__.__name__}, "
            f"Operands: {(calc.a, calc.b)}, "
            f"Result: {calc.result}"
        )
        logging.info(log_message)

class AutoSaveObserver(Observer):
    """Saves the calculation history, respecting the auto-save setting."""
    def __init__(self, config: 'CalculatorConfig'):
        """Initializes the observer and loads existing history."""
        self.config = config
        self.output_file = config.get_history_file_path()
        self.history = []
        # FIX: Load the history from the file if it exists upon initialization.
        self._load_initial_history()

    def _load_initial_history(self):
        """Loads the auto-save history file at the start of the application."""
        if os.path.exists(self.output_file):
            try:
                df = pd.read_csv(self.output_file)
                # Convert the DataFrame back into the list of dictionaries format.
                self.history = df.to_dict('records')
            except pd.errors.EmptyDataError:
                # If the file is empty, just start with an empty history.
                self.history = []
            except Exception as e:
                logging.error(f"Failed to load initial auto-save history: {e}")
                self.history = []


    def update(self, subject: 'Calculator') -> None:
        """Appends the last calculation and saves if auto-save is enabled."""
        if not self.config.auto_save:
            return

        if not subject.last_calculation:
            return #pragma: no cover

        calc = subject.last_calculation
        self.history.append({
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Operation": calc.operation.__class__.__name__,
            "Operand_A": calc.a,
            "Operand_B": calc.b,
            "Result": calc.result
        })

        try:
            df = pd.DataFrame(self.history)
            df.to_csv(self.output_file, index=False, encoding=self.config.encoding)
        except Exception as e: #pragma: no cover
            logging.error(f"Failed to auto-save history: {e}", exc_info=True)

import pandas as pd
from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING

# This block only runs during static type checking, which avoids the runtime error.
if TYPE_CHECKING: #pragma: no cover
    from .calculator import Calculator 
    from .calculator_config import CalculatorConfig

class Observer(ABC):
    """The Observer interface declares the update method."""
    @abstractmethod
    def update(self, subject: 'Calculator') -> None:
        pass # pragma: no cover

class LoggingObserver(Observer):
    """Logs calculation details to a file specified in the configuration."""
    def __init__(self, config: 'CalculatorConfig'):
        """Initializes the observer with a specific configuration object."""
        self.config = config
        self.log_file = self.config.get_log_file_path()

    def update(self, subject: 'Calculator') -> None:
        """Pulls the last calculation from the calculator and logs it."""
        if not subject.last_calculation:
            return 

        calc = subject.last_calculation
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        result_str = f"{calc.result:.{self.config.precision}f}"
        log_entry = (
            f"[{timestamp}] "
            f"Operation: {calc.operation.__class__.__name__}, "
            f"Operands: {(calc.a, calc.b)}, "
            f"Result: {result_str}\n"
        )
        
        try:
            with open(self.log_file, 'a', encoding=self.config.encoding) as f:
                f.write(log_entry)
        except IOError as e: #pragma: no cover
            print(f"Error: Could not write to log file {self.log_file}. {e}") # pragma: no cover

class AutoSaveObserver(Observer):
    """Saves the calculation history, respecting the auto-save setting."""
    def __init__(self, config: 'CalculatorConfig'):
        """Initializes the observer with a specific configuration object."""
        self.config = config
        self.output_file = self.config.get_history_file_path()
        self.history = []

    def update(self, subject: 'Calculator') -> None:
        """Appends the last calculation and saves if auto-save is enabled."""
        if not self.config.auto_save:
            return

        if not subject.last_calculation:
            return

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
            print(f"Error: Could not save history to {self.output_file}. {e}") # pragma: no cover

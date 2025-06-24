import os
import logging
from dotenv import load_dotenv

def setup_logging():
    """Configures the application-wide logger based on the current config."""
    # Get the singleton config instance defined at the bottom of this file
    config = CalculatorConfig()
    
    # Configure the root logger.
    # `force=True` is crucial for pytest, as it allows re-configuring the logger for each test run.
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=config.get_log_file_path(),  # Use the path from the config
        filemode='a',
        force=True
    )

class CalculatorConfig:
    """
    Manages loading and accessing application configuration from .env file.
    """
    def __init__(self):
        load_dotenv()

        self.log_dir = os.getenv('CALCULATOR_LOG_DIR', 'logs')
        self.history_dir = os.getenv('CALCULATOR_HISTORY_DIR', 'history')

        self.log_file_name = os.getenv('CALCULATOR_LOG_FILE', 'app.log')

        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(self.history_dir, exist_ok=True)

        self.max_history_size = int(os.getenv('CALCULATOR_MAX_HISTORY_SIZE', 100))
        self.auto_save = os.getenv('CALCULATOR_AUTO_SAVE', 'true').lower() in ('true', '1', 't')
        
        self.precision = int(os.getenv('CALCULATOR_PRECISION', 4))
        self.max_input_value = float(os.getenv('CALCULATOR_MAX_INPUT_VALUE', 1e9))
        self.encoding = os.getenv('CALCULATOR_DEFAULT_ENCODING', 'utf-8')

    def get_log_file_path(self) -> str:
        """Constructs the full path for the configured log file."""
        return os.path.join(self.log_dir, self.log_file_name)

    def get_history_file_path(self, filename: str = 'calculation_history.csv') -> str:
        """Constructs the full path for a history file."""
        return os.path.join(self.history_dir, filename)

# Create a single instance of the config to be imported by other modules
config = CalculatorConfig()

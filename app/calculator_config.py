import os
from dotenv import load_dotenv

class CalculatorConfig:
    """
    Manages loading and accessing application configuration from .env file.
    Provides default values for settings if they are not defined.
    """
    def __init__(self):
        # Load environment variables from .env file in the project root
        load_dotenv()

        # -- Directory and File Settings --
        self.log_dir = os.getenv('CALCULATOR_LOG_DIR', 'logs')
        self.history_dir = os.getenv('CALCULATOR_HISTORY_DIR', 'history')
        # Read the log filename from the environment, with a default value
        self.log_file_name = os.getenv('CALCULATOR_LOG_FILE', 'calculations.log')

        # Create directories if they don't exist
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(self.history_dir, exist_ok=True)

        # -- History Settings --
        # Getenv returns a string, so we must cast it to an integer.
        self.max_history_size = int(os.getenv('CALCULATOR_MAX_HISTORY_SIZE', 100))
        # Handle boolean conversion for auto-save
        self.auto_save = os.getenv('CALCULATOR_AUTO_SAVE', 'true').lower() in ('true', '1', 't')
        
        # -- Calculation Settings --
        self.precision = int(os.getenv('CALCULATOR_PRECISION', 4))
        self.max_input_value = float(os.getenv('CALCULATOR_MAX_INPUT_VALUE', 1e9))
        self.encoding = os.getenv('CALCULATOR_DEFAULT_ENCODING', 'utf-8')

    def get_log_file_path(self) -> str:
        """Constructs the full path for the configured log file."""
        # Use the configured log file name
        return os.path.join(self.log_dir, self.log_file_name)

    def get_history_file_path(self, filename: str = 'calculation_history.csv') -> str:
        """Constructs the full path for a history file."""
        return os.path.join(self.history_dir, filename)

# Create a single instance of the config to be imported by other modules
# This makes it a singleton, ensuring settings are loaded only once.
config = CalculatorConfig()

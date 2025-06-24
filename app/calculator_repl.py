
import sys
import pandas as pd
import ast
from datetime import datetime
import logging
from colorama import Fore, Style, init
from app.calculator import Calculator
from app.logger import LoggingObserver, AutoSaveObserver
from app.calculator_config import config, setup_logging
from app.operations import OperationFactory
from app.calculation import Calculation
from app.exceptions import OperationError, ValidationError
from app.input_validators import validate_operands

# Initialize colorama once when the module is imported.
init(autoreset=True)

class App:
    def __init__(self):
        """Initializes the REPL, sets up logging, and registers observers."""
        setup_logging()
        
        self.calculator = Calculator()
        self.history = []
        
        self.logger = LoggingObserver(config)
        self.auto_saver = AutoSaveObserver(config)
        
        self.calculator.register_observer(self.logger)
        self.calculator.register_observer(self.auto_saver)
        
        self.calculation_commands = {'add', 'subtract', 'multiply', 'divide', 'power', 'root', 'modulus', 'int_divide', 'percent', 'abs_diff'}

        self.commands = {
            "exit": self._exit_app, "help": self._show_help, "history": self._display_history,
            "clear": self._clear_history, "undo": self._undo_calculation, "redo": self._redo_calculation,
            "save": self._save_history, "load": self._load_history,
        }

    def start(self):
        """Starts the read-eval-print loop (REPL) for the calculator."""
        logging.info("Application started.")
        print(f"{Fore.CYAN}{Style.BRIGHT}Welcome to the Enhanced Calculator!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Type 'help' for available commands or 'exit' to quit.{Style.RESET_ALL}")
        while True:
            try:
                user_input = input(f"{Fore.YELLOW}>>> {Style.RESET_ALL}").strip()
                if not user_input:
                    continue
                parts = user_input.split()
                command_name = parts[0].lower()
                args = parts[1:]
                if command_name in self.commands:
                    self.commands[command_name](args)
                elif command_name in self.calculation_commands:
                    self._perform_calculation(command_name, args)
                else:
                    logging.warning(f"Unknown command entered: '{command_name}'")
                    print(f"{Fore.RED}Unknown command: '{command_name}'{Style.RESET_ALL}")
            except KeyboardInterrupt:
                self._exit_app()
            except Exception as e:
                logging.error(f"An unexpected error occurred in the main loop: {e}", exc_info=True)
                print(f"{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}")

    def _perform_calculation(self, command_name, args):
        """Validates input, performs calculation, and handles its own errors."""
        try:
            a, b = validate_operands(args)
            calculation = self.calculator.execute_operation(command_name, a, b)
            self.history.append(calculation)
            print(f"{Fore.GREEN}Result: {calculation.result}{Style.RESET_ALL}")
        except (ValidationError, OperationError) as e:
            logging.error(f"Failed to perform calculation '{command_name}' with args {args}: {e}")
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        except Exception as e:
            logging.error(f"An unexpected calculation error occurred: {e}", exc_info=True)
            print(f"{Fore.RED}An unexpected error occurred during calculation: {e}{Style.RESET_ALL}")

    def _display_history(self, args=None):
        if not self.history:
            print(f"{Fore.YELLOW}No history to display.{Style.RESET_ALL}")
            return
        print(f"\n{Style.BRIGHT}Calculation History:{Style.RESET_ALL}")
        for calc in self.history:
            print(f"  - {calc}")

    def _clear_history(self, args=None):
        self.history.clear()
        logging.info("Calculation history cleared.")
        print(f"{Fore.YELLOW}History cleared.{Style.RESET_ALL}")

    def _undo_calculation(self, args=None):
        if self.history:
            self.calculator.undo()
            self.history.pop()
        else:
            print(f"{Fore.YELLOW}No operation to undo.{Style.RESET_ALL}")

    def _redo_calculation(self, args=None):
        self.calculator.redo()
    
    def _save_history(self, args=None):
        if not self.history:
            print(f"{Fore.YELLOW}History is empty. Nothing to save.{Style.RESET_ALL}") #pragma: no cover
            return #pragma: no cover
        file_path = config.get_history_file_path("manual_history.csv")
        history_data = [{"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Operation": calc.operation.__class__.__name__, "Operands": (calc.a, calc.b), "Result": calc.result} for calc in self.history]
        try:
            df = pd.DataFrame(history_data)
            df.to_csv(file_path, index=False)
            logging.info(f"History successfully saved to {file_path}")
            print(f"{Fore.GREEN}History successfully saved to {file_path}{Style.RESET_ALL}")
        except Exception as e:
            logging.error(f"Failed to save history: {e}", exc_info=True)
            print(f"{Fore.RED}Error saving history: {e}{Style.RESET_ALL}")

    def _load_history(self, args=None):
        file_path = config.get_history_file_path("manual_history.csv")
        try:
            df = pd.read_csv(file_path)
            self.history.clear()
            for index, row in df.iterrows():
                op_instance = OperationFactory.create_operation(row['Operation'].replace('Operation', '').lower())
                operands_tuple = ast.literal_eval(row['Operands'])
                a, b = operands_tuple
                calc = Calculation(a, b, op_instance, row['Result'])
                self.history.append(calc)
            logging.info(f"History successfully loaded from {file_path}")
            print(f"{Fore.GREEN}History successfully loaded from {file_path}{Style.RESET_ALL}")
            self._display_history()
        except FileNotFoundError:
            logging.warning(f"Load history failed: file not found at {file_path}") #pragma: no cover
            print(f"{Fore.RED}Error: History file not found at {file_path}{Style.RESET_ALL}") #pragma: no cover
        except Exception as e:
            logging.error(f"Failed to load history: {e}", exc_info=True)
            print(f"{Fore.RED}Error loading history: {e}{Style.RESET_ALL}")
    
    def _exit_app(self, args=None):
        logging.info("Application exiting.")
        print(f"{Fore.CYAN}Exiting Calculator. Goodbye!{Style.RESET_ALL}")
        sys.exit(0)

    def _show_help(self, args=None): 
        print(f"\n{Style.BRIGHT}Available Commands:{Style.RESET_ALL}") #pragma: no cover
        print(f"  - {Fore.YELLOW}add/subtract/multiply/divide... <num1> <num2>{Style.RESET_ALL}") #pragma: no cover
        print(f"  - {Fore.YELLOW}history{Style.RESET_ALL}       : Display the calculation history for this session.") #pragma: no cover
        print(f"  - {Fore.YELLOW}clear{Style.RESET_ALL}         : Clear the session history.") #pragma: no cover
        print(f"  - {Fore.YELLOW}undo / redo{Style.RESET_ALL}   : Undo or redo the last calculation.") #pragma: no cover
        print(f"  - {Fore.YELLOW}save / load{Style.RESET_ALL}   : Manually save or load the session history.") #pragma: no cover
        print(f"  - {Fore.YELLOW}help{Style.RESET_ALL}          : Show this help message.") #pragma: no cover
        print(f"  - {Fore.YELLOW}exit{Style.RESET_ALL}          : Exit the application.") #pragma: no cover

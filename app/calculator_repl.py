# app/calculator_repl.py

import sys
import pandas as pd
import ast # Used for safely evaluating string representations of data structures
from datetime import datetime 
from app.calculator import Calculator
from app.logger import LoggingObserver, AutoSaveObserver
from app.calculator_config import config
from app.operations import OperationFactory
from app.calculation import Calculation

class App:
    def __init__(self):
        """Initializes the REPL application, calculator, and observers."""
        self.calculator = Calculator()
        self.history = [] # To store Calculation objects
        
        self.logger = LoggingObserver(config)
        self.auto_saver = AutoSaveObserver(config)
        
        self.calculator.register_observer(self.logger)
        self.calculator.register_observer(self.auto_saver)
        
        self.calculation_commands = {'add', 'subtract', 'multiply', 'divide', 'power', 'root', 'modulus', 'int_divide', 'percent', 'abs_diff'}

        self.commands = {
            "exit": self._exit_app,
            "help": self._show_help,
            "history": self._display_history,
            "clear": self._clear_history,
            "undo": self._undo_calculation,
            "redo": self._redo_calculation,
            "save": self._save_history,
            "load": self._load_history,
        }

    def start(self):
        """Starts the read-eval-print loop (REPL) for the calculator."""
        print("Welcome to the Enhanced Calculator!")
        print("Type 'help' for available commands or 'exit' to quit.")

        while True:
            try:
                user_input = input(">>> ").strip()
                if not user_input:
                    continue

                parts = user_input.split()
                command_name = parts[0].lower()
                args = parts[1:]

                if command_name in self.commands:
                    self.commands[command_name](args)
                elif command_name in self.calculation_commands:
                    self._perform_calculation(command_name, args) #pragma: no cover
                else:
                    print(f"Unknown command: '{command_name}'")

            except KeyboardInterrupt:
                self._exit_app()
            except Exception as e:
                print(f"An error occurred: {e}") #pragma: no cover

    def _perform_calculation(self, command_name, args):
        """Handles all calculation commands."""
        if len(args) != 2:
            print(f"Error: {command_name} requires exactly two numerical arguments.")
            return
        
        try:
            a, b = map(float, args)
            calculation = self.calculator.execute_operation(command_name, a, b)
            self.history.append(calculation)
            print(f"Result: {calculation.result}")

        except ValueError as e:
            print(f"Error: Invalid input or operation. {e}")
        except Exception as e:
            print(f"An unexpected error occurred during calculation: {e}")

    def _display_history(self, args=None):
        """Displays the current session's calculation history."""
        if not self.history:
            print("No history to display.")
            return
        print("\nCalculation History:")
        for calc in self.history:
            print(f"  - {calc}")

    def _clear_history(self, args=None):
        """Clears the current session's history."""
        self.history.clear()
        print("History cleared.")

    def _undo_calculation(self, args=None):
        """Undoes the last calculation."""
        if self.history:
            self.calculator.undo()
            self.history.pop()
        else:
            print("No operation to undo.")

    def _redo_calculation(self, args=None):
        """Redoes the last undone calculation."""
        self.calculator.redo()
    
    def _save_history(self, args=None):
        """Manually saves the current session history to a CSV file."""
        if not self.history:
            print("History is empty. Nothing to save.")
            return

        file_path = config.get_history_file_path("manual_history.csv")
        # Prepare data according to the requirement: operation, operands, result, timestamp
        history_data = [
            {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Operation": calc.operation.__class__.__name__,
                "Operands": (calc.a, calc.b), # Store operands as a tuple
                "Result": calc.result
            } for calc in self.history
        ]
        
        try:
            df = pd.DataFrame(history_data)
            df.to_csv(file_path, index=False)
            print(f"History successfully saved to {file_path}")
        except Exception as e:
            print(f"Error saving history: {e}")

    def _load_history(self, args=None):
        """Loads calculation history from a CSV file."""
        file_path = config.get_history_file_path("manual_history.csv")
        try:
            df = pd.read_csv(file_path)
            self.history.clear()
            for index, row in df.iterrows():
                op_name_class = row['Operation']
                op_name_str = op_name_class.replace('Operation', '').lower()
                op_instance = OperationFactory.create_operation(op_name_str)

                # Safely parse the 'Operands' string back into a tuple
                operands_tuple = ast.literal_eval(row['Operands'])
                a, b = operands_tuple

                calc = Calculation(a, b, op_instance, row['Result'])
                self.history.append(calc)
            
            print(f"History successfully loaded from {file_path}")
            self._display_history()

        except FileNotFoundError:
            print(f"Error: History file not found at {file_path}")
        except Exception as e:
            print(f"Error loading history: {e}")

    def _exit_app(self, args=None):
        """Gracefully exits the application."""
        print("Exiting Calculator. Goodbye!")
        sys.exit(0)

    def _show_help(self, args=None):
        """Displays the help message with available commands."""
        print("\nAvailable Commands:")
        print("  - add/subtract/multiply/divide... <num1> <num2>")
        print("  - history       : Display the calculation history for this session.")
        print("  - clear         : Clear the session history.")
        print("  - undo / redo   : Undo or redo the last calculation.")
        print("  - save / load   : Manually save or load the session history.")
        print("  - help          : Show this help message.")
        print("  - exit          : Exit the application.")

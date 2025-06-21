# app/calculator.py

from app.operations import OperationFactory
from app.calculation import Calculation
from app.history import HistoryManager
from app.calculator_memento import CalculatorMemento

class Calculator:
    """The main calculator class that performs operations."""

    def __init__(self):
        """Initializes the calculator."""
        # --- Add these new properties ---
        self._current_result = 0.0
        self._history_manager = HistoryManager()
        # Save the initial state
        self._history_manager.save(self.create_memento())

    # --- Add this new method to create a memento ---
    def create_memento(self) -> CalculatorMemento:
        """Creates a memento of the current result."""
        return CalculatorMemento(self._current_result)

    # --- Add this new method to restore from a memento ---
    def restore_from_memento(self, memento: CalculatorMemento | None):
        """Restores the calculator's state from a memento."""
        if memento:
            self._current_result = memento.get_state()
        else:
            # If no memento, reset to initial state
            self._current_result = 0.0
        print(f"State restored. Current result is: {self._current_result}")


    def execute_operation(self, operation_name: str, a: float, b: float) -> Calculation:
        """Executes a calculation by creating the appropriate operation."""
        try:
            operation = OperationFactory.create_operation(operation_name)
            self._current_result = operation.calculate(a, b)
            
            # --- After a successful calculation, save the state ---
            self._history_manager.save(self.create_memento())
            
            calculation = Calculation(a, b, operation, self._current_result)
            return calculation
            
        except ValueError as e:
            print(f"Error: {e}")
            raise
    
    # --- Add the new undo and redo methods ---
    def undo(self):
        """Undoes the last operation."""
        print("Undoing last operation...")
        memento = self._history_manager.undo()
        self.restore_from_memento(memento)

    def redo(self):
        """Redoes the last undone operation."""
        print("Redoing last operation...")
        memento = self._history_manager.redo()
        if memento:
             self.restore_from_memento(memento)
        else:
            print("Nothing to redo.")


# --- Example Usage (for testing purposes) ---
if __name__ == '__main__': #pragma: no cover
    calc = Calculator()
    
    # Perform some calculations
    calc.execute_operation('add', 10, 5)      # Result: 15
    print(f"Current result: {calc._current_result}")
    calc.execute_operation('subtract', 15, 3)  # Result: 12
    print(f"Current result: {calc._current_result}")
    
    # Undo the last operation
    calc.undo() # Should restore state to 15
    
    # Undo again
    calc.undo() # Should restore state to 0 (initial state)
    
    # Redo an operation
    calc.redo() # Should restore state to 15
    
    # Redo again
    calc.redo() # Should restore state to 12
    
    # Try to redo again (should do nothing)
    calc.redo()

from typing import List, Any, TYPE_CHECKING
from app.operations import OperationFactory
from app.calculation import Calculation
from app.history import HistoryManager
from app.calculator_memento import CalculatorMemento

# This block only runs during static type checking, not at runtime.
# This breaks the circular import.
if TYPE_CHECKING:
    from app.logger import Observer #pragma: no cover

class Calculator:
    """
    The main calculator class that performs operations.
    It acts as the 'Subject' in the Observer pattern and the 'Originator'
    in the Memento pattern.
    """

    _observers: List['Observer'] = []
    last_calculation: Calculation | None = None

    def __init__(self):
        """Initializes the calculator."""
        self._current_result = 0.0
        self._history_manager = HistoryManager()
        self._history_manager.save(self.create_memento())

    # --- Observer Pattern Methods ---
    def register_observer(self, observer: 'Observer') -> None:
        """Adds an observer to the list."""
        print(f"Registered observer: {observer.__class__.__name__}")
        self._observers.append(observer)

    def unregister_observer(self, observer: 'Observer') -> None:
        """Removes an observer from the list."""
        try:
            self._observers.remove(observer)
            print(f"Unregistered observer: {observer.__class__.__name__}")
        except ValueError:
            print(f"Observer {observer.__class__.__name__} not found.") # pragma: no cover

    def _notify_observers(self) -> None:
        """Notifies all registered observers by calling their update method."""
        print("Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    # --- Memento Pattern Methods ---
    def create_memento(self) -> CalculatorMemento:
        """Creates a memento of the current result."""
        return CalculatorMemento(self._current_result)

    def restore_from_memento(self, memento: CalculatorMemento | None):
        """Restores the calculator's state from a memento."""
        if memento:
            self._current_result = memento.get_state()
        else:
            self._current_result = 0.0
        print(f"State restored. Current result is: {self._current_result}")

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

    # --- Core Execution Method ---
    def execute_operation(self, operation_name: str, a: float, b: float) -> Calculation:
        """Executes a calculation, updates state, and notifies observers."""
        try:
            operation = OperationFactory.create_operation(operation_name)
            self._current_result = operation.calculate(a, b)
            
            self._history_manager.save(self.create_memento())
            calculation = Calculation(a, b, operation, self._current_result)
            
            self.last_calculation = calculation
            self._notify_observers()
            
            return calculation
            
        except ValueError as e:
            print(f"Error: {e}") #pragma: no cover
            raise #pragma: no cover

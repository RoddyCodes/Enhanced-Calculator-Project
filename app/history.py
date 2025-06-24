
from app.calculator_memento import CalculatorMemento

class HistoryManager:
    """The Caretaker, responsible for managing undo/redo history."""
    
    def __init__(self):
        self._history: list[CalculatorMemento] = []
        self._redo_stack: list[CalculatorMemento] = []

    def save(self, memento: CalculatorMemento):
        """Saves a new state to the history."""
        self._history.append(memento)
        # When a new action is taken, the redo stack should be cleared.
        self._redo_stack.clear()

    def undo(self) -> CalculatorMemento | None:
        """
        Moves the most recent history item to the redo stack and returns
        the state to revert to (the second to last state).
        """
        if len(self._history) < 2:
            # Can't undo if there's only the initial state or it's empty
            return None
        
        # Pop the current state and move it to the redo stack.
        last_memento = self._history.pop()
        self._redo_stack.append(last_memento)
        
        # Return the previous state to restore the calculator.
        return self._history[-1]

    def redo(self) -> CalculatorMemento | None:
        """Moves an item from the redo stack back to the history."""
        if not self._redo_stack:
            return None
            
        # Pop from redo and move it back to the main history.
        memento_to_restore = self._redo_stack.pop()
        self._history.append(memento_to_restore)
        
        return memento_to_restore
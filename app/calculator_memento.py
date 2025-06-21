# app/calculator_memento.py

class CalculatorMemento:
    """The Memento object that stores the state of the calculator's result."""
    
    def __init__(self, state: float):
        # We make the state "private" to protect it from outside changes.
        self._state = state

    def get_state(self) -> float:
        """Provides a way to retrieve the stored state."""
        return self._state
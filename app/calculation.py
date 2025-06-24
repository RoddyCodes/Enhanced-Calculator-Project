
from app.operations import Operation

class Calculation:
    """A simple class to hold the data for a single calculation."""
    
    def __init__(self, a: float, b: float, operation: Operation, result: float):
        self.a = a
        self.b = b
        self.operation = operation
        self.result = result

    def __str__(self):
        """Provides a user-friendly string representation of the calculation."""
        # Get the operation name from the class name (e.g., Add -> 'add')
        op_name = self.operation.__class__.__name__.lower()
        return f"{self.a} {op_name} {self.b} = {self.result}"
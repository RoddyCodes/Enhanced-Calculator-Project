# app/exceptions.py

class CalculatorError(Exception):
    """Base exception class for all calculator-related errors."""
    pass

class OperationError(CalculatorError):
    """Raised for errors related to arithmetic operations (e.g., division by zero)."""
    pass

class ValidationError(CalculatorError):
    """Raised for errors related to invalid user input."""
    pass

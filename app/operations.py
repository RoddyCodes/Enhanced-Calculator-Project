import math
from abc import ABC, abstractmethod

#base class for all arithmetic operations
class Operation(ABC):
    @abstractmethod

    def calculate(self, a, b):
        """
        performs the calculation
        Args: 
            a(float)
            b(float)
        Returns:
            result(float)
        """

    pass

class Add(Operation):
    """
    performs the addition arithmetic operation

    """
    def calculate(self, a,b):
        return a+b
    
class Subtract(Operation):
    """
    performs the subtraction arithmetic operation

    """
    def calculate(self, a,b):
        return a-b
    
class Multiply(Operation):
    """
    performs the multiplication arithmetic operation

    """
    def calculate(self, a,b):
        return a*b
    
class Divide(Operation):
    """
    performs the division arithmetic operation

    """
    def calculate(self, a,b):
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a/b
    
class Power(Operation):
    """
    performs the Power arithmetic operation

    """
    def calculate(self, a,b):
        return a**b
    

class Root(Operation):
    """
    performs the Root arithmetic operation

    """
    def calculate(self, a,b):
        if a < 0 and b%2 ==0:
            raise ValueError("Cannot take an even root of a negative number.")
        return a ** (1/b)
    
class Modulus(Operation):
    """
    performs the modulus arithmetic operation

    """
    def calculate(self, a,b):
        if b ==0:
            raise ValueError("Cannot perform modulus with zero.")
        return a%b
    
class IntegerDivide(Operation):
    """
    performs the integer divide arithmetic operation

    """
    def calculate(self, a,b):
        return a // b
    
class Percentage(Operation):
    """
    performs the percentage arithmetic operation

    """
    def calculate(self, a,b):
        return (a/b) * 100
    
class AbsoluteDifference(Operation):
    """
    performs the absolute difference arithmetic operation

    """
    def calculate(self, a,b):
        return abs(a-b)
    
# Factory Class

class OperationFactory:
    """
    factory creates operation objects
    """

    # A mapping from operation names (strings) to operation classes
    _operations = {
        'add': Add,
        'subtract': Subtract,
        'multiply': Multiply,
        'divide': Divide,
        'power': Power,
        'root': Root,
        'modulus': Modulus,
        'int_divide': IntegerDivide,
        'percent': Percentage,
        'abs_diff': AbsoluteDifference
    }

    @staticmethod
    def create_operation(operation_name: str) -> Operation:
        """
        create instance of operation class based on name

        Args:
            operation_name (str): The name of the operation (e.g., 'add').
        
        Returns:
            Operation: An instance of the corresponding operation class.
        
        Raises:
            ValueError: If the operation_name is not recognized.
        
        """
        operation_class = OperationFactory._operations.get(operation_name.lower())
        if not operation_class:
            raise ValueError(f"Unknown operation: {operation_name}")
        return operation_class()
    


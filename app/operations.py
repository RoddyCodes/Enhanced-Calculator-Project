import math
from abc import ABC, abstractmethod

from app.exceptions import OperationError, CalculatorError, ValidationError

class Operation(ABC):
    @abstractmethod
    def calculate(self, a, b):
        pass # pragma: no cover

class Add(Operation):
    def calculate(self, a,b):
        return a+b
    
class Subtract(Operation):
    def calculate(self, a,b):
        return a-b
    
class Multiply(Operation):
    def calculate(self, a,b):
        return a*b
    
class Divide(Operation):
    def calculate(self, a,b):
        if b == 0:
            # Raise the specific OperationError
            raise OperationError("Cannot divide by zero.")
        return a/b
    
class Power(Operation):
    def calculate(self, a,b):
        return a**b #pragma: no cover
    
class Root(Operation):
    def calculate(self, a,b):
        if a < 0 and b % 2 == 0:
            raise OperationError("Cannot take an even root of a negative number.")
        return a ** (1/b)
    
class Modulus(Operation):
    def calculate(self, a,b):
        if b == 0:
            raise OperationError("Cannot perform modulus with zero.")
        return a%b
    
class IntegerDivide(Operation):
    def calculate(self, a,b):
        if b == 0:
            raise OperationError("Cannot perform integer division by zero.")
        return a // b
    
class Percentage(Operation):
    def calculate(self, a,b):
        if b == 0:
            raise OperationError("Cannot calculate percentage with zero as the denominator.")
        return (a/b) * 100
    
class AbsoluteDifference(Operation):
    def calculate(self, a,b):
        return abs(a-b)
    
class OperationFactory:
    _operations = {
        'add': Add, 'subtract': Subtract, 'multiply': Multiply, 'divide': Divide,
        'power': Power, 'root': Root, 'modulus': Modulus, 'int_divide': IntegerDivide,
        'percent': Percentage, 'abs_diff': AbsoluteDifference
    }

    @staticmethod
    def create_operation(operation_name: str) -> Operation:
        operation_class = OperationFactory._operations.get(operation_name.lower())
        if not operation_class:
            # Raise the specific OperationError
            raise OperationError(f"Unknown operation: {operation_name}")
        return operation_class()

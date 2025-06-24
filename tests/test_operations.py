
import pytest
from app.operations import (
    Add, Subtract, Multiply, Divide, Power, Root, Modulus, IntegerDivide,
    Percentage, AbsoluteDifference, OperationFactory
)
# Import your custom exception
from app.exceptions import OperationError

# --- Standard Operation Tests ---

@pytest.mark.parametrize("a, b, expected", [
    (10, 5, 15), (-1, 1, 0), (2.5, -2.5, 0)
])
def test_add_operation(a, b, expected):
    """Test the Add operation."""
    assert Add().calculate(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
    (10, 5, 5), (5, 10, -5), (-5, -5, 0)
])
def test_subtract_operation(a, b, expected):
    """Test the Subtract operation."""
    assert Subtract().calculate(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
    (3, 4, 12), (-2, 5, -10), (5, 0, 0)
])
def test_multiply_operation(a, b, expected):
    """Test the Multiply operation."""
    assert Multiply().calculate(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
    (27, 3, 3.0), (16, 2, 4.0), (16, 4, 2.0)
])
def test_root_operation(a, b, expected):
    """Test the Root operation's happy path."""
    assert Root().calculate(a, b) == pytest.approx(expected)

@pytest.mark.parametrize("a, b, expected", [
    (10, 3, 1), (10, 2, 0)
])
def test_modulus_operation(a, b, expected):
    """Test the Modulus operation's happy path."""
    assert Modulus().calculate(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
    (10, 15, 5), (-10, 10, 20), (5, 5, 0)
])
def test_absolute_difference_operation(a, b, expected):
    """Test the AbsoluteDifference operation."""
    assert AbsoluteDifference().calculate(a, b) == expected

def test_integer_divide_operation():
    """Test the IntegerDivide for a successful calculation."""
    assert IntegerDivide().calculate(10, 3) == 3

def test_percentage_operation():
    """Test the Percentage for a successful calculation."""
    assert Percentage().calculate(50, 200) == 25

# --- Tests with Error Handling ---

def test_divide_operation_error():
    """Test the Divide operation for division-by-zero."""
    with pytest.raises(OperationError, match="Cannot divide by zero."):
        Divide().calculate(10, 0)

def test_root_operation_error():
    """Test the Root operation for an even root of a negative number."""
    with pytest.raises(OperationError, match="Cannot take an even root of a negative number."):
        Root().calculate(-16, 2)

def test_modulus_operation_by_zero():
    """Test that Modulus raises an OperationError for division by zero."""
    with pytest.raises(OperationError, match="Cannot perform modulus with zero."):
        Modulus().calculate(10, 0)

def test_integer_divide_operation_error():
    """Test IntegerDivide for division-by-zero."""
    with pytest.raises(OperationError, match="Cannot perform integer division by zero."):
        IntegerDivide().calculate(10, 0)

def test_percentage_operation_error():
    """Test Percentage for division-by-zero."""
    with pytest.raises(OperationError, match="Cannot calculate percentage with zero as the denominator."):
        Percentage().calculate(50, 0)

def test_operation_factory_unknown():
    """Test that the factory raises an OperationError for an unknown operation."""
    with pytest.raises(OperationError, match="Unknown operation: bogus"):
        OperationFactory.create_operation("bogus")

# tests/test_operations.py

import pytest
from app.operations import (
    Add, Subtract, Multiply, Divide, Power, Root, Modulus, IntegerDivide,
    Percentage, AbsoluteDifference, OperationFactory
)

# Using @pytest.mark.parametrize allows us to test many different inputs
# with the same test function, which is clean and efficient.

@pytest.mark.parametrize("a, b, expected", [
    (10, 5, 15),      # Positive numbers
    (-1, 1, 0),       # Negative and positive
    (2.5, -2.5, 0),   # Floating point numbers
    (0, 0, 0)         # Zeros
])
def test_add_operation(a, b, expected):
    """Test the Add operation with various scenarios."""
    add_op = Add()
    assert add_op.calculate(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
    (10, 5, 5),
    (5, 10, -5),
    (-5, -5, 0)
])
def test_subtract_operation(a, b, expected):
    """Test the Subtract operation."""
    sub_op = Subtract()
    assert sub_op.calculate(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
    (3, 4, 12),
    (-2, 5, -10),
    (5, 0, 0)
])
def test_multiply_operation(a, b, expected):
    """Test the Multiply operation."""
    mult_op = Multiply()
    assert mult_op.calculate(a, b) == expected

def test_divide_operation():
    """Test the Divide operation, including the crucial division-by-zero error."""
    div_op = Divide()
    assert div_op.calculate(10, 2) == 5
    
    # Use pytest.raises as a context manager to assert that an error is thrown.
    # The 'match' parameter checks that the error message is correct.
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        div_op.calculate(10, 0)

@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 8),      # Basic power
    (10, 0, 1),     # Power of 0 is 1
    (4, 0.5, 2.0)   # Fractional exponent (square root)
])
def test_power_operation(a, b, expected):
    """Test the Power operation."""
    power_op = Power()
    assert power_op.calculate(a, b) == pytest.approx(expected)

@pytest.mark.parametrize("a, b, expected", [
    (27, 3, 3),     # Cubic root
    (16, 2, 4),     # Square root
    (16, 4, 2)      # 4th root
])
def test_root_operation(a, b, expected):
    """Test the Root operation."""
    root_op = Root()
    assert root_op.calculate(a, b) == pytest.approx(expected)

def test_root_operation_error():
    """Test the specific error case for Root (even root of a negative number)."""
    root_op = Root()
    with pytest.raises(ValueError, match="Cannot take an even root of a negative number."):
        root_op.calculate(-16, 2)

@pytest.mark.parametrize("a, b, expected", [
    (10, 3, 1),
    (10, 2, 0)
])
def test_modulus_operation(a, b, expected):
    """Test the Modulus operation."""
    mod_op = Modulus()
    assert mod_op.calculate(a, b) == expected
    
def test_modulus_operation_by_zero():
    """Test that the Modulus operation correctly raises a ValueError when b is zero."""
    mod_op = Modulus()
    with pytest.raises(ValueError, match="Cannot perform modulus with zero."):
        # This line will trigger the error and the test will pass because it's expected.
        mod_op.calculate(10, 0)

def test_integer_divide_operation():
    """Test the IntegerDivide operation."""
    int_div_op = IntegerDivide()
    assert int_div_op.calculate(10, 3) == 3

def test_percentage_operation():
    """Test the Percentage operation."""
    perc_op = Percentage()
    assert perc_op.calculate(50, 100) == 50

def test_absolute_difference_operation():
    """Test the AbsoluteDifference operation."""
    abs_diff_op = AbsoluteDifference()
    assert abs_diff_op.calculate(10, 15) == 5
    assert abs_diff_op.calculate(-10, 10) == 20

# --- Test the Factory Class ---

@pytest.mark.parametrize("op_name, expected_instance", [
    ("add", Add),
    ("subtract", Subtract),
    ("multiply", Multiply),
    ("divide", Divide)
])
def test_operation_factory_creation(op_name, expected_instance):
    """Test that the factory creates the correct type of operation instance."""
    operation_instance = OperationFactory.create_operation(op_name)
    assert isinstance(operation_instance, expected_instance)

def test_operation_factory_unknown():
    """Test that the factory raises a ValueError for an unknown operation."""
    with pytest.raises(ValueError, match="Unknown operation: bogus"):
        OperationFactory.create_operation("bogus")
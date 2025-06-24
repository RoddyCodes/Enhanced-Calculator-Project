
from app.calculation import Calculation
from app.operations import Add

def test_calculation_string_representation():
    """
    Tests the __str__ method of the Calculation class to ensure it formats
    the output string correctly.
    """
    # 1. Setup: Use the  'Add' class
    add_operation = Add()
    calculation = Calculation(10, 5, add_operation, 15)
    
    # 2. Action: Convert the calculation object to a string
    result_string = str(calculation)
    
    # 3. Assert: Check if the string matches the expected format.
    #  __str__ method uses .lower(), so 'Add' becomes 'add'.
    expected_string = "10 add 5 = 15"
    assert result_string == expected_string

def test_calculation_properties():
    """
    Tests that the Calculation class correctly stores its properties.
    This test ensures the __init__ method is working as expected.
    """
    # 1. Setup
    add_operation = Add()
    calculation = Calculation(20, 10, add_operation, 30)
    
    # 2. Assert
    assert calculation.a == 20
    assert calculation.b == 10
    assert isinstance(calculation.operation, Add)
    assert calculation.result == 30

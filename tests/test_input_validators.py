
import pytest
from app.input_validators import validate_operands
from app.exceptions import ValidationError
from app.calculator_config import config # Import the config singleton

def test_validate_operands_valid():
    """Tests that the validator returns correct float values for valid input."""
    operands = ['10.5', '-20']
    a, b = validate_operands(operands)
    assert a == 10.5
    assert b == -20.0

def test_validate_operands_too_large(monkeypatch):
    """
    Tests that the validator raises a ValidationError if inputs exceed the configured max value.
    """
    #  Directly patch the attribute on the imported config object.
    monkeypatch.setattr(config, 'max_input_value', 1000.0)
    
    with pytest.raises(ValidationError, match="Operands must be between -1000.0 and 1000.0."):
        validate_operands(['2000', '5'])

def test_validate_operands_not_numbers():
    """
    Tests that the validator raises a ValidationError for non-numeric inputs.
    """
    with pytest.raises(ValidationError, match="Both arguments must be valid numbers."):
        validate_operands(['ten', 'five'])

def test_validate_operands_wrong_count():
    """
    Tests that the validator raises a ValidationError for the wrong number of operands.
    """
    with pytest.raises(ValidationError, match="Exactly two numerical arguments are required."):
        validate_operands(['10'])

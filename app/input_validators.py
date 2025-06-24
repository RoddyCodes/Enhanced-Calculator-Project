
from app.exceptions import ValidationError
from app.calculator_config import config

def validate_operands(operands: list[str]) -> tuple[float, float]:
    """
    Validates that the input operands are valid numbers and within configured limits.

    Args:
        operands (list[str]): A list of string inputs from the user.

    Returns:
        tuple[float, float]: A tuple of the validated operands as floats.

    Raises:
        ValidationError: If the input is not valid.
    """
    if len(operands) != 2:
        raise ValidationError("Exactly two numerical arguments are required.")

    try:
        a = float(operands[0])
        b = float(operands[1])
    except ValueError:
        raise ValidationError("Both arguments must be valid numbers.")

    max_val = config.max_input_value
    if abs(a) > max_val or abs(b) > max_val:
        raise ValidationError(f"Operands must be between -{max_val} and {max_val}.")

    return a, b

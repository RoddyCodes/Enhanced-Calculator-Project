
import pytest
from app.calculator import Calculator

@pytest.fixture
def calculator_fixture():
    """
    This fixture creates a new Calculator instance for each test function.
    Using a fixture ensures that tests are isolated from each other.
    """
    return Calculator()

def test_initial_state(calculator_fixture):
    """Test that the calculator initializes with a result of 0."""
    assert calculator_fixture._current_result == 0.0

def test_execute_operation(calculator_fixture):
    """Test a single, basic calculation."""
    # Act: Perform an addition
    calc = calculator_fixture
    calculation = calc.execute_operation('add', 10, 5)
    
    # Assert: Check the result of the Calculation object and the calculator's internal state
    assert calculation.result == 15
    assert calc._current_result == 15

def test_undo_redo_sequence(calculator_fixture):
    """Test a full sequence of operations, undos, and redos."""
    # Arrange: Perform a series of calculations
    calc = calculator_fixture
    calc.execute_operation('add', 10, 5)      # Result: 15
    calc.execute_operation('subtract', 15, 3)  # Result: 12
    
    # Act & Assert: Undo operations
    calc.undo()
    assert calc._current_result == 15  # Assert state after first undo
    
    calc.undo()
    assert calc._current_result == 0.0   # Assert state after second undo (back to initial)
    
    # Act & Assert: Redo operations
    calc.redo()
    assert calc._current_result == 15  # Assert state after first redo
    
    calc.redo()
    assert calc._current_result == 12  # Assert state after second redo

def test_undo_at_beginning(calculator_fixture):
    """Test that calling undo at the start does nothing."""
    calc = calculator_fixture
    initial_state = calc._current_result
    
    calc.undo() # Try to undo
    
    assert calc._current_result == initial_state # The state should not change

def test_redo_without_undo(calculator_fixture):
    """Test that calling redo before an undo does nothing."""
    calc = calculator_fixture
    calc.execute_operation('add', 10, 5)
    initial_state = calc._current_result

    calc.redo() # Try to redo

    assert calc._current_result == initial_state # The state should not change

def test_redo_stack_clears_after_new_operation(calculator_fixture):
    """Test that the redo history is cleared when a new operation is performed."""
    # Arrange
    calc = calculator_fixture
    calc.execute_operation('add', 10, 5)  # Result: 15
    calc.execute_operation('add', 15, 5) # Result: 20
    
    # Act: Undo, then perform a new operation
    calc.undo()  # Back to 15. The redo stack now holds the state for 20.
    assert calc._current_result == 15
    
    calc.execute_operation('multiply', 10, 2) # New operation. Result: 20. This should clear the redo stack.
    assert calc._current_result == 20
    
    # Assert: Try to redo. It should do nothing.
    calc.redo()
    assert calc._current_result == 20 # The result should still be 20, not the old "redone" 20.

def test_execute_operation_error(calculator_fixture):
    """
    Test that execute_operation correctly handles and raises a ValueError.
    This test covers the 'except' block in the execute_operation method.
    """
    calc = calculator_fixture
    
    # Use pytest.raises to assert that a ValueError is raised
    # when we perform an invalid operation (division by zero).
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        calc.execute_operation('divide', 10, 0)

def test_unregister_observer(calculator_fixture):
    """
    Tests both successful and unsuccessful unregistering of an observer.
    This test will cover the full try...except block in unregister_observer.
    """
    # Create a dummy observer class just for this test
    class DummyObserver:
        def update(self, subject):
            pass

    observer_to_remove = DummyObserver()
    calculator = calculator_fixture

    # --- Test 1: Successful unregister ---
    calculator.register_observer(observer_to_remove)
    assert observer_to_remove in calculator._observers # Confirm it's there
    
    # This will execute the 'try' block
    calculator.unregister_observer(observer_to_remove)
    assert observer_to_remove not in calculator._observers # Confirm it's gone

    # --- Test 2: Unregistering an observer that doesn't exist ---
    # This will execute the 'except ValueError' block, giving you 100% coverage
    calculator.unregister_observer(observer_to_remove)
        

import pytest
from app.calculator import Calculator
from app.exceptions import OperationError

@pytest.fixture
def calculator_fixture():
    """Provides a new Calculator instance for each test."""
    return Calculator()

def test_initial_state(calculator_fixture):
    """Test that the calculator initializes with a result of 0."""
    assert calculator_fixture._current_result == 0.0

def test_execute_operation(calculator_fixture):
    """Test a single, basic calculation."""
    calc = calculator_fixture
    calculation = calc.execute_operation('add', 10, 5)
    
    assert calculation.result == 15
    assert calc._current_result == 15

def test_undo_redo_sequence(calculator_fixture):
    """Test a full sequence of operations, undos, and redos."""
    calc = calculator_fixture
    calc.execute_operation('add', 10, 5)
    calc.execute_operation('subtract', 15, 3)
    
    calc.undo()
    assert calc._current_result == 15
    
    calc.undo()
    assert calc._current_result == 0.0
    
    calc.redo()
    assert calc._current_result == 15
    
    calc.redo()
    assert calc._current_result == 12

def test_undo_at_beginning(calculator_fixture):
    """Test that calling undo at the start does nothing and returns None."""
    calc = calculator_fixture
    initial_state = calc._current_result
    # The undo method should return None when there's nothing to undo
    assert calc.undo() is None
    assert calc._current_result == initial_state

def test_redo_without_undo(calculator_fixture):
    """Test that calling redo before an undo does nothing and returns None."""
    calc = calculator_fixture
    calc.execute_operation('add', 10, 5)
    initial_state = calc._current_result
    # The redo method should return None when there's nothing to redo
    assert calc.redo() is None
    assert calc._current_result == initial_state

def test_redo_stack_clears_after_new_operation(calculator_fixture):
    """Test that the redo history is cleared when a new operation is performed."""
    calc = calculator_fixture
    calc.execute_operation('add', 10, 5)
    calc.execute_operation('add', 15, 5)
    
    calc.undo()
    assert calc._current_result == 15
    
    calc.execute_operation('multiply', 10, 2)
    assert calc._current_result == 20
    
    # Redo should do nothing now
    calc.redo()
    assert calc._current_result == 20

def test_execute_operation_error(calculator_fixture):
    """Test that execute_operation correctly raises an OperationError."""
    calc = calculator_fixture
    with pytest.raises(OperationError, match="Cannot divide by zero."):
        calc.execute_operation('divide', 10, 0)

def test_unregister_observer(calculator_fixture):
    """Tests both successful and unsuccessful unregistering of an observer."""
    class DummyObserver:
        def update(self, subject):
            pass

    observer_to_remove = DummyObserver()
    calculator = calculator_fixture

    calculator.register_observer(observer_to_remove)
    assert observer_to_remove in calculator._observers
    
    calculator.unregister_observer(observer_to_remove)
    assert observer_to_remove not in calculator._observers 
    # This call covers the 'except ValueError' path
    calculator.unregister_observer(observer_to_remove) 

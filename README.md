# Enhanced Calculator Application

## Project Description

This project is an advanced command-line calculator built with Python. It goes beyond basic arithmetic to include features that demonstrate robust software design and modern development practices. The application is built with a modular and extensible architecture, leveraging several key design patterns:

- **Factory Pattern**: Dynamically creates different arithmetic operation objects (_add_, _subtract_, _power_, etc.) without exposing the creation logic to the client.
- **Memento Pattern**: Manages the calculator's state, enabling full _undo_ and _redo_ functionality for calculations.
- **Observer Pattern**: Decouples secondary actions from the core calculation logic. Observers for logging (_LoggingObserver_) and auto-saving history (_AutoSaveObserver_) respond to new calculations automatically.

Key features include a full-featured REPL (Read-Eval-Print Loop), persistent history management with _pandas_, comprehensive logging, color-coded output with _colorama_, and a full suite of unit tests with over **90%** coverage.

---

## Installation Instructions

Follow these steps to set up and run the project locally.

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/RoddyCodes/Enhanced-Calculator-Project.git
cd Enhanced-Calculator-Project
```

### 2. Create and Activate a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create the virtual environment (named 'myenv' in this example)
python3 -m venv myenv

# Activate the virtual environment
source myenv/bin/activate
```

You will know the environment is active when your terminal prompt is prefixed with `(myenv)`.

### 3. Install Dependencies

All required packages are listed in the **requirements.txt** file. Install them using `pip`:

```bash
# Ensure you are using the pip from your virtual environment
python3 -m pip install -r requirements.txt
```

---

## Configuration Setup

The application uses a **.env** file to manage configuration settings. This file should be created in the root directory of the project.

### 1. Create the .env file

Create a file named **.env** in the project root.

### 2. Add Configuration Variables

Copy and paste the following template into your **.env** file. You can adjust the values as needed.

```env
# .env file

# --- Directories ---
# Paths are relative to the project root. The app will create these folders.
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history

# --- Logging ---
# The name of the log file that will be created inside CALCULATOR_LOG_DIR
CALCULATOR_LOG_FILE=app.log

# --- History Settings ---
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true

# --- Calculation Settings ---
CALCULATOR_PRECISION=4
CALCULATOR_MAX_INPUT_VALUE=1000000000
CALCULATOR_DEFAULT_ENCODING=utf-8
```

---

## Usage Guide

The application is run via a command-line interface (REPL).

### 1. Start the Application

To start the calculator, run the **main.py** script from the project root:

```bash
python3 main.py
```

You will be greeted with a welcome message and a `>>>` prompt.

### 2. Supported Commands

The following commands are available:

| Command                                                                                                             | Description                                                                 | Example        |
| ------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- | -------------- |
| **add**/**subtract**/**multiply**/**divide**/**power**/**root**/**modulus**/**int_divide**/**percent**/**abs_diff** | Performs a calculation with two numbers.                                    | `>>> add 10 5` |
| **history**                                                                                                         | Displays the calculation history for the current session.                   | `>>> history`  |
| **clear**                                                                                                           | Clears the in-memory calculation history.                                   | `>>> clear`    |
| **undo**                                                                                                            | Reverts the last calculation.                                               | `>>> undo`     |
| **redo**                                                                                                            | Re-applies the last undone calculation.                                     | `>>> redo`     |
| **save**                                                                                                            | Manually saves the current session history to _history/manual_history.csv_. | `>>> save`     |
| **load**                                                                                                            | Loads history from _history/manual_history.csv_ into the current session.   | `>>> load`     |
| **help**                                                                                                            | Displays the list of available commands.                                    | `>>> help`     |
| **exit**                                                                                                            | Exits the application gracefully.                                           | `>>> exit`     |

---

## Testing Instructions

The project includes a comprehensive suite of unit tests using _pytest_.

### 1. Run All Tests

To run the entire test suite, execute the following command from the project root:

```bash
pytest
```

### 2. Check Test Coverage

To run the tests and generate a coverage report, use the _pytest-cov_ plugin. The project is configured to enforce at least **90%** coverage.

```bash
pytest --cov=app --cov-report=term-missing
```

This command will show a detailed report in the terminal, including which lines of code were missed by the tests.

---

## CI/CD Information

This repository is configured with a GitHub Actions workflow for Continuous Integration (CI).

- **Workflow File**: _.github/workflows/python-app.yml_
- **Triggers**: The workflow automatically runs on every `push` or `pull_request` to the `main` branch.
- **Jobs**:
  1.  Sets up the specified Python environment.
  2.  Installs all dependencies from **requirements.txt**.
  3.  Runs the _pytest_ suite.
  4.  Measures test coverage and **fails the build if coverage drops below 90%**.

This ensures that all code merged into the main branch is tested and meets the quality standard for test coverage.

import os
import subprocess
import sys
from pathlib import Path
import threading
from typing import Tuple

# Monkey patch to fix PyCharm's debugger issue
if hasattr(threading.Thread, 'isAlive') and not hasattr(threading.Thread, 'is_alive'):
    threading.Thread.is_alive = threading.Thread.isAlive


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def run_test(interpreter: str, test_file: str, timeout: int = 10) -> Tuple[bool, str]:
    """Run a single test file with timeout protection"""
    try:
        result = subprocess.run(
            [sys.executable, interpreter, str(test_file)],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            input="TestInput\n",  # Provide default input
            universal_newlines=True
        )
        return True, result.stdout
    except subprocess.TimeoutExpired:
        return False, f"Test timed out after {timeout} seconds"
    except subprocess.CalledProcessError as e:
        return False, e.stderr if e.stderr else e.stdout
    except Exception as e:
        return False, str(e)


def print_test_result(test_name: str, success: bool, output: str = ""):
    """Print formatted test result"""
    status = f"{Colors.OKGREEN}PASS{Colors.ENDC}" if success else f"{Colors.FAIL}FAIL{Colors.ENDC}"
    print(f"{Colors.BOLD}{test_name:<20}{status}{Colors.ENDC}")
    if output.strip():
        print(f"  {output.strip()}")


def run_all_tests(interpreter: str = "main.py", test_dir: str = "./programs") -> bool:
    """Run all tests with proper path handling"""
    print(f"{Colors.HEADER}Running Flow-Matic Interpreter Tests{Colors.ENDC}")
    print(f"{Colors.OKBLUE}Using interpreter: {interpreter}{Colors.ENDC}")
    print(f"{Colors.OKBLUE}Test directory: {test_dir}{Colors.ENDC}\n")

    # Convert to absolute paths
    interpreter_path = Path(interpreter).resolve()
    test_dir_path = Path(test_dir).resolve()

    if not interpreter_path.exists():
        print(f"{Colors.FAIL}Error: Interpreter not found at {interpreter_path}{Colors.ENDC}")
        return False

    if not test_dir_path.exists():
        print(f"{Colors.FAIL}Error: Test directory not found at {test_dir_path}{Colors.ENDC}")
        return False

    # Get all test files in order
    test_order = [
        'io-test.fm',
        'var-ops.fm',
        'math-test.fm',
        'control-flow.fm',
        'record-test.fm',
        'collection-test.fm',
        'datetime-test.fm',
        'full-test.fm'
    ]

    all_passed = True
    test_results = []

    for test_file in test_order:
        test_path = test_dir_path / test_file
        if not test_path.exists():
            print(f"{Colors.WARNING}Skipping missing test: {test_file}{Colors.ENDC}")
            continue

        print(f"Running {Colors.BOLD}{test_file}{Colors.ENDC}...")
        success, output = run_test(str(interpreter_path), str(test_path))
        test_results.append((test_file, success, output))
        all_passed = all_passed and success
        print_test_result(test_file, success, output)

    # Summary
    passed = sum(1 for _, success, _ in test_results if success)
    total = len(test_results)

    print(f"\n{Colors.BOLD}Summary:{Colors.ENDC}")
    print(f"Tests Run: {total}")
    print(f"Tests Passed: {passed}/{total}")

    if all_passed:
        print(f"{Colors.OKGREEN}All tests passed!{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}Some tests failed.{Colors.ENDC}")

    return all_passed


if __name__ == "__main__":
    # Disable PyCharm's debugger hooks if detected
    if 'pydevd' in sys.modules:
        sys.modules['pydevd'] = None
        os.environ.pop('PYTHONBREAKPOINT', None)

    # Default paths
    interpreter = "main.py"
    test_dir = "./programs"

    # Handle command line arguments
    if len(sys.argv) > 1:
        interpreter = sys.argv[1]
    if len(sys.argv) > 2:
        test_dir = sys.argv[2]

    # Run tests
    success = run_all_tests(interpreter, test_dir)
    sys.exit(0 if success else 1)
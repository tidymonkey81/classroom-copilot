import os
import sys
import subprocess
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

def load_env():
    load_dotenv(find_dotenv())
    required_vars = ["BACKEND_URL", "BACKEND_PORT", "USERPROFILE", "APP_DIR", "EXCEL_CURRICULUM_FILE", "EXCEL_TIMETABLE_FILE"]
    for var in required_vars:
        if var not in os.environ:
            print(f"Error: {var} is not set in the environment.")
            sys.exit(1)

def select_test_file():
    test_categories = {
        "A": {
            "name": "Database Initialization",
            "tests": {
                "1": "backend/app/tests/pytest_init_timetable.py",
                "2": "backend/app/tests/pytest_init_curriculum.py",
                "3": "backend/app/tests/pytest_init_calendar.py"
            }
        },
        "B": {
            "name": "Graph QA",
            "tests": {
                "1": "backend/app/tests/pytest_init_timetable_graph_qa.py",
                "2": "backend/app/tests/pytest_init_curriculum_graph_qa.py",
                "3": "backend/app/tests/pytest_init_calendar_graph_qa.py"
            }
        },
        "C": {
            "name": "Connections",
            "tests": {
                "1": "backend/app/tests/pytest_arbor.py"
            }
        }
    }

    print("Select a test file to run:")
    for category_key, category in test_categories.items():
        print(f"\n{category_key}: {category['name']}")
        for test_key, test_file in category["tests"].items():
            print(f"  {category_key}{test_key}: {test_file}")

    choice = input("Enter your choice: ").upper()

    if len(choice) < 2:
        print("Invalid choice.")
        sys.exit(1)

    category_key = choice[0]
    test_key = choice[1:]

    if category_key in test_categories and test_key in test_categories[category_key]["tests"]:
        return test_categories[category_key]["tests"][test_key], choice

    print("Invalid choice.")
    sys.exit(1)

def create_log_dir(choice):
    base_dir = "."
    if choice[0] == "A":
        log_dir = os.path.join(base_dir, "logs", "pytests", "database", "init")
    elif choice[0] == "B":
        log_dir = os.path.join(base_dir, "logs", "pytests", "database", "langchain", "graph_qa")
    elif choice[0] == "C":
        log_dir = os.path.join(base_dir, "logs", "pytests", "database", "connections", "arbor")
    else:
        print("Invalid choice.")
        sys.exit(1)
    
    os.makedirs(log_dir, exist_ok=True)
    return log_dir

def run_tests(test_file, log_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_name = os.path.basename(test_file).replace(".py", "")
    result = subprocess.run([
        "pytest", test_file,
        f"--junitxml={os.path.join(log_dir, f'{test_name}_pytest_report_{timestamp}.xml')}",
        f"--html={os.path.join(log_dir, f'{test_name}_pytest_report_{timestamp}.html')}",
        "--self-contained-html"
    ])
    if result.returncode != 0:
        print(f"{result.returncode} tests failed.")
        sys.exit(result.returncode)
    else:
        print("All tests passed.")

def main():
    load_env()
    test_file, choice = select_test_file()
    if not test_file:
        print("Invalid choice.")
        sys.exit(1)

    log_dir = create_log_dir(choice)
    run_tests(test_file, log_dir)

if __name__ == "__main__":
    main()
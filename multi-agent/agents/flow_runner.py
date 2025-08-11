# agents/flow_runner.py

from agents.code_writer import generate_code
from agents.test_generator import generate_tests


def run_code_writer_and_test(task: str, language: str, model: str = "mistral") -> tuple[str, str]:
    """
    Runs the code writer agent to generate solution code for the task,
    then passes that code to the test generator agent to generate test cases.

    Args:
        task (str): Task description from user.
        language (str): Programming language for the solution.
        model (str): Local LLM model name (default is "mistral").

    Returns:
        Tuple[str, str]: Generated code and generated test cases.
    """
    print("🚀 Running Code Writer Agent...")
    code = generate_code(task, language, model=model)

    print("\n🧪 Running Test Generator Agent...")
    tests = generate_tests(code, model=model)

    return code.strip(), tests.strip()

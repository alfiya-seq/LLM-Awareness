# agents/test_generator.py

import requests
from pathlib import Path

PROMPT_PATH = Path("prompts/test_generator_prompt.txt")
TEST_FILE_PATH = Path("test_solution.py")

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"  # Change to your preferred model name

def load_test_prompt_template() -> str:
    with open(PROMPT_PATH, "r") as f:
        return f.read()

def build_test_prompt(code: str) -> str:
    template = load_test_prompt_template()
    return template.replace("{{code}}", code)

def run_ollama(prompt: str, model: str = MODEL_NAME) -> str:
    response = requests.post(OLLAMA_API_URL, json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    response.raise_for_status()
    return response.json()["response"]

def generate_tests(code: str, model: str = MODEL_NAME) -> str:
    prompt = build_test_prompt(code)
    print(f"\n🧪 Prompt sent to LLM for test generation:\n", prompt)
    tests = run_ollama(prompt, model=model)

    TEST_FILE_PATH.write_text(tests.strip())
    print(f"\n✅ Tests saved to {TEST_FILE_PATH.absolute()}")

    return tests.strip()

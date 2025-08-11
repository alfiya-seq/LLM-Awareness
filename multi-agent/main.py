# main.py

from dotenv import load_dotenv
import os
from agents.code_writer import generate_code

load_dotenv()
model_name = os.getenv("MODEL_NAME", "mistral")

# Task input
with open("examples/sample_task.txt", "r") as f:
    task = f.read()

# Language input (can be CLI or hardcoded for now)
language = input("Enter target language (e.g., Python, JavaScript, Java, C++): ").strip()

print(f"\n🚀 Generating {language} code for the task...")
generated_code = generate_code(task, language, model=model_name)

print("\n✅ Generated Code:\n")
print(generated_code)

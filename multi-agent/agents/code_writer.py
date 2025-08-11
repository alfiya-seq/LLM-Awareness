# agents/code_writer.py

import subprocess
from pathlib import Path
import requests

PROMPT_PATH = Path("prompts/code_writer_prompt.txt")

def load_prompt_template() -> str:
    with open(PROMPT_PATH, "r") as f:
        return f.read()

def build_prompt(task: str, language: str) -> str:
    template = load_prompt_template()
    return template.replace("{{task}}", task).replace("{{language}}", language)

# For Ollama HTTP API execution
def run_ollama_http(prompt: str, model: str = "mistral", stream: bool = False) -> str:
    url = "http://localhost:11434/api/generate"
    try:
        response = requests.post(url, json={
            "model": model,
            "prompt": prompt,
            "stream": stream
        })
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        print("🔴 Error contacting Ollama:", e)
        return "Error: Failed to generate code from Ollama."
    
# For local LLM execution   
def run_local_llm(prompt: str, model: str = "mistral") -> str:
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result.stdout.decode("utf-8")

def generate_code(task: str, language: str, model: str = "mistral") -> str:
    prompt = build_prompt(task, language)
    print(f"\n🧠 Prompt sent to LLM for {language}:\n", prompt)
    code = run_ollama_http(prompt, model=model)
    return code.strip()

import subprocess     #Python’s built-in module to run shell commands (like ollama run ...) from your script

def run_mistral(prompt: str) -> str:
    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt.encode(),          # Convert prompt (string) → bytes
        stdout=subprocess.PIPE         # Capture standard output
    )
    return result.stdout.decode()      # convert butes response to string

# main.py

from dotenv import load_dotenv
import os

load_dotenv()

model_name = os.getenv("MODEL_NAME")
retry_limit = os.getenv("RETRY_LIMIT")

print("Loaded environment config:")
print("MODEL_NAME =", model_name)
print("RETRY_LIMIT =", retry_limit)

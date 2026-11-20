
import os

MODELO = os.getenv("MODELO_OLLAMA", "qwen2.5:3b")

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434"
)

MAX_PASOS = 3

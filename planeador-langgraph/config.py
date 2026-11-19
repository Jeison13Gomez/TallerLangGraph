
import os

# Modelo local con soporte para herramientas
MODELO = os.getenv("MODELO_OLLAMA", "qwen2.5:3b")

# Dirección del servidor de Ollama
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

# Máximo de agentes especialistas que puede consultar el supervisor
MAX_PASOS = 3

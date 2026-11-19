
import time
import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama

from config import MODELO, OLLAMA_URL
from grafo import grafo


app = FastAPI(
    title="Planeador de Fin de Semana Multiagente",
    description="API REST con LangGraph y Ollama",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    question: str = Field(min_length=1)


class ChatResponse(BaseModel):
    requestId: str
    answer: str
    elapsedMs: int
    status: str


@app.get("/health/llm")
def health_llm():
    try:
        modelo = ChatOllama(
            model=MODELO,
            base_url=OLLAMA_URL,
            temperature=0
        )

        respuesta = modelo.invoke("Responde únicamente OK")

        return {
            "estado": "disponible",
            "modelo": MODELO,
            "respuesta": respuesta.content
        }

    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail="Ollama no está disponible"
        )


@app.post(
    "/api/v1/chat",
    response_model=ChatResponse
)
def chat(datos: ChatRequest):
    inicio = time.perf_counter()
    request_id = str(uuid.uuid4())

    try:
        resultado = grafo.invoke({
            "consulta": datos.question,
            "resultados": [],
            "consultados": []
        })

        tiempo_ms = int(
            (time.perf_counter() - inicio) * 1000
        )

        return ChatResponse(
            requestId=request_id,
            answer=resultado["respuesta_final"],
            elapsedMs=tiempo_ms,
            status="success"
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al procesar la consulta"
        )

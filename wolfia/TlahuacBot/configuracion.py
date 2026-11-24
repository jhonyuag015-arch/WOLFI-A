# PROYECTO: TLAHUACBOT
# Configuracion central: todo lo que quieras ajustar esta aqui.

import os
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
CARPETA_DATOS = CARPETA / "Datos"


# ----------------------------------------------------------------------
# OLLAMA (Llama)
# ----------------------------------------------------------------------

# Usamos 127.0.0.1 y no "localhost": en Windows "localhost" prueba primero
# IPv6 y cada conexion pierde tiempo antes de llegar a Ollama.
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434/api/chat")

# Si tienes tu propio modelo entrenado, cambia el nombre (por ejemplo "tlahuacbot").
MODELO = os.environ.get("OLLAMA_MODELO", "llama3.2:3b")

# Pon USAR_LLAMA=0 en el entorno para apagar Llama y usar solo el motor.
USAR_LLAMA = os.environ.get("USAR_LLAMA", "1") == "1"

# Cuanto tiempo se queda el modelo cargado en memoria sin usarse.
KEEP_ALIVE = "60m"

# Segundos maximos: para conectar y para esperar el PRIMER texto de Llama
# (con streaming el resto llega por partes, asi que no hay limite total).
TIMEOUT_CONEXION = 5
TIMEOUT_RESPUESTA = 90

# IMPORTANTE: num_ctx debe ser el mismo en todas las llamadas. Si cambia,
# Ollama vuelve a cargar el modelo y la respuesta tarda mucho mas.
OPCIONES = {
    "temperature": 0.5,
    "num_predict": 280,   # tope de palabras de la respuesta (mas alto = mas lento)
    "num_ctx": 2048,      # memoria de contexto (sistema + datos + historial + respuesta)
}


# ----------------------------------------------------------------------
# CONVERSACION
# ----------------------------------------------------------------------

MAX_CARACTERES_PREGUNTA = 500

# Memoria: cuantos mensajes recuerda Llama y de que largo maximo.
MAX_HISTORIAL = 4
MAX_CARACTERES_HISTORIAL = 350

# Datos de carrera que se le pasan a Llama (menos datos = respuesta mas rapida).
MAX_CARRERAS_CONTEXTO = 3
MAX_CARACTERES_CONTEXTO = 2200

# Respuestas guardadas para preguntas repetidas (botones, tarjetas, demos).
TAMANO_CACHE = 64


# ----------------------------------------------------------------------
# SERVIDOR
# ----------------------------------------------------------------------

# Pon TLAHUACBOT_DEBUG=1 en el entorno para modo desarrollo.
DEBUG = os.environ.get("TLAHUACBOT_DEBUG", "0") == "1"

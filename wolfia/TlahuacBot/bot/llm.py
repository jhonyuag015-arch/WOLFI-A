# PROYECTO: TLAHUACBOT
# Capa de Llama (Ollama): prompt, llamada con streaming y calentamiento.

import json
import re
import threading

import requests

import configuracion as cfg


SISTEMA = (
    "Eres TláhuacBot, el asistente virtual del Tecnológico de Tláhuac II "
    "(TecNM). Resuelves dudas de aspirantes y estudiantes sobre carreras, "
    "materias, campo laboral, modalidad, duración y admisión.\n"
    "Reglas:\n"
    "1. Los datos propios del Tec (duración, modalidad, créditos, título, "
    "objetivo, perfiles, qué carreras existen) salen SOLO del CONTEXTO. No "
    "los inventes ni los cambies.\n"
    "2. Puedes complementar con conocimiento general de la disciplina (temas, "
    "puestos, habilidades), diciéndolo con frases como \"en general\" o "
    "\"normalmente\" y aclarando que el plan oficial lo confirman en el Tec.\n"
    "3. Nunca inventes costos, becas, fechas, teléfonos, direcciones, "
    "requisitos ni materias como plan oficial. Si no está en el CONTEXTO, di "
    "que no tienes el dato y que lo consulten con el Tecnológico.\n"
    "4. Recuerdas la conversación: \"esa carrera\" o \"y cuánto dura\" se "
    "refiere a la carrera de la que venían hablando.\n"
    "5. Si la pregunta no tiene relación con el Tec o con elegir carrera, "
    "explica amablemente que solo puedes ayudar con eso.\n"
    "6. Español cercano y amable, máximo 4 oraciones. Si hablas de una "
    "carrera, puedes cerrar con una pregunta corta. Texto plano: sin "
    "asteriscos, viñetas, negritas, encabezados ni emojis."
)

# Una sola sesion HTTP: reutiliza la conexion con Ollama entre preguntas.
_sesion = requests.Session()


class ErrorLlama(Exception):
    # Ollama no esta disponible o fallo a media respuesta.
    pass


def _carga(mensajes, opciones=None, stream=True):
    return {
        "model": cfg.MODELO,
        "stream": stream,
        "keep_alive": cfg.KEEP_ALIVE,
        "options": {**cfg.OPCIONES, **(opciones or {})},
        "messages": mensajes,
    }


def generar(pregunta, contexto, historial):
    # Generador: va entregando el texto de Llama por pedazos.
    # Si Ollama falla lanza ErrorLlama (quien llama usa la respuesta del motor).
    mensajes = [{"role": "system", "content": SISTEMA}]
    mensajes += historial[-cfg.MAX_HISTORIAL:]
    mensajes.append({
        "role": "user",
        "content": f"CONTEXTO:\n{contexto}\n\nPREGUNTA: {pregunta}",
    })

    try:
        # "with" cierra la conexion si el usuario se va a media respuesta,
        # y Ollama deja de generar texto que nadie va a leer.
        with _sesion.post(
            cfg.OLLAMA_URL,
            json=_carga(mensajes),
            stream=True,
            timeout=(cfg.TIMEOUT_CONEXION, cfg.TIMEOUT_RESPUESTA),
        ) as respuesta:
            respuesta.raise_for_status()
            for linea in respuesta.iter_lines():
                if not linea:
                    continue
                dato = json.loads(linea)
                if dato.get("error"):
                    raise ErrorLlama(dato["error"])
                trozo = dato.get("message", {}).get("content", "")
                if trozo:
                    yield trozo
                if dato.get("done"):
                    return
    except (requests.RequestException, ValueError) as error:
        raise ErrorLlama(str(error)) from error


def limpiar_trozo(trozo):
    # Quita simbolos de Markdown de un pedazo (la pagina muestra texto plano).
    return re.sub(r"[*_`#]+", "", trozo)


def limpiar(texto):
    # Limpieza final de la respuesta completa.
    texto = limpiar_trozo(texto)
    texto = re.sub(r"^\s*[-•]\s+", "", texto, flags=re.MULTILINE).strip()

    # Si el limite de palabras la corto a media oracion, la dejamos en la
    # ultima oracion completa.
    if texto and texto[-1] not in ".!?…":
        corte = max(texto.rfind(c) for c in ".!?")
        if corte > len(texto) // 2:
            texto = texto[:corte + 1]
    return texto


def calentar():
    # Carga el modelo en memoria al arrancar, para que la primera pregunta
    # real no pague la carga (puede tardar decenas de segundos).
    def tarea():
        mensajes = [
            {"role": "system", "content": SISTEMA},
            {"role": "user", "content": "hola"},
        ]
        try:
            _sesion.post(
                cfg.OLLAMA_URL,
                json=_carga(mensajes, {"num_predict": 1}, stream=False),
                timeout=300,
            )
        except requests.RequestException:
            pass  # Ollama apagado: el motor atiende mientras tanto.

    if cfg.USAR_LLAMA:
        threading.Thread(target=tarea, daemon=True).start()

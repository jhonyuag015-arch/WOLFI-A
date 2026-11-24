# PROYECTO: TLAHUACBOT
# Evaluacion del chatbot.
#
# Cada caso tiene la pregunta y la "intencion" que el bot DEBERIA devolver.
# El script calcula el porcentaje de aciertos y muestra los casos que fallan.
#
# Como usarlo:  python evaluacion.py
#
# IMPORTANTE: agrega aqui preguntas reales que te hagan tus companeros.
# Mientras mas distintas sean a las que ya tiene el bot, mas honesto
# sera el porcentaje.

from bot.motor import responder


# (pregunta, intencion esperada)
CASOS = [
    # --- Charla basica ---
    ("hola", "saludo"),
    ("buenas tardes", "saludo"),
    ("Gracias", "gracias"),
    ("adios", "despedida"),

    # --- Temas generales ---
    ("¿Qué carreras hay?", "oferta_educativa"),
    ("¿Qué ingenierías ofrece el Tecnológico?", "oferta_educativa"),
    ("que opciones de estudio tiene el tec", "oferta_educativa"),
    ("¿Hay carreras virtuales?", "modalidades"),
    ("Hola, ¿qué carreras hay en línea?", "modalidades"),
    ("¿Cuántos semestres duran las carreras?", "duracion"),
    ("¿Cómo me inscribo?", "admision"),
    ("como saco ficha", "admision"),

    # --- Que se estudia ---
    ("¿Qué voy a aprender en Logística?", "logistica_estudios"),
    ("que se estudia en sistemas", "sistemas_estudios"),
    ("que materias llevan en turismo", "turismo_estudios"),
    ("¿Qué estudian en mecanica?", "mecanica_estudios"),
    ("quiero estudiar tecnologias de la informacion, que voy a aprender",
     "ti_estudios"),
    ("hola buenos dias, que se estudia en turismo", "turismo_estudios"),

    # --- Campo laboral ---
    ("¿Dónde puedo trabajar si estudio Turismo?", "turismo_trabajo"),
    ("campo laboral de TI", "ti_trabajo"),
    ("en que puedo trabajar con ITIC", "ti_trabajo"),
    ("trabajo de logistica", "logistica_trabajo"),
    ("donde trabaja un ingeniero mecanico", "mecanica_trabajo"),
    ("¿Qué hace un ingeniero en sistemas?", "sistemas_trabajo"),

    # --- Modalidad y duracion por carrera ---
    ("¿Cuánto dura mecánica?", "mecanica_modalidad"),
    ("¿Es presencial Turismo?", "turismo_modalidad"),
    ("sistemas es en linea?", "sistemas_modalidad"),
    ("cuanto dura turismo?", "turismo_modalidad"),

    # --- Objetivo y perfiles ---
    ("¿Cuál es la meta de Ingeniería Mecánica?", "objetivo_mecanica"),
    ("cual es el objetivo de turismo", "objetivo_turismo*"),
    ("para que sirve estudiar gestion empresarial", "objetivo_gestion*"),
    ("ingenieria en sistemas computacionales objetivo", "objetivo_sistemas*"),
    ("requisitos de ingreso a gestion empresarial", "gestion_perfil_ingreso"),
    ("perfil de ingreso de logistica", "logistica_perfil_ingreso"),
    ("que habilidades tendre al terminar mecanica",
     "perfil_egreso_mecanica"),
    ("perfil de egreso de turismo", "perfil_egreso_turismo*"),

    # --- Solo mencionan la carrera ---
    ("mecanica", "ficha_mecanica"),
    ("informacion de logistica", "ficha_logistica"),
    ("ahora quiero saber de la ingeniería en tecnologías de la información",
     "ficha_ti"),

    # --- Errores de dedo ---
    ("que se estudia en logistca", "logistica_estudios"),
    ("donde puedo trabjar si estudio turismo", "turismo_trabajo"),

    # --- Varias carreras ---
    ("¿Cuál es el campo laboral de sistemas y gestion?",
     "sistemas_trabajo+gestion_trabajo"),
    ("que es mas dificil, sistemas o mecanica", "varias_carreras"),

    # --- Falta la carrera ---
    ("¿Qué se estudia?", "pedir_carrera"),
    ("donde puedo trabajar", "pedir_carrera"),

    # --- Cosas que el bot todavia no sabe ---
    ("¿Cuánto cuesta la inscripción?", "sin_respuesta"),
    ("¿Dónde queda el Tec?", "sin_respuesta"),
    ("hay becas", "sin_respuesta"),
    ("cuando empiezan las clases", "sin_respuesta"),
    ("Necesito ayuda de una persona", "sin_respuesta"),

    # --- Fuera de tema ---
    ("tengo hambre", "no_entendido"),
    ("cual es la capital de francia", "no_entendido"),

    # --- Segunda tanda (preguntas escritas despues de afinar el bot) ---
    ("oye y en turismo que se aprende", "turismo_estudios"),
    ("cual es el campo de trabajo de gestion empresarial", "gestion_trabajo"),
    ("la de logistica es presencial", "logistica_modalidad"),
    ("cuantos semestres son en sistemas", "sistemas_modalidad"),
    ("que necesito para entrar a mecanica", "mecanica_perfil_ingreso"),
    ("que carreras hay disponibles", "oferta_educativa"),
    ("hay alguna carrera a distancia", "modalidades"),
    ("como puedo entrar al tec", "admision"),
    ("ITIC en que se trabaja", "ti_trabajo"),
    ("cual es la finalidad de logistica", "objetivo_logistica*"),
    ("me cuentas de gestion empresarial", "ficha_gestion"),
    ("cuanto cuesta estudiar turismo", "sin_respuesta"),
    ("a que hora entran", "no_entendido"),
    ("quien es el director", "no_entendido"),
    ("muchas gracias por todo", "gracias"),
    ("que onda", "no_entendido"),
    ("sistemas o ti cual me conviene", "varias_carreras"),
    ("de que se trata ingenieria mecanica", "mecanica_estudios"),
    ("donde laboran los egresados de ti", "ti_trabajo"),
    ("modalidad de gestion", "gestion_modalidad"),
]


def evaluar():
    aciertos = 0
    fallas = []

    for pregunta, esperada in CASOS:
        resultado = responder(pregunta)
        obtenida = resultado["intencion"]

        if obtenida == esperada:
            aciertos += 1
        else:
            fallas.append((pregunta, esperada, obtenida, resultado["confianza"]))

    total = len(CASOS)
    porcentaje = 100 * aciertos / total

    print(f"Aciertos: {aciertos} de {total} ({porcentaje:.1f}%)")

    if fallas:
        print("\nCasos que fallaron:")
        for pregunta, esperada, obtenida, confianza in fallas:
            print(f"  Pregunta : {pregunta}")
            print(f"  Esperada : {esperada}")
            print(f"  Obtenida : {obtenida} (confianza {confianza})")
            print()


if __name__ == "__main__":
    evaluar()

"""Funciones de cálculo y parámetros configurables del diagnóstico."""

from questions import DIMENSIONS, QUESTIONS


# Puntos de corte del nivel de madurez, evaluados de menor a mayor.
NIVELES_MADUREZ = [
    (1.80, "Reactivo"),
    (2.60, "Básico"),
    (3.40, "Activo"),
    (4.20, "Preventivo"),
    (5.00, "Excelencia Operacional"),
]

# Parámetros configurables del modelo; no son una escala científica universal.
NIVELES_EXPOSICION = [
    (0.80, "Baja"),
    (1.60, "Media-Baja"),
    (2.40, "Media"),
    (3.20, "Alta"),
    (4.00, "Muy alta"),
]


def validar_configuracion(perdidas):
    """Verifica preguntas, dimensiones, alternativas y asociaciones."""
    if len(QUESTIONS) != 12 or len(DIMENSIONS) != 6:
        raise ValueError("El cuestionario debe contener 12 preguntas y 6 dimensiones.")
    ids = [pregunta["id"] for pregunta in QUESTIONS]
    if len(ids) != len(set(ids)):
        raise ValueError("Los identificadores de las preguntas deben ser únicos.")
    for dimension in DIMENSIONS:
        if not any(pregunta["dimension"] == dimension for pregunta in QUESTIONS):
            raise ValueError(f"La dimensión '{dimension}' no tiene preguntas asociadas.")
    for pregunta in QUESTIONS:
        campos = {"id", "dimension", "indicador", "pregunta", "opciones"}
        if not campos.issubset(pregunta):
            raise ValueError(f"La pregunta {pregunta.get('id', '?')} está incompleta.")
        if pregunta["dimension"] not in DIMENSIONS:
            raise ValueError(f"La pregunta {pregunta['id']} tiene una dimensión desconocida.")
        if [opcion["valor"] for opcion in pregunta["opciones"]] != [1, 2, 3, 4, 5]:
            raise ValueError(f"La pregunta {pregunta['id']} debe tener opciones del 1 al 5.")
    ids_validos = set(ids)
    for perdida in perdidas:
        campos = {"id", "nombre", "descripcion", "preguntas", "dimensiones"}
        if not campos.issubset(perdida):
            raise ValueError(f"La pérdida {perdida.get('id', '?')} está incompleta.")
        if not perdida["preguntas"]:
            raise ValueError(f"La pérdida {perdida['id']} no tiene preguntas asociadas.")
        if not set(perdida["preguntas"]).issubset(ids_validos):
            raise ValueError(f"La pérdida {perdida['id']} contiene preguntas inexistentes.")
        if not set(perdida["dimensiones"]).issubset(set(DIMENSIONS)):
            raise ValueError(f"La pérdida {perdida['id']} contiene dimensiones desconocidas.")


def _validar_respuestas(respuestas, exigir_todas=True):
    """Valida valores enteros 1-5 y, cuando corresponde, las 12 respuestas."""
    ids_esperados = {pregunta["id"] for pregunta in QUESTIONS}
    if exigir_todas and set(respuestas) != ids_esperados:
        raise ValueError("Deben responderse todas las preguntas antes de calcular.")
    if not set(respuestas).issubset(ids_esperados):
        raise ValueError("Las respuestas contienen identificadores desconocidos.")
    if any(not isinstance(valor, int) or not 1 <= valor <= 5 for valor in respuestas.values()):
        raise ValueError("Todas las respuestas deben ser números enteros entre 1 y 5.")


def calcular_dimensiones(respuestas):
    """Calcula el promedio de las preguntas asociadas a cada dimensión."""
    _validar_respuestas(respuestas)
    resultados = {}
    for dimension in DIMENSIONS:
        ids = [p["id"] for p in QUESTIONS if p["dimension"] == dimension]
        if not ids:
            raise ValueError(f"La dimensión '{dimension}' no tiene preguntas.")
        resultados[dimension] = sum(respuestas[id_pregunta] for id_pregunta in ids) / len(ids)
    return resultados


def calcular_excelencia_operacional(resultados_dimensiones):
    """Calcula el promedio simple de las seis dimensiones."""
    if set(resultados_dimensiones) != set(DIMENSIONS):
        raise ValueError("Faltan resultados de una o más dimensiones.")
    valores = list(resultados_dimensiones.values())
    if any(not 1 <= valor <= 5 for valor in valores):
        raise ValueError("Los resultados de las dimensiones deben estar entre 1 y 5.")
    return sum(valores) / len(valores)


def calcular_brechas(resultados_dimensiones):
    """Calcula la distancia respecto del nivel objetivo 5."""
    if set(resultados_dimensiones) != set(DIMENSIONS):
        raise ValueError("Faltan resultados para calcular las brechas.")
    return {dimension: 5 - valor for dimension, valor in resultados_dimensiones.items()}


def clasificar_nivel(valor):
    """Clasifica una nota de 1 a 5 usando NIVELES_MADUREZ."""
    if not 1 <= valor <= 5:
        raise ValueError("El valor de madurez debe estar entre 1 y 5.")
    return next(nombre for limite, nombre in NIVELES_MADUREZ if valor <= limite)


def calcular_exposicion_perdidas(respuestas, matriz_perdidas):
    """Calcula exposición 0-4 como 5 menos el promedio relacionado.

    El resultado es una señal diagnóstica: no cuantifica dinero, frecuencia ni
    confirma la existencia de una pérdida.
    """
    _validar_respuestas(respuestas)
    exposicion = {}
    for perdida in matriz_perdidas:
        ids = perdida["preguntas"]
        if not ids:
            raise ValueError(f"La pérdida {perdida['id']} no tiene preguntas asociadas.")
        promedio = sum(respuestas[id_pregunta] for id_pregunta in ids) / len(ids)
        exposicion[perdida["id"]] = max(0.0, min(4.0, 5 - promedio))
    return exposicion


def clasificar_exposicion(valor):
    """Clasifica una exposición 0-4 usando NIVELES_EXPOSICION."""
    if not 0 <= valor <= 4:
        raise ValueError("La exposición debe estar entre 0 y 4.")
    return next(nombre for limite, nombre in NIVELES_EXPOSICION if valor <= limite)


def obtener_principales_brechas(resultados_dimensiones, cantidad=3):
    """Devuelve las dimensiones con mayor distancia respecto de 5."""
    brechas = calcular_brechas(resultados_dimensiones)
    ordenadas = sorted(brechas, key=brechas.get, reverse=True)[:cantidad]
    return [{"dimension": d, "resultado": resultados_dimensiones[d], "brecha": brechas[d]}
            for d in ordenadas]


def obtener_principales_perdidas(exposicion, matriz_perdidas, cantidad=5):
    """Une la configuración y ordena los focos por exposición."""
    por_id = {perdida["id"]: perdida for perdida in matriz_perdidas}
    ids = sorted(exposicion, key=exposicion.get, reverse=True)[:cantidad]
    return [{**por_id[id_perdida], "exposicion": exposicion[id_perdida],
             "nivel_exposicion": clasificar_exposicion(exposicion[id_perdida])}
            for id_perdida in ids]


def generar_resumen_diagnostico(nota, resultados, exposicion, matriz_perdidas):
    """Construye un resumen objetivo mediante una plantilla fija."""
    brechas = obtener_principales_brechas(resultados, 2)
    focos = obtener_principales_perdidas(exposicion, matriz_perdidas, 3)
    nombres_brechas = " y ".join(item["dimension"] for item in brechas)
    nombres_focos = ", ".join(item["nombre"] for item in focos)
    texto_focos = (f"El análisis orientativo del árbol de pérdidas identifica como focos "
                   f"prioritarios de revisión: {nombres_focos}." if focos else
                   "La matriz de pérdidas aún no contiene focos configurados.")
    nota_visible = f"{nota:.2f}".replace(".", ",")
    return (f"La empresa obtuvo un Índice de Excelencia Operacional de {nota_visible} sobre 5, "
            f"correspondiente al nivel {clasificar_nivel(nota)}. Las principales brechas "
            f"se concentran en {nombres_brechas}. {texto_focos}")

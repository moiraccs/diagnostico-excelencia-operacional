"""Interfaz principal del Diagnóstico de Excelencia Operacional."""

import pandas as pd
import streamlit as st

from calculations import (
    calcular_brechas,
    calcular_dimensiones,
    calcular_excelencia_operacional,
    calcular_exposicion_perdidas,
    clasificar_exposicion,
    clasificar_nivel,
    generar_resumen_diagnostico,
    obtener_principales_brechas,
    obtener_principales_perdidas,
    validar_configuracion,
)
from losses import LOSSES, MATRIZ_VALIDADA
from questions import DIMENSIONS, QUESTIONS
from visualizations import (
    crear_escala_madurez,
    crear_grafico_brechas,
    crear_radar,
    crear_visualizacion_perdidas,
)


st.set_page_config(
    page_title="Diagnóstico de Excelencia Operacional",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Estilos sobrios para mejorar legibilidad en computador.
st.markdown("""
<style>
:root {--azul:#173B57; --turquesa:#1D7A78; --naranja:#D98B2B; --fondo:#F5F7F9; --texto:#263746;}
.stApp {background:var(--fondo); color:var(--texto);}
.block-container {max-width:1180px; padding:2.4rem 2.2rem 4rem;}
html, body, [class*="st-"] {font-size:18px;}
h1 {font-size:40px !important; color:var(--azul); line-height:1.15 !important;}
h2 {font-size:29px !important; color:var(--azul); margin-top:1.4rem !important;}
h3 {font-size:24px !important; color:var(--azul);}
p, li {font-size:18px; line-height:1.65;}
[data-testid="stRadio"] label p {font-size:17px !important; line-height:1.48 !important;}
[data-testid="stRadio"] > div {gap:0.65rem;}
[data-testid="stProgress"] > div > div {background-color:var(--turquesa);}
[data-testid="stButton"] button, [data-testid="stDownloadButton"] button {
  min-height:48px; font-size:17px; border-radius:8px; font-weight:600;
}
.hero {background:linear-gradient(135deg,#173B57 0%,#215B70 100%); padding:54px 58px;
  border-radius:18px; color:white; box-shadow:0 12px 35px rgba(23,59,87,.14); margin:10px 0 26px;}
.hero h1 {color:white !important; font-size:42px !important; margin:0 0 16px;}
.hero .subtitle {font-size:25px; line-height:1.38; font-weight:500; max-width:920px;}
.hero .detail {font-size:18px; line-height:1.65; max-width:900px; opacity:.92; margin-top:22px;}
.dimension-card {background:white; border-left:7px solid var(--turquesa); border-radius:12px;
  padding:22px 26px; margin:20px 0 26px; box-shadow:0 5px 18px rgba(30,52,70,.07);}
.dimension-card .eyebrow {color:var(--turquesa); font-weight:700; font-size:16px; letter-spacing:.08em;}
.dimension-card .name {color:var(--azul); font-weight:750; font-size:29px; margin-top:4px;}
.question-card {background:white; border:1px solid #DCE4EA; border-radius:12px;
  padding:25px 28px 17px; margin:18px 0 18px; box-shadow:0 3px 12px rgba(30,52,70,.05);}
.question-text {font-size:21px; line-height:1.45; font-weight:700; color:#243B4D; margin-bottom:8px;}
.indicator {font-size:16px; color:#5B6F7D; margin-bottom:16px;}
.result-card {background:white; border-top:7px solid var(--turquesa); border-radius:16px;
  padding:28px 34px; text-align:center; box-shadow:0 8px 25px rgba(23,59,87,.10);}
.result-label {font-size:20px; color:#526775; text-transform:uppercase; letter-spacing:.05em;}
.result-number {font-size:54px; font-weight:800; color:var(--azul); line-height:1.15; margin:10px 0;}
.result-level {font-size:24px; font-weight:700; color:var(--turquesa);}
.summary-card {background:#EAF3F2; border:1px solid #C7DEDB; border-radius:12px; padding:24px 28px;}
.summary-card h3 {margin-top:0;}
.gap-card {background:white; border:1px solid #DCE4EA; border-radius:11px; padding:19px 21px;
  min-height:170px; box-shadow:0 3px 12px rgba(30,52,70,.05);}
.gap-rank {font-size:15px; font-weight:700; color:var(--naranja); text-transform:uppercase;}
.gap-name {font-size:20px; font-weight:700; color:var(--azul); margin:7px 0 10px;}
.loss-card {background:white; border-left:5px solid var(--naranja); border-radius:10px;
  padding:18px 22px; margin:12px 0; box-shadow:0 3px 12px rgba(30,52,70,.05);}
.loss-card strong {color:var(--azul); font-size:19px;}
.commercial {background:#173B57; color:white; border-radius:14px; padding:28px 32px; margin-top:30px;}
.commercial h3 {color:white !important; margin-top:0;}
.commercial p {color:white; opacity:.94;}
.small-note {font-size:15px; color:#607584; line-height:1.5;}
div[data-testid="stDataFrame"] {background:white; border-radius:10px; padding:4px;}
@media (max-width:700px) {.block-container{padding:1.3rem .9rem 3rem}.hero{padding:34px 25px}.hero h1{font-size:34px!important}}
</style>
""", unsafe_allow_html=True)


def formato(valor):
    """Presenta decimales con coma, sin alterar los valores de cálculo."""
    return f"{valor:.2f}".replace(".", ",")


def inicializar_estado():
    """Crea las variables necesarias para navegar sin perder respuestas."""
    valores_iniciales = {
        "pantalla": "inicio",
        "dimension_actual": 0,
        "diagnostico": None,
        # Este diccionario no está ligado a los widgets; por eso sus valores se
        # conservan aunque la pregunta deje de mostrarse al cambiar de dimensión.
        "respuestas_guardadas": {},
    }
    for clave, valor in valores_iniciales.items():
        if clave not in st.session_state:
            st.session_state[clave] = valor


def reiniciar_diagnostico():
    """Limpia respuestas, resultados y navegación."""
    for pregunta in QUESTIONS:
        st.session_state.pop(f"respuesta_{pregunta['id']}", None)
    st.session_state["pantalla"] = "inicio"
    st.session_state["dimension_actual"] = 0
    st.session_state["diagnostico"] = None
    st.session_state["respuestas_guardadas"] = {}


def guardar_respuesta(id_pregunta):
    """Copia una selección del widget al almacenamiento persistente."""
    seleccion = st.session_state.get(f"respuesta_{id_pregunta}")
    if seleccion:
        st.session_state["respuestas_guardadas"][id_pregunta] = int(
            seleccion.split(" — ", 1)[0]
        )


def leer_respuestas():
    """Devuelve una copia de las respuestas persistentes."""
    return dict(st.session_state["respuestas_guardadas"])


def generar_diagnostico():
    """Ejecuta todos los cálculos únicamente con las 12 respuestas."""
    respuestas = leer_respuestas()
    resultados = calcular_dimensiones(respuestas)
    nota = calcular_excelencia_operacional(resultados)
    brechas = calcular_brechas(resultados)
    exposicion = calcular_exposicion_perdidas(respuestas, LOSSES)
    st.session_state["diagnostico"] = {
        "respuestas": respuestas, "resultados": resultados, "nota": nota,
        "brechas": brechas, "exposicion": exposicion,
    }
    st.session_state["pantalla"] = "resultados"


def csv_respuestas(respuestas):
    """Exporta las respuestas con sus descriptores."""
    filas = []
    for pregunta in QUESTIONS:
        valor = respuestas[pregunta["id"]]
        texto = next(opcion["texto"] for opcion in pregunta["opciones"] if opcion["valor"] == valor)
        filas.append({
            "Pregunta": pregunta["pregunta"], "Indicador": pregunta["indicador"],
            "Dimensión": pregunta["dimension"], "Respuesta numérica": valor,
            "Texto de la respuesta seleccionada": texto,
        })
    return pd.DataFrame(filas).to_csv(index=False).encode("utf-8-sig")


def csv_resultados(diagnostico):
    """Exporta dimensiones, resultado general y exposición orientativa."""
    filas = []
    for dimension in DIMENSIONS:
        valor = diagnostico["resultados"][dimension]
        filas.append({
            "Tipo": "Dimensión", "Elemento": dimension, "Puntaje": formato(valor),
            "Indicador complementario": formato(diagnostico["brechas"][dimension]),
            "Nombre del indicador": "Brecha", "Clasificación": clasificar_nivel(valor),
        })
    filas.append({
        "Tipo": "Resultado general", "Elemento": "Índice de Excelencia Operacional",
        "Puntaje": formato(diagnostico["nota"]), "Indicador complementario": "",
        "Nombre del indicador": "", "Clasificación": clasificar_nivel(diagnostico["nota"]),
    })
    por_id = {perdida["id"]: perdida for perdida in LOSSES}
    for id_perdida, valor in diagnostico["exposicion"].items():
        filas.append({
            "Tipo": "Posible foco de pérdida", "Elemento": por_id[id_perdida]["nombre"],
            "Puntaje": "", "Indicador complementario": formato(valor),
            "Nombre del indicador": "Exposición orientativa (0-4)",
            "Clasificación": clasificar_exposicion(valor),
        })
    return pd.DataFrame(filas).to_csv(index=False).encode("utf-8-sig")


def mostrar_inicio():
    st.markdown("""
    <div class="hero">
      <h1>Diagnóstico de Excelencia Operacional</h1>
      <div class="subtitle">Identifique el nivel actual de gestión de su empresa, sus principales brechas y los focos de pérdida que pueden estar afectando su desempeño.</div>
      <div class="detail">Esta herramienta permite realizar una evaluación inicial de las prácticas de gestión de la empresa. A partir de sus respuestas se analizarán seis dimensiones de Excelencia Operacional y se identificarán posibles focos de pérdida que requieren mayor atención.</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### Una visión inicial, clara y basada en sus respuestas")
    columnas = st.columns(3)
    columnas[0].markdown("**6 dimensiones**  \nPrácticas esenciales de gestión operacional.")
    columnas[1].markdown("**12 preguntas**  \nAlternativas adaptadas a distintos niveles de desarrollo.")
    columnas[2].markdown("**Resultados visuales**  \nBrechas y focos de pérdida que requieren revisión.")
    st.write("")
    if st.button("Comenzar diagnóstico", type="primary", width="stretch"):
        st.session_state["pantalla"] = "cuestionario"
        st.rerun()


def mostrar_cuestionario():
    indice = st.session_state["dimension_actual"]
    dimension = DIMENSIONS[indice]
    numero = indice + 1
    progreso = numero / len(DIMENSIONS)
    st.title("Diagnóstico de Excelencia Operacional")
    st.markdown(f"**Progreso del diagnóstico: {round(progreso * 100)} %**")
    st.progress(progreso)
    st.markdown(
        f'<div class="dimension-card"><div class="eyebrow">DIMENSIÓN {numero} DE {len(DIMENSIONS)}</div>'
        f'<div class="name">{dimension}</div></div>', unsafe_allow_html=True)
    st.info("Seleccione la alternativa que mejor represente las prácticas habituales de la empresa, no una situación excepcional.")

    preguntas_dimension = [pregunta for pregunta in QUESTIONS if pregunta["dimension"] == dimension]
    for pregunta in preguntas_dimension:
        st.markdown(
            f'<div class="question-card"><div class="question-text">Pregunta {pregunta["id"]}. '
            f'{pregunta["pregunta"]}</div><div class="indicator">Indicador: '
            f'{pregunta["indicador"]}</div></div>', unsafe_allow_html=True)
        opciones = [f'{opcion["valor"]} — {opcion["texto"]}' for opcion in pregunta["opciones"]]
        clave_widget = f"respuesta_{pregunta['id']}"
        # Al volver a una dimensión, reconstruye la selección visible a partir
        # del diccionario persistente.
        if clave_widget not in st.session_state and pregunta["id"] in st.session_state["respuestas_guardadas"]:
            valor_guardado = st.session_state["respuestas_guardadas"][pregunta["id"]]
            st.session_state[clave_widget] = opciones[valor_guardado - 1]
        st.radio(
            f"Respuesta de la pregunta {pregunta['id']}", opciones, index=None,
            key=clave_widget, label_visibility="collapsed",
            on_change=guardar_respuesta, args=(pregunta["id"],))
        st.write("")

    izquierda, _, derecha = st.columns([1, 2, 1])
    if indice > 0 and izquierda.button("Anterior", width="stretch"):
        st.session_state["dimension_actual"] -= 1
        st.rerun()

    ids_dimension = [pregunta["id"] for pregunta in preguntas_dimension]
    respondidas = all(id_pregunta in st.session_state["respuestas_guardadas"]
                      for id_pregunta in ids_dimension)
    if indice < len(DIMENSIONS) - 1:
        if derecha.button("Siguiente", type="primary", width="stretch"):
            if respondidas:
                st.session_state["dimension_actual"] += 1
                st.rerun()
            else:
                st.error("Debe responder las dos preguntas de esta dimensión antes de continuar.")
    else:
        if derecha.button("Generar diagnóstico", type="primary", width="stretch"):
            if not respondidas:
                st.error("Debe responder las dos preguntas de esta dimensión antes de continuar.")
            elif len(leer_respuestas()) != len(QUESTIONS):
                st.error("Faltan respuestas en una dimensión anterior. Use “Anterior” para revisarlas.")
            else:
                try:
                    generar_diagnostico()
                    st.rerun()
                except (ValueError, KeyError, TypeError, ZeroDivisionError) as error:
                    st.error(f"No fue posible calcular el diagnóstico: {error}")


def mostrar_resultados():
    diagnostico = st.session_state["diagnostico"]
    resultados, brechas = diagnostico["resultados"], diagnostico["brechas"]
    exposicion, nota = diagnostico["exposicion"], diagnostico["nota"]
    nivel = clasificar_nivel(nota)

    st.title("Resultados del diagnóstico")
    st.markdown(
        f'<div class="result-card"><div class="result-label">Índice de Excelencia Operacional</div>'
        f'<div class="result-number">{formato(nota)} / 5,00</div>'
        f'<div class="result-level">Nivel actual: {nivel}</div></div>', unsafe_allow_html=True)
    st.plotly_chart(crear_escala_madurez(nota), width="stretch", config={"displayModeBar": False})

    resumen = generar_resumen_diagnostico(nota, resultados, exposicion, LOSSES)
    st.markdown(f'<div class="summary-card"><h3>Resumen del diagnóstico</h3><p>{resumen}</p></div>',
                unsafe_allow_html=True)

    st.header("Desarrollo de las dimensiones")
    st.plotly_chart(crear_radar(resultados), width="stretch", config={"displayModeBar": False})
    st.caption("Las áreas más cercanas al borde exterior presentan un mayor nivel de desarrollo. Las áreas con mayor distancia respecto al nivel 5 representan las principales brechas detectadas.")

    st.header("Principales brechas detectadas")
    principales_brechas = obtener_principales_brechas(resultados, 3)
    columnas = st.columns(3)
    for posicion, (columna, item) in enumerate(zip(columnas, principales_brechas), start=1):
        columna.markdown(
            f'<div class="gap-card"><div class="gap-rank">Prioridad de revisión {posicion}</div>'
            f'<div class="gap-name">{item["dimension"]}</div><div>Resultado: '
            f'<strong>{formato(item["resultado"])} / 5</strong></div><div>Brecha: '
            f'<strong>{formato(item["brecha"])}</strong></div></div>', unsafe_allow_html=True)
    st.plotly_chart(crear_grafico_brechas(brechas), width="stretch", config={"displayModeBar": False})

    st.header("Árbol de pérdidas simplificado")
    st.markdown("Este módulo relaciona las prácticas evaluadas con **posibles focos de pérdida**. La exposición es una señal orientativa de 0 a 4; no confirma que la pérdida exista y no representa una cuantificación económica.")
    if not MATRIZ_VALIDADA:
        st.warning("La matriz pregunta–pérdida incluida en esta versión es provisional y debe reemplazarse por la relación validada en la tesis antes de utilizar sus resultados como instrumento definitivo.")
    st.plotly_chart(crear_visualizacion_perdidas(exposicion, LOSSES), width="stretch",
                    config={"displayModeBar": False})

    st.subheader("Principales focos de pérdida que requieren revisión")
    principales_perdidas = obtener_principales_perdidas(exposicion, LOSSES, 5)
    for posicion, perdida in enumerate(principales_perdidas, start=1):
        dimensiones = ", ".join(perdida["dimensiones"])
        st.markdown(
            f'<div class="loss-card"><strong>{posicion}. {perdida["nombre"]}</strong><br>'
            f'Exposición orientativa: <b>{formato(perdida["exposicion"])} / 4 — '
            f'{perdida["nivel_exposicion"]}</b><br>Relacionado principalmente con: {dimensiones}<br>'
            f'<span class="small-note">{perdida["descripcion"]}</span></div>', unsafe_allow_html=True)

    dos_brechas = [item["dimension"] for item in principales_brechas[:2]]
    st.info(f"Las mayores brechas se concentran en {dos_brechas[0]} y {dos_brechas[1]}. Estas dimensiones están asociadas a varios de los focos de pérdida presentados y requieren una revisión más profunda; esta relación no implica causalidad estadística.")

    st.header("Tabla de resultados")
    tabla = pd.DataFrame([{
        "Dimensión": dimension, "Resultado": formato(resultados[dimension]),
        "Brecha": formato(brechas[dimension]), "Nivel": clasificar_nivel(resultados[dimension]),
    } for dimension in DIMENSIONS])
    st.dataframe(tabla, hide_index=True, width="stretch")

    st.header("Descargar resultados")
    col1, col2 = st.columns(2)
    col1.download_button(
        "Descargar respuestas.csv", csv_respuestas(diagnostico["respuestas"]),
        "respuestas.csv", "text/csv", width="stretch")
    col2.download_button(
        "Descargar resultados.csv", csv_resultados(diagnostico),
        "resultados.csv", "text/csv", width="stretch")

    st.markdown("""
    <div class="commercial"><h3>¿Qué significan estos resultados?</h3>
    <p>Este diagnóstico entrega una visión inicial del nivel de desarrollo de las prácticas de gestión y de los principales focos de pérdida que podrían estar afectando el desempeño de la organización. Las brechas identificadas pueden profundizarse mediante análisis de procesos, datos operacionales y observación en terreno.</p></div>
    """, unsafe_allow_html=True)
    st.button("Profundizar diagnóstico", disabled=True, width="stretch",
              help="Funcionalidad preparada para una futura versión.")
    st.caption("Este botón no envía información ni se conecta con servicios externos.")
    st.write("")
    st.button("Realizar nuevo diagnóstico", on_click=reiniciar_diagnostico, width="stretch")


inicializar_estado()
try:
    validar_configuracion(LOSSES)
except (ValueError, KeyError, TypeError) as error:
    st.error(f"Error en la configuración del diagnóstico: {error}")
    st.stop()

if st.session_state["pantalla"] == "inicio":
    mostrar_inicio()
elif st.session_state["pantalla"] == "cuestionario":
    mostrar_cuestionario()
elif st.session_state["pantalla"] == "resultados" and st.session_state["diagnostico"]:
    mostrar_resultados()
else:
    reiniciar_diagnostico()
    st.rerun()

"""Gráficos reutilizables del diagnóstico."""

import plotly.graph_objects as go

from questions import DIMENSIONS


AZUL = "#173B57"
TURQUESA = "#1D7A78"
NARANJA = "#D98B2B"


def crear_escala_madurez(nota):
    """Crea una escala horizontal de madurez entre 1 y 5."""
    figura = go.Figure(go.Indicator(
        mode="gauge+number", value=nota,
        number={"suffix": " / 5,00", "valueformat": ".2f", "font": {"size": 34, "color": AZUL}},
        gauge={
            "shape": "bullet",
            "axis": {"range": [1, 5], "tickvals": [1, 2, 3, 4, 5], "tickfont": {"size": 15}},
            "bar": {"color": AZUL, "thickness": 0.38}, "bgcolor": "white", "borderwidth": 0,
            "steps": [
                {"range": [1, 1.8], "color": "#F3D8D6"},
                {"range": [1.8, 2.6], "color": "#F6E5C8"},
                {"range": [2.6, 3.4], "color": "#F4EFC9"},
                {"range": [3.4, 4.2], "color": "#D9EADF"},
                {"range": [4.2, 5], "color": "#BFDCD8"},
            ],
            "threshold": {"line": {"color": NARANJA, "width": 5}, "value": nota},
        }, domain={"x": [0.04, 0.96], "y": [0.34, 0.86]},
    ))
    etiquetas = [(1.05, "Reactivo"), (2, "Básico"), (3, "Activo"),
                 (4, "Preventivo"), (4.92, "Excelencia<br>Operacional")]
    for x, texto in etiquetas:
        figura.add_annotation(x=x, y=0.12, xref="x", yref="paper", text=texto,
                              showarrow=False, font={"size": 13, "color": "#475569"})
    figura.update_xaxes(range=[1, 5], visible=False)
    figura.update_layout(height=225, margin=dict(l=20, r=20, t=10, b=35),
                         paper_bgcolor="white", separators=",.")
    return figura


def crear_radar(resultados_dimensiones):
    """Compara los resultados con el objetivo fijo de Excelencia Operacional."""
    etiquetas = ["Estandarización", "Adopción digital", "Control de procesos",
                 "Gestión del cliente", "Participación operativa", "Optimización de recursos"]
    valores = [resultados_dimensiones[dimension] for dimension in DIMENSIONS]
    theta = etiquetas + [etiquetas[0]]
    resultado = valores + [valores[0]]
    figura = go.Figure()
    figura.add_trace(go.Scatterpolar(
        r=resultado, theta=theta, fill="toself", name="Resultado de la empresa",
        line=dict(color=TURQUESA, width=4), fillcolor="rgba(29,122,120,0.25)",
        hovertemplate="%{theta}: %{r:.2f}<extra></extra>"))
    figura.add_trace(go.Scatterpolar(
        r=[5] * len(theta), theta=theta, name="Excelencia Operacional",
        line=dict(color=NARANJA, width=2, dash="dash"),
        hovertemplate="Objetivo: 5,00<extra></extra>"))
    figura.update_layout(
        title=dict(text="Brechas hacia la Excelencia Operacional", x=0.5, font=dict(size=24, color=AZUL)),
        polar=dict(bgcolor="#F8FAFC",
            radialaxis=dict(visible=True, range=[0, 5], tickvals=[0, 1, 2, 3, 4, 5],
                            gridcolor="#CBD5E1", tickfont=dict(size=13)),
            angularaxis=dict(gridcolor="#CBD5E1", tickfont=dict(size=14))),
        legend=dict(orientation="h", y=-0.16, x=0.5, xanchor="center", font=dict(size=14)),
        margin=dict(l=80, r=80, t=90, b=100), height=650,
        paper_bgcolor="white", separators=",.")
    return figura


def crear_grafico_brechas(brechas):
    """Muestra las seis brechas ordenadas de mayor a menor."""
    orden = sorted(brechas, key=brechas.get)
    valores = [brechas[dimension] for dimension in orden]
    figura = go.Figure(go.Bar(
        x=valores, y=orden, orientation="h", marker_color=NARANJA,
        text=[f"{valor:.2f}" for valor in valores], textposition="outside",
        hovertemplate="%{y}<br>Brecha: %{x:.2f}<extra></extra>"))
    figura.update_layout(
        xaxis=dict(range=[0, 4.2], title="Brecha respecto del nivel 5", gridcolor="#E2E8F0"),
        yaxis=dict(title=""), height=390, margin=dict(l=20, r=50, t=15, b=45),
        paper_bgcolor="white", plot_bgcolor="white", font=dict(size=14), separators=",.")
    return figura


def crear_visualizacion_perdidas(exposicion, matriz_perdidas):
    """Crea un mapa de barras para el árbol de pérdidas simplificado."""
    por_id = {perdida["id"]: perdida for perdida in matriz_perdidas}
    orden = sorted(exposicion, key=exposicion.get)
    valores = [exposicion[id_perdida] for id_perdida in orden]
    nombres = [por_id[id_perdida]["nombre"] for id_perdida in orden]
    colores = ["#4F9E91" if valor <= 1.6 else "#E0B04B" if valor <= 2.4
               else "#D97A45" if valor <= 3.2 else "#B84A4A" for valor in valores]
    figura = go.Figure(go.Bar(
        x=valores, y=nombres, orientation="h", marker_color=colores,
        text=[f"{valor:.2f}" for valor in valores], textposition="outside",
        hovertemplate="%{y}<br>Exposición orientativa: %{x:.2f} / 4<extra></extra>"))
    figura.update_layout(
        xaxis=dict(range=[0, 4.2], title="Exposición orientativa (0 = menor; 4 = mayor)",
                   tickvals=[0, 1, 2, 3, 4], gridcolor="#E2E8F0"),
        yaxis=dict(title="", automargin=True), height=max(400, 58 * len(orden)),
        margin=dict(l=20, r=55, t=20, b=55), paper_bgcolor="white",
        plot_bgcolor="white", font=dict(size=14), separators=",.")
    return figura

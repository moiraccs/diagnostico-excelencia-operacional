# Diagnóstico de Excelencia Operacional

Aplicación web local desarrollada con Python, Streamlit, Pandas y Plotly. Evalúa 12 preguntas en seis dimensiones, calcula el Índice de Excelencia Operacional, muestra brechas y genera un árbol de pérdidas simplificado con exposición orientativa.

## Qué incluye esta versión

- Portada profesional antes del cuestionario.
- Navegación paso a paso por seis dimensiones.
- Indicador de progreso y conservación de respuestas al avanzar o retroceder.
- Validación obligatoria de las 12 preguntas.
- Índice general, nivel de madurez y escala visual de 1 a 5.
- Radar de dimensiones y principales brechas.
- Árbol de pérdidas simplificado con escala de exposición de 0 a 4.
- Resumen ejecutivo automático basado exclusivamente en los resultados.
- Descarga de `respuestas.csv` y `resultados.csv`.

> **Importante:** la relación pregunta–pérdida incluida en `losses.py` es una matriz inicial y provisional para probar la plataforma. Debe reemplazarse por la matriz validada en la tesis antes de considerar definitivo el módulo de pérdidas.

## 1. Instalar Python

Instale **Python 3.11 o 3.12** desde [python.org](https://www.python.org/downloads/). En Windows marque **Add Python to PATH** durante la instalación.

Para comprobar la instalación:

```bash
python --version
```

## 2. Mantener juntos los archivos

```text
diagnostico_excelencia/
├── app.py
├── calculations.py
├── losses.py
├── questions.py
├── visualizations.py
├── requirements.txt
└── README.md
```

## 3. Abrir una terminal en la carpeta

En Windows, abra la carpeta en el Explorador de archivos, escriba `cmd` en la barra de dirección y presione Enter. También puede usar PowerShell o la terminal de Visual Studio Code.

## 4. Crear un entorno virtual (recomendado)

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 5. Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

## 6. Ejecutar la aplicación

```bash
python -m streamlit run app.py
```

La aplicación se abrirá normalmente en `http://localhost:8501`. Para detenerla presione `Ctrl + C` en la terminal.

## Dónde modificar cada elemento

### Preguntas, alternativas y dimensiones

Edite `questions.py`. Cada pregunta contiene `id`, `dimension`, `indicador`, `pregunta` y cinco alternativas. El orden de las alternativas determina automáticamente sus valores del 1 al 5.

### Pérdidas y relaciones

Edite `losses.py`. Cada pérdida contiene:

- `id`: identificador único;
- `nombre`: texto presentado en resultados;
- `descripcion`: explicación prudente del foco;
- `preguntas`: lista de identificadores relacionados;
- `dimensiones`: lista de dimensiones asociadas.

Una pregunta puede repetirse en varias pérdidas y una pérdida puede incluir varias preguntas. Cuando la matriz sea validada, cambie `MATRIZ_VALIDADA = False` a `MATRIZ_VALIDADA = True`.

### Puntos de corte y fórmulas

Edite `calculations.py`:

- `NIVELES_MADUREZ`: intervalos Reactivo–Excelencia Operacional;
- `NIVELES_EXPOSICION`: intervalos Baja–Muy alta;
- `calcular_exposicion_perdidas()`: fórmula del módulo de pérdidas;
- `calcular_dimensiones()`: cálculo de dimensiones;
- `calcular_excelencia_operacional()`: cálculo del índice general.

### Gráficos y colores

Edite `visualizations.py`. En la parte superior están los colores principales. Las funciones de radar, brechas y pérdidas están separadas.

### Interfaz y textos visibles

Edite `app.py`. Allí están la portada, navegación, tarjetas, resumen visual, descargas y estilos CSS.

## Interpretación de la exposición

La fórmula inicial es:

```text
exposición = 5 - promedio de las preguntas relacionadas
```

El resultado se limita a una escala entre 0 y 4. Es una señal diagnóstica: no confirma la existencia de una pérdida, no demuestra causalidad y no cuantifica impacto económico.

## Errores comunes

- **`python` no se reconoce:** reinstale Python marcando **Add Python to PATH** o utilice `py` en lugar de `python`.
- **`No module named streamlit`:** active el entorno virtual y ejecute `python -m pip install -r requirements.txt`.
- **No encuentra `questions`, `losses` o `calculations`:** confirme que todos los archivos estén en la misma carpeta.
- **Puerto 8501 ocupado:** ejecute `python -m streamlit run app.py --server.port 8502`.
- **Los cambios no aparecen:** guarde el archivo y elija **Rerun** en la aplicación, o reinicie Streamlit.
- **Error de configuración:** revise que las preguntas conserven valores 1–5 y que todos los identificadores usados en `losses.py` existan en `questions.py`.

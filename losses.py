"""Configuración editable del árbol de pérdidas simplificado.

Esta matriz es INICIAL Y PROVISIONAL para probar la plataforma. No representa
una relación causal ni una matriz científicamente validada. Sustituya nombres,
descripciones y asociaciones por la matriz validada en la tesis.
"""

MATRIZ_VALIDADA = False

# Una pregunta puede aparecer en varias pérdidas y una pérdida puede relacionarse
# con varias preguntas. Las dimensiones ayudan a explicar la asociación.
LOSSES = [
    {
        "id": "L1",
        "nombre": "Variabilidad en la ejecución del trabajo",
        "descripcion": "Posible exposición asociada a funciones poco claras o procesos que dependen de la experiencia individual.",
        "preguntas": [1, 2],
        "dimensiones": ["Estandarización de las operaciones"],
    },
    {
        "id": "L2",
        "nombre": "Pérdida de información y trazabilidad",
        "descripcion": "Posible exposición asociada a registros dispersos, manuales o con actualización insuficiente.",
        "preguntas": [3, 4, 6],
        "dimensiones": ["Adopción digital", "Control de procesos"],
    },
    {
        "id": "L3",
        "nombre": "Desviaciones operacionales no detectadas",
        "descripcion": "Foco que requiere revisión cuando el desempeño y las pérdidas no se controlan sistemáticamente.",
        "preguntas": [5, 6],
        "dimensiones": ["Control de procesos"],
    },
    {
        "id": "L4",
        "nombre": "Reclamos y disconformidades recurrentes",
        "descripcion": "Posible exposición relacionada con seguimiento limitado de reclamos y requerimientos del cliente.",
        "preguntas": [7, 8],
        "dimensiones": ["Gestión del cliente"],
    },
    {
        "id": "L5",
        "nombre": "Repetición de problemas",
        "descripcion": "Riesgo de pérdida que requiere revisión cuando las causas y soluciones no se analizan de forma organizada.",
        "preguntas": [6, 9, 10],
        "dimensiones": ["Control de procesos", "Participación operativa"],
    },
    {
        "id": "L6",
        "nombre": "Tiempo improductivo en resolución de problemas",
        "descripcion": "Posible exposición asociada a una resolución reactiva o con participación operativa limitada.",
        "preguntas": [9, 10],
        "dimensiones": ["Participación operativa"],
    },
    {
        "id": "L7",
        "nombre": "Recursos destinados sin priorización",
        "descripcion": "Foco de revisión relacionado con la selección y organización de recursos para mejorar procesos.",
        "preguntas": [5, 11],
        "dimensiones": ["Control de procesos", "Optimización de recursos"],
    },
    {
        "id": "L8",
        "nombre": "Demoras en la ejecución de mejoras",
        "descripcion": "Posible exposición asociada a mejoras sin responsables, seguimiento o agilidad suficiente.",
        "preguntas": [10, 11, 12],
        "dimensiones": ["Participación operativa", "Optimización de recursos"],
    },
]

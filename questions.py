"""Datos editables del cuestionario de Excelencia Operacional."""

DIMENSIONS = [
    "Estandarización de las operaciones",
    "Adopción digital",
    "Control de procesos",
    "Gestión del cliente",
    "Participación operativa",
    "Optimización de recursos",
]

def _options(*texts):
    """Convierte cinco textos ordenados en opciones con valores del 1 al 5."""
    return [{"valor": i, "texto": text} for i, text in enumerate(texts, start=1)]

QUESTIONS = [
    {"id": 1, "dimension": DIMENSIONS[0], "indicador": "Definición de funciones y responsabilidades",
     "pregunta": "¿Qué grado de definición y organización presentan las funciones y responsabilidades del personal?",
     "opciones": _options(
        "Las funciones y responsabilidades no están claramente definidas y las tareas se asignan según las necesidades del momento.",
        "El personal conoce sus principales funciones pero éstas se basan en indicaciones verbales o experiencia.",
        "Las principales funciones y responsabilidades están definidas y son conocidas por el personal.",
        "Las funciones y responsabilidades se revisan para evitar confusiones o tareas sin responsables.",
        "Cada trabajador tiene claras sus responsabilidades y puede realizar su trabajo sin necesitar instrucciones constantes.")},
    {"id": 2, "dimension": DIMENSIONS[0], "indicador": "Documentación formal de procesos clave",
     "pregunta": "¿Cómo se encuentran documentados y estandarizados los procesos claves de la empresa?",
     "opciones": _options(
        "Los procesos se realizan según la experiencia de cada trabajador y no se encuentran escritos.",
        "Existen algunas instrucciones o documentos pero sólo para ciertas actividades.",
        "Los procesos principales cuentan con procedimientos o instrucciones que orientan la forma de trabajar.",
        "Los procedimientos se revisan y se verifica que las actividades se realicen de acuerdo a lo establecido.",
        "Los procedimientos se mantienen actualizados y se mejoran a partir de los resultados.")},
    {"id": 3, "dimension": DIMENSIONS[1], "indicador": "Uso de herramientas tecnológicas para control de datos",
     "pregunta": "¿En qué medida se utilizan herramientas tecnológicas para registrar y controlar los datos de los procesos?",
     "opciones": _options(
        "Los datos no se registran regularmente o se mantienen principalmente en registros manuales.",
        "Se utilizan herramientas digitales básicas para algunos registros pero la información se encuentra separada o depende de cada trabajador.",
        "Se utilizan herramientas digitales de manera regular para registrar y organizar los datos importantes de los procesos.",
        "Las herramientas digitales permiten revisar datos e indicadores para detectar desviaciones o problemas de los procesos.",
        "Las herramientas digitales facilitan el seguimiento de los procesos y sus datos se utilizan para anticipar problemas y generar mejoras.")},
    {"id": 4, "dimension": DIMENSIONS[1], "indicador": "Disponibilidad de información para reportes de gestión",
     "pregunta": "¿En qué medida la empresa dispone de información actualizada para apoyar la gestión y toma de decisiones?",
     "opciones": _options(
        "La información se recopila cuando surge un problema o una necesidad específica.",
        "Existe información sobre los procesos pero no siempre está actualizada.",
        "La información relevante se encuentra organizada, disponible y actualizada.",
        "La información actualizada se revisa regularmente para controlar resultados.",
        "La información está disponible y se utiliza para anticipar situaciones, tomar decisiones y generar mejoras.")},
    {"id": 5, "dimension": DIMENSIONS[2], "indicador": "Uso de indicadores de desempeño en procesos",
     "pregunta": "¿En qué grado utilizan los indicadores para medir y controlar el desempeño de los procesos?",
     "opciones": _options(
        "No existen indicadores definidos y el desempeño se revisa cuando surge un problema.",
        "Se revisan algunos datos o resultados pero sin indicadores definidos.",
        "Existen indicadores definidos para los principales procesos y sus resultados se revisan.",
        "Los indicadores se monitorean para detectar desviaciones y tomar acciones.",
        "Los indicadores orientan la toma de decisiones y se utilizan para mejorar el desempeño del proceso.")},
    {"id": 6, "dimension": DIMENSIONS[2], "indicador": "Registro de errores, desperdicios, fallas e interrupciones operacionales",
     "pregunta": "¿Qué grado de registro y análisis existe sobre las pérdidas que ocurren durante la operación?",
     "opciones": _options(
        "Las pérdidas se atienden cuando ocurren pero generalmente no se registran.",
        "Algunas pérdidas son registradas.",
        "Las principales pérdidas se registran regularmente y se cuenta con información para analizarlas.",
        "Los registros se analizan para identificar pérdidas recurrentes, conocer sus causas y tomar acciones preventivas.",
        "Las pérdidas se analizan continuamente y la información se utiliza para eliminar sus causas y mejorar los procesos.")},
    {"id": 7, "dimension": DIMENSIONS[3], "indicador": "Registro de reclamos o quejas",
     "pregunta": "¿En qué medida se registran y utilizan los reclamos o quejas recibidas de los clientes?",
     "opciones": _options(
        "Los reclamos se atienden cuando ocurren pero no se registran regularmente.",
        "Algunos reclamos se registran pero de manera irregular y con poco seguimiento.",
        "Los reclamos se registran regularmente y se realiza el seguimiento de las situaciones informadas por los clientes.",
        "Los reclamos registrados se analizan para identificar problemas y tomar acciones.",
        "La información de los reclamos se utiliza continuamente para prevenir nuevos problemas y mejorar los productos, servicios o procesos.")},
    {"id": 8, "dimension": DIMENSIONS[3], "indicador": "Medición de cumplimiento según requerimientos",
     "pregunta": "¿En qué medida la empresa verifica que se cumplan los requerimientos acordados con sus clientes?",
     "opciones": _options(
        "El cumplimiento se revisa cuando el cliente informa un problema o manifiesta disconformidad.",
        "Algunos requerimientos se verifican pero de manera informal sin mantener registros.",
        "Los principales requerimientos acordados con los clientes están definidos y su cumplimiento se verifica regularmente.",
        "El cumplimiento se controla para detectar desviaciones y corregirlas antes de que afecten al cliente.",
        "El cumplimiento se revisa continuamente y sus resultados se utilizan para anticipar necesidades y mejorar el servicio entregado.")},
    {"id": 9, "dimension": DIMENSIONS[4], "indicador": "Participación del personal en la solución de problemas",
     "pregunta": "¿Qué grado de participación tiene el personal en la identificación y solución de problemas relacionados con su trabajo?",
     "opciones": _options(
        "Los problemas son resueltos principalmente por supervisores o jefaturas.",
        "Los trabajadores informan los problemas y ocasionalmente proponen soluciones pero la decisión depende de la jefatura.",
        "Los trabajadores participan regularmente en identificación de problemas y búsqueda de soluciones.",
        "Los trabajadores participan en el análisis de las causas y proponen acciones para evitar que los problemas vuelvan a ocurrir.",
        "Los trabajadores identifican, solucionan y previenen problemas de manera activa, aportando a la mejora de su trabajo.")},
    {"id": 10, "dimension": DIMENSIONS[4], "indicador": "Existencia de dinámicas de resolución de problemas",
     "pregunta": "¿Qué tan organizada está la forma de resolver problemas ocurridos en el trabajo?",
     "opciones": _options(
        "Los problemas se resuelven cuando ocurren para continuar con el trabajo lo antes posible.",
        "Algunos problemas se revisan para buscar soluciones.",
        "Existe una forma definida para analizar los problemas, identificar sus causas y establecer acciones.",
        "Se realiza seguimiento a las soluciones implementadas para comprobar sus resultados.",
        "Cuando la solución funciona se incorpora a la forma de trabajar y se aplica en otras situaciones similares para prevenir el mismo problema.")},
    {"id": 11, "dimension": DIMENSIONS[5], "indicador": "Implementación de mejoras con los recursos disponibles",
     "pregunta": "¿Qué tan bien se aprovechan los recursos disponibles para realizar mejoras en los procesos?",
     "opciones": _options(
        "Los recursos disponibles se utilizan para resolver las necesidades inmediatas y rara vez para realizar mejoras.",
        "Algunos recursos disponibles se aprovechan para realizar pequeñas mejoras cuando surge una necesidad.",
        "Los recursos disponibles se organizan y utilizan regularmente para realizar mejoras en los procesos.",
        "Los recursos se priorizan considerando los problemas detectados y las mejoras que pueden generar beneficios.",
        "La empresa busca continuamente nuevas formas de aprovechar mejor sus recursos para mejorar los procesos y resultados.")},
    {"id": 12, "dimension": DIMENSIONS[5], "indicador": "Agilidad para ejecutar mejoras",
     "pregunta": "¿Con qué facilidad se llevan a cabo las mejoras en los procesos?",
     "opciones": _options(
        "Las mejoras rara vez se llevan a cabo y los cambios se realizan cuando existe un problema urgente.",
        "Algunas mejoras se realizan pero suelen demorarse por la falta de coordinación o seguimiento.",
        "Las mejoras se organizan, tienen responsables y se llevan a cabo.",
        "Las mejoras se priorizan, se realizan y se revisan sus resultados.",
        "Las mejoras se llevan a cabo con agilidad, se evalúan sus resultados y aquellas que funcionan se incorporan de forma habitual.")},
]

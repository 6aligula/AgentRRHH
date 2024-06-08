# Evaluación de Modelos de IA para la Evaluación de Candidatos

Este repositorio contiene una evaluación comparativa de varios modelos de IA utilizados para evaluar la experiencia laboral de candidatos y generar puntuaciones basadas en dicha experiencia.

## Prueba con el modelo phi3:mini

### Pregunta

```bash
¿Cuál es la puntuación del candidato?
```

### Respuesta

```bash
Asistente: {
    "puntuacion": 40,
    "experiencia": [
        {
            "puesto": "Coordinador de Promociones y Ofertas",
            "empresa": "Nombre de la Empresa",
            "duración": "Duración del puesto"
        },
        {
            "puesto": "Encargado de Gestión de Residuos y Reciclaje",
            "empresa": "Nombre de la Empresa",
            "duración": "Duración del puesto"
        }
    ],
    "descripcion": "El candidato posee experiencia en roles que están relacionados con las habilidades y responsabilidades requeridas por el puesto propuesto. Como Coordinador de Promociones y Ofertas, demostró habilidades para coordinar eventos y actividades promocionales, lo cual puede ser relevante en la gestión de campañas de marketing o relaciones con clientes. En su rol como Encargado de Gestión de Residuos y Reciclaje, el candidato pudo desarrollar habilidades organizativas y responsabilidad ambiental, que aunque no directamente relacionadas al puesto propuesto, reflejan una disposición para la gestión eficiente y un compromiso con prácticas sostenibles."
} 

Tú: salir
¡Hasta luego!
```

### Pregunta 

```bash
¿Cuál es la puntuación del candidato?
```

### Respuesta

```bash
Asistente: {
    "puntuacion": 25,
    "experiencia": [
        {
            "puesto": "Coordinador de Promociones y Ofertas",
            "empresa": "Supermercado XYZ",
            "duración": "6 meses"
        },
        {
            "puesto": "Encargado de Gestión de Residuos y Reciclaje",
            "empresa": "Supermercado ABC",
            "duración": "3 meses"
        }
    ],
    "descripcion": "El candidato ha demostrado experiencia en el sector de supermercados, destacando su papel como Coordinador de Promociones y Ofertas en Supermercado XYZ y como Encargado de Gestión de Residuos y Reciclaje en Supermercado ABC. Su participación se centró en la gestión de actividades comerciales y sostenibilidad ambiental, respectivamente. Esto refleja una comprensión práctica del manejo de inventarios, atención al cliente y soluciones de marketing dentro del contexto supermercadista."
} 
```

**Conclusión:** El modelo presenta inconsistencias y genera respuestas alucinadas.

## Prueba con el modelo llama3 de 4,7GB

### Pregunta

```bash
¿Cuál es la puntuación del candidato?
```

### Respuesta

```bash
Respuesta en bruto del modelo: A continuación, se presenta la evaluación del candidato para el puesto de encargado de supermercado:

{
    "puntuacion": 25,
    "experiencia": [
        {
            "puesto": "Coordinador de Promociones y Ofertas",
            "empresa": "Compañía XYZ",
            "duración": "2 años"
        },
        {
            "puesto": "Encargado de Gestión de Residuos y Reciclaje",
            "empresa": "Supermercado ABC",
            "duración": "1 año 6 meses"
        }
    ],
    "descripcion": "El candidato tiene experiencia en coordinar promociones y ofertas, lo que demuestra su capacidad para gestionar recursos y lograr objetivos. Además, ha demostrado habilidades en la gestión de residuos y reciclaje en un supermercado, lo que sugiere que es consciente de las responsabilidades ambientales y sociales en la gestión de una tienda."
}

La puntuación se basa en la experiencia laboral del candidato, que tiene 2 años y 6 meses en total. Los 10 puntos se asignan por el puesto de Coordinador de Promociones y Ofertas, ya que está relacionado con la gestión de tiendas/supermercados. Los otros 15 puntos se asignan por el puesto de Encargado de Gestión de Residuos y Reciclaje, ya que también está relacionado con la gestión de tiendas/supermercados y demuestra habilidades en la gestión de recursos y lograr objetivos.

La descripción de la experiencia destaca las habilidades del candidato en la coordinación de promociones y ofertas, así como su capacidad para gestionar residuos y reciclaje de manera efectiva.
```

**Conclusión:** El modelo sigue mostrando alucinaciones y falta de precisión.


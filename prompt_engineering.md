# Pregunta probando el modelo phi3:mini

```{bash}
¿Cuál es la puntuación del candidato?
```

# Respuesta

```{bash}
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

# Pregunta 

```{bash}
¿Cuál es la puntuación del candidato?
```

# Respuesta

```{bash}
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
**Claramente el modelo esta alucinando**

# Pregunta probando el modelo llama3 de 4,7GB

```{bash}
¿Cuál es la puntuación del candidato?
```

# Respuesta

```{bash}
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

**sigue alucinando**
-------------------------------------------------------------------------------------------------------------------------------

# Pregunta usando el modelo gpt-4o de openai

```{bash}
¿Cuál es la puntuación del candidato?
```

# Respuesta

```{bash}
json
{
    "puntuacion": 65,
    "experiencia": [
        {
            "puesto": "Reponedor",
            "empresa": "GRUPO SUPECO MAXOR S.L.",
            "duración": "09/2021 - 03/2022"
        },
        {
            "puesto": "Mozo de almacén y manipulador de cartón",
            "empresa": "ENCUNY S.L.",
            "duración": "02/2020 - 08/2021"
        },
        {
            "puesto": "Responsable de cocina",
            "empresa": "AREAS S.A.U.",
            "duración": "08/2018 - 02/2019"
        }
    ],
    "descripcion": "Andrés F. Uribe tiene experiencia relevante en roles de reponedor y mozo de almacén, lo cual es útil para la gestión de inventarios y stock en un supermercado. Sin embargo, no tiene experiencia directa en puestos de liderazgo o gestión de equipos en un entorno de supermercado, lo que limita su puntuación en experiencia laboral. En cuanto a habilidades y competencias, Andrés muestra conocimientos en logística y coordinación de almacén, así como en atención al cliente y resolución de conflictos, pero carece de experiencia en liderazgo y ventas. Su formación académica se limita a un graduado en ESO, sin cursos adicionales relevantes para el puesto. En conocimientos técnicos, no se menciona manejo de software de gestión de tiendas o herramientas de análisis de datos. En resumen, Andrés tiene una base sólida en operaciones y logística, pero carece de experiencia y formación en liderazgo y gestión específica para un puesto de encargado de supermercado."
}
```
El modelo me responde con un formato markdown ```{json} response``` de lo que puedo deducir que esta totalmente preprado para ser consumido por un front.

**Ajusto al modelo para que responda solo con el formato json deseado**

## Nuevo prompt 

```{bash}
Genera una respuesta en formato JSON que contenga la siguiente información, sin comillas de markdown, solo siñete al formato json especificado
```

# Respuesta

```{bash}
{
    "puntuacion": 65,
    "experiencia": [
        {
            "puesto": "Reponedor",
            "empresa": "GRUPO SUPECO MAXOR S.L.",
            "duración": "09/2021 - 03/2022"
        },
        {
            "puesto": "Mozo de almacén y manipulador de cartón",
            "empresa": "ENCUNY S.L.",
            "duración": "02/2020 - 08/2021"
        },
        {
            "puesto": "Responsable de cocina",
            "empresa": "AREAS S.A.U.",
            "duración": "08/2018 - 02/2019"
        }
    ],
    "descripcion": "Andrés F. Uribe V. tiene una experiencia laboral variada, con roles que incluyen reponedor, mozo de almacén y responsable de cocina. Aunque no ha ocupado directamente un puesto de encargado de supermercado, ha demostrado habilidades relevantes como gestión de inventarios, control de calidad y liderazgo en sus roles anteriores. Su experiencia en GRUPO SUPECO MAXOR S.L. como reponedor y en ENCUNY S.L. como mozo de almacén y manipulador de cartón le ha proporcionado conocimientos en logística y coordinación de almacén. Además, su rol como responsable de cocina en AREAS S.A.U. le ha permitido desarrollar habilidades de liderazgo y gestión de equipos. Sin embargo, carece de formación académica específica en áreas como administración de empresas o gestión comercial, lo que limita su puntuación en ese criterio. En general, Andrés muestra potencial para el puesto de encargado de supermercado, pero necesitaría formación adicional y experiencia directa en roles de supervisión en el sector."
} 
```
**El modelo gpt-4o ha demostrado ser totalmente capacitado para esta tarea a un precio de 1 centimo por cada interacción.**

# Pregunta usando el modelo gpt-3.5-turbo

```{bash}
¿Cuál es la puntuación del candidato?
```

# Respuesta

```{bash}
{
    "puntuacion": 65,
    "experiencia": [
        {
            "puesto": "Mozo de almacén y manipulador de cartón",
            "empresa": "ENCUNY S.L.",
            "duración": "02/2020 - 08/2021"
        },
        {
            "puesto": "Reponedor",
            "empresa": "ENCUNY S.L.",
            "duración": "09/2021 - 03/2022"
        },
        {
            "puesto": "Oficial de encoladora packaging y manipulador profesional de cartón",
            "empresa": "ENCUNY S.L. GRUPO SUPECO MAXOR S.L.",
            "duración": "03/2022 - 02/2024"
        }
    ],
    "descripcion": "El candidato cuenta con experiencia relevante en el sector de supermercados y logística, habiendo desempeñado roles como mozo de almacén, manipulador de cartón, reponedor y oficial de encoladora packaging. Su experiencia en ENCUNY S.L. y GRUPO SUPECO MAXOR S.L. demuestra su capacidad para gestionar inventarios, coordinar equipos y cumplir con normativas de calidad. Además, posee habilidades en logística, control de stock y seguridad alimentaria. Aunque su formación académica no incluye un grado universitario relacionado, sus conocimientos técnicos y habilidades prácticas lo hacen un candidato adecuado para el puesto de encargado de supermercado."
} 
```

# Conclusión

**Precisión en la Experiencia Laboral:**

 - GPT-4 es más preciso en listar las empresas y los roles correctos, de acuerdo con la información proporcionada en el CV.
 - GPT-3.5-turbo tiene errores en la asignación de empresas para ciertos roles.

**Calidad de la Descripción:**

 - GPT-4 proporciona una evaluación más crítica y completa de las cualificaciones del candidato, incluyendo la necesidad de formación adicional.
 - GPT-3.5-turbo ofrece una evaluación positiva pero omite detalles importantes como la falta de formación específica y la necesidad de formación adicional.
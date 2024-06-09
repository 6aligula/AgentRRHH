import json
import requests

LOCAL_API_URL = "http://localhost:11434/api/chat"

def probar_modelo_local(prompt):
    messages = [
        {"role": "system", "content": "Eres un experto en selección de personal"},
        {"role": "user", "content": prompt}
    ]
    
    # Realizar la petición al modelo local
    response = requests.post(
        LOCAL_API_URL,
        headers={"Content-Type": "application/json"},
        json={"model": "llama3", "messages": messages}
    )
    
    # Imprimir la respuesta completa
    print("Estado de la respuesta:", response.status_code)
    print("Contenido de la respuesta:", response.text)
    
    # Intentar parsear la respuesta como JSON
    try:
        response_json = response.json()
        print("Respuesta JSON parseada:", json.dumps(response_json, indent=4))
    except json.JSONDecodeError as e:
        print(f"Error decodificando JSON: {e}")
        print(f"Respuesta completa: {response.text}")

# Crear un prompt de prueba
prompt_de_prueba = """Usa la siguiente información para evaluar al candidato.

Contexto del CV del candidato: John Doe tiene experiencia en gestión de supermercados durante 10 años.
Contexto de la oferta de trabajo: encargado de supermercado
Contextos adicionales relevantes: La empresa busca un encargado con habilidades en gestión de personal y optimización de inventarios.

Para evaluar al candidato, considera los siguientes criterios y asigna una puntuación en base a ellos.

Genera una respuesta en formato JSON que contenga la siguiente información, sin añadir las comillas de markdown.
a. Valor numérico con la puntuación de 0 a 100 según la experiencia y los otros criterios mencionados.
b. Listado de la experiencia: Debe devolver un listado con las experiencias que son relacionadas a la oferta propuesta, este listado debe contener la siguiente información de cada experiencia: Puesto, Empresa y duración.
c. Descripción de la experiencia: Debe devolver un texto explicativo sobre la experiencia del candidato y por qué ha obtenido la puntuación dada.

Respuesta JSON:
{
    "puntuacion": <valor_numérico>,
    "experiencia": [
        {
            "puesto": "<puesto>",
            "empresa": "<empresa>",
            "duración": "<duración>"
        }
    ],
    "descripcion": "<descripción>"
}
"""

# Probar el modelo local con el prompt de prueba
probar_modelo_local(prompt_de_prueba)

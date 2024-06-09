import json
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from uploadData import cargar_documentos, crear_vectorstore, leer_pdf
from openai import OpenAI
import requests

# Códigos de escape ANSI para colores
AZUL = "\033[94m"
VERDE = "\033[92m"
RESET = "\033[0m"

# Cargar variables de entorno desde el archivo .env
load_dotenv()

def obtener_input_usuario(prompt):
    """
    Solicita y devuelve la entrada del usuario después de verificar que no esté vacía.
    """
    while True:
        entrada = input(f"{AZUL}{prompt}:{RESET} ").strip()
        if entrada:
            return entrada
        else:
            print("La entrada no puede estar vacía. Inténtalo de nuevo.")

def leer_cv(ruta_cv):
    """
    Lee el contenido del CV desde un archivo de texto.
    """
    with open(ruta_cv, 'r', encoding='utf-8') as file:
        cv_completo = file.read()
    return cv_completo

def cargar_multiples_documentos(rutas_archivos):
    """
    Carga múltiples documentos desde las rutas especificadas.
    """
    documentos = []
    for ruta in rutas_archivos:
        if ruta.endswith('.pdf'):
            documentos.append(leer_pdf(ruta))
        else:
            documentos.extend(cargar_documentos(ruta))
    return documentos

def cargar_datos():
    oferta = "encargado de supermercado"
    cv_completo = leer_cv("cv.txt")
    rutas_archivos = [
            "src/Lista_Trabajos_Relacionados_Encargado_Supermercado.pdf",
            "src/Sistema_de_Puntuacion.pdf"
        ]
    contextos_adicionales = cargar_multiples_documentos(rutas_archivos)
    
    if not oferta or not cv_completo:
        raise ValueError("Las claves 'oferta' y 'cv' no pueden estar vacías.")
    
    return oferta, cv_completo, contextos_adicionales

def configurar_vectorstore():
    embed_model = FastEmbedEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vectorstore = Chroma(embedding_function=embed_model,
                         persist_directory="chroma_db_dir",
                         collection_name="cv_data")
    
    total_rows = len(vectorstore.get()['ids'])
    if total_rows == 0:
        rutas_archivos = [
            "src/Lista_Trabajos_Relacionados_Encargado_Supermercado.pdf",
            "src/Sistema_de_Puntuacion.pdf"
        ]
        docs = cargar_multiples_documentos(rutas_archivos)
        vectorstore = crear_vectorstore(docs)
    
    retriever = vectorstore.as_retriever(search_kwargs={'k': 4})
    return retriever

def crear_prompt(cv_completo, oferta, contextos_adicionales):
    contextos_adicionales_texto = "\n".join(contextos_adicionales)

    return f"""Usa la siguiente información para evaluar al candidato.

Contexto del CV del candidato: {cv_completo}
Contexto de la oferta de trabajo: {oferta}
Contextos adicionales relevantes: {contextos_adicionales_texto}

Para evaluar al candidato, considera los siguientes criterios y asigna una puntuación en base a ellos.

Genera una respuesta en formato JSON que contenga la siguiente información, sin añadir las comillas de markdown.
a. Valor numérico con la puntuación de 0 a 100 según la experiencia y los otros criterios mencionados.
b. Listado de la experiencia: Debe devolver un listado con las experiencias que son relacionadas a la oferta propuesta, este listado debe contener la siguiente información de cada experiencia: Puesto, Empresa y duración.
c. Descripción de la experiencia: Debe devolver un texto explicativo sobre la experiencia del candidato y por qué ha obtenido la puntuación dada.

Respuesta JSON:
{{
    "puntuacion": <valor_numérico>,
    "experiencia": [
        {{
            "puesto": "<puesto>",
            "empresa": "<empresa>",
            "duración": "<duración>"
        }}
    ],
    "descripcion": "<descripción>"
}}
"""


#MODEL="gpt-4o"
MODEL="gpt-3.5-turbo"
LOCAL_API_URL = "http://localhost:11434/api/chat"

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as an env var>"))

def parse_ollama_response(response):
    try:
        for line in response.iter_lines():
            if line:
                obj = json.loads(line.decode('utf-8'))
                if 'message' in obj and 'content' in obj['message']:
                    yield obj['message']['content']
    except Exception as e:
        print(f"Error procesando la respuesta: {e}")

def obtener_respuesta(prompt, usar_modelo_local=False):
    messages = [
        {"role": "system", "content": "Eres un experto en selección de personal"},
        {"role": "user", "content": prompt}
    ]
    
    if usar_modelo_local:
        response = requests.post(
            LOCAL_API_URL,
            headers={"Content-Type": "application/json"},
            json={"model": "phi3:mini", "messages": messages},
            stream=True
        )
        return parse_ollama_response(response)
    else:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=500,
            temperature=0
        )
        return response.choices[0].message.content
    
def obtener_respuesta_con_barra_de_carga(prompt, usar_modelo_local):
    with ThreadPoolExecutor() as executor:
        future = executor.submit(obtener_respuesta, prompt, usar_modelo_local)
        with tqdm(total=100, desc="Generando respuesta", bar_format="{l_bar}{bar} [ tiempo restante: {remaining} ]") as pbar:
            while not future.done():
                time.sleep(0.1)  # Simulate work being done
                pbar.update(1)
                if pbar.n >= 100:
                    pbar.n = 0  # Reset the progress bar
                    pbar.last_print_n = 0
            pbar.update(100 - pbar.n)  # Ensure it completes at 100%
        return future.result()

def mostrar_respuesta_en_tiempo_real(response_stream):
    respuesta_completa = ""
    for parte_respuesta in response_stream:
        print(parte_respuesta, end="", flush=True)
        respuesta_completa += parte_respuesta
    return respuesta_completa

def iniciar_chat(oferta, cv_completo, contextos_adicionales, usar_modelo_local=False):
    print("¡Bienvenido al chat!")
    pregunta = "¿Cuál es la puntuación del candidato?"

    try:
        prompt = crear_prompt(cv_completo, oferta, contextos_adicionales)
        print(f"{AZUL}Tú:{RESET} {pregunta}")

        if usar_modelo_local:
            respuesta_stream = obtener_respuesta(prompt, usar_modelo_local)
            respuesta = mostrar_respuesta_en_tiempo_real(respuesta_stream)
        else:
            respuesta = obtener_respuesta_con_barra_de_carga(prompt, usar_modelo_local)

        try:
            resultado_json = json.loads(respuesta)
        except json.JSONDecodeError:
            print(f"{VERDE}Error:{RESET} La respuesta del modelo no es un JSON válido.")
            print(f"{VERDE}Respuesta en bruto del modelo después del error:{RESET} {respuesta}")
            return

        print(f"{VERDE}Asistente:{RESET}", json.dumps(resultado_json, indent=4, ensure_ascii=False), '\n')
    except ValueError as ve:
        print(f"{VERDE}Error:{RESET} {str(ve)}")
    except Exception as e:
        print(f"{VERDE}Error inesperado, añade al fichero .env: OPENAI_API_KEY=tu-api-key:{RESET} {str(e)}")

          

if __name__ == "__main__":
    try:
        oferta, cv_completo, contextos_adicionales = cargar_datos()
        print(f"{AZUL}Oferta:{RESET} {oferta}\n")
        # Determinar si usar modelo local o no
        usar_modelo_local = obtener_input_usuario("¿Deseas usar el modelo local? (s/n)").lower() == 's'
        iniciar_chat(oferta, cv_completo, contextos_adicionales, usar_modelo_local)
    except Exception as e:
        print(f"{VERDE}Error inicializando el chat:{RESET} {str(e)}")

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

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as an env var>"))

def obtener_respuesta(prompt):
    # Define los mensajes del chat
    messages = [
        {"role": "system", "content": "Eres un experto en selección de personal"},
        {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=500,
        temperature=0
    )
    return response.choices[0].message.content


def iniciar_chat(oferta, cv_completo, contextos_adicionales):
    print("¡Bienvenido al chat!")
    pregunta = "¿Cuál es la puntuación del candidato?"

    try:
        prompt = crear_prompt(cv_completo, oferta, contextos_adicionales)
        print(f"{AZUL}Tú:{RESET} {pregunta}")

        # Start the progress animation
        with ThreadPoolExecutor() as executor:
            future = executor.submit(obtener_respuesta, prompt)
            with tqdm(total=100, desc="Generando respuesta", bar_format="{l_bar}{bar} [ tiempo restante: {remaining} ]") as pbar:
                while not future.done():
                    time.sleep(0.1)  # Simulate work being done
                    pbar.update(1)
                    if pbar.n >= 100:
                        pbar.n = 0  # Reset the progress bar
                        pbar.last_print_n = 0
                pbar.update(100 - pbar.n)  # Ensure it completes at 100%

        respuesta = future.result()
        
        # Parse the response
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
        print(f"{VERDE}Error inesperado:{RESET} {str(e)}")
          

if __name__ == "__main__":
    try:
        oferta, cv_completo, contextos_adicionales = cargar_datos()
        print(print(f"{AZUL}Oferta:{RESET} {oferta}\n"))
        iniciar_chat(oferta, cv_completo, contextos_adicionales)
    except Exception as e:
        print(f"{VERDE}Error inicializando el chat:{RESET} {str(e)}")

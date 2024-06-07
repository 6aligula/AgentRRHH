import json
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from uploadData import cargar_documentos, crear_vectorstore
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
import time
from tqdm import tqdm
import threading
from concurrent.futures import ThreadPoolExecutor

# Códigos de escape ANSI para colores
AZUL = "\033[94m"
VERDE = "\033[92m"
RESET = "\033[0m"

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
        documentos.extend(cargar_documentos(ruta))
    return documentos

def cargar_datos():
    #oferta = obtener_input_usuario("Introduce el nombre de la oferta de trabajo")
    oferta = "encargado de supermercado"
    cv_completo = leer_cv("cv.txt")
    
    if not oferta or not cv_completo:
        raise ValueError("Las claves 'oferta' y 'cv' no pueden estar vacías.")
    
    return oferta, cv_completo

def configurar_modelo():
    llm = Ollama(model="phi3:mini")
    embed_model = FastEmbedEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vectorstore = Chroma(embedding_function=embed_model,
                         persist_directory="chroma_db_dir",
                         collection_name="cv_data")
    
    total_rows = len(vectorstore.get()['ids'])
    if total_rows == 0:
        rutas_archivos = [
            "src/Ejemplo_Sistema_de_Puntuacion_Experiencia.pdf",
            "src/Lista_Trabajos_Relacionados_Encargado_Supermercado.pdf",
            "src/Sistema_de_Puntuacion.pdf"
        ]
        docs = cargar_multiples_documentos(rutas_archivos)
        vectorstore = crear_vectorstore(docs)
    
    retriever = vectorstore.as_retriever(search_kwargs={'k': 4})
    return llm, retriever

def crear_qa_chain(llm, retriever):
    custom_prompt_template = """Usa la siguiente información para evaluar el CV del candidato.

Contexto: {context}
Pregunta: {question}

Genera una respuesta en formato JSON que contenga la siguiente información:
a. Valor numérico con la puntuación de 0 a 100 según la experiencia: Se debe tener en cuenta sólo los puestos de trabajo relacionados con el del título aportado, por ejemplo, no debe contar la experiencia como repartidor para un puesto de cajero.
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
    prompt = PromptTemplate(template=custom_prompt_template, input_variables=['context', 'question'])

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )
    
    return qa

def iniciar_chat(qa, oferta, cv_completo):
    print("¡Bienvenido al chat! Escribe 'salir' para terminar.")
    
    def get_response(inputs):
        return qa.invoke(inputs)

    while True:
        pregunta = input(f"{AZUL}Tú:{RESET} ")
        if pregunta.lower() == 'salir':
            print("¡Hasta luego!")
            break

        try:
            context = f"CV completo: {cv_completo}\nOferta de trabajo: {oferta}"
            inputs = {
                "query": pregunta,
                "context": context
            }
            
            # Debug prints
            print(f"Inputs: {inputs}")

            # Start the progress animation
            with ThreadPoolExecutor() as executor:
                future = executor.submit(get_response, inputs)
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
                resultado_json = json.loads(respuesta['result'])
            except json.JSONDecodeError:
                print(f"{VERDE}Error:{RESET} La respuesta del modelo no es un JSON válido.")
                continue

            print(f"{VERDE}Asistente:{RESET}", json.dumps(resultado_json, indent=4, ensure_ascii=False), '\n')
        except ValueError as ve:
            print(f"{VERDE}Error:{RESET} {str(ve)}")
        except Exception as e:
            print(f"{VERDE}Error inesperado:{RESET} {str(e)}")
            

if __name__ == "__main__":
    try:
        oferta, cv_completo = cargar_datos()
        #print(f"CV:\n{cv_completo[:100]}...\n")  # Muestra las primeras 100 caracteres para verificación
        #print(f"La oferta es {oferta}\n")

        llm, retriever = configurar_modelo()
        qa = crear_qa_chain(llm, retriever)
        iniciar_chat(qa, oferta, cv_completo)
    except Exception as e:
        print(f"{VERDE}Error inicializando el chat:{RESET} {str(e)}")

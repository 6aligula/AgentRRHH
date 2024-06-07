import json
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from uploadData import cargar_documentos, crear_vectorstore
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

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
    try:
        with open(ruta_cv, 'r', encoding='utf-8') as file:
            cv_completo = file.read()
        print(f"CV leído correctamente:\n{cv_completo[:100]}...")  # Muestra las primeras 100 caracteres para verificación
        return cv_completo
    except Exception as e:
        print(f"Error leyendo el CV desde {ruta_cv}: {e}")
        return ""

def cargar_multiples_documentos(rutas_archivos):
    """
    Carga múltiples documentos desde las rutas especificadas.
    """
    documentos = []
    for ruta in rutas_archivos:
        documentos.extend(cargar_documentos(ruta))
    return documentos

def cargar_datos():
    oferta = obtener_input_usuario("Introduce el nombre de la oferta de trabajo")
    cv_completo = leer_cv("cv.txt")
    print(f"Oferta:\n{oferta}\n")
    print(f"CV:\n{cv_completo[:100]}...")  # Muestra las primeras 100 caracteres para verificación
    
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
    Oferta de trabajo: {oferta}
    CV del candidato: {cv}

    Contexto: {context}
    Pregunta: {query}

    Genera una respuesta en formato JSON que contenga la siguiente información:
    a. Valor numérico con la puntuación de 0 a 100 según la experiencia: Se debe tener en cuenta sólo los puestos de trabajo relacionados con el del título aportado, por ejemplo, no debe contar la experiencia como repartidor para un puesto de cajero.
    b. Listado de la experiencia: Debe devolver un listado con las experiencias que son relacionadas a la oferta propuesta, este listado debe contener la siguiente información de cada experiencia: Puesto, Empresa y duración.
    c. Descripción de la experiencia: Debe devolver un texto explicativo sobre la experiencia del candidato y por qué ha obtenido la puntuación dada.

    Respuesta JSON:
    """
    prompt = PromptTemplate(template=custom_prompt_template, input_variables=['oferta', 'cv', 'context', 'query'])

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
    while True:
        pregunta = input(f"{AZUL}Tú:{RESET} ")
        if pregunta.lower() == 'salir':
            print("¡Hasta luego!")
            break

        try:
            inputs = {
                "query": pregunta,
                "oferta": oferta,
                "cv": cv_completo,
                "context": ""
            }
            
            # Debug prints
            print(f"Inputs: {inputs}")

            respuesta = qa.invoke(inputs)
            
            metadata = []
            for doc in respuesta['source_documents']:
                metadata.append(('page: ' + str(doc.metadata['page']), doc.metadata['file_path']))
            resultado_json = {
                "puntuacion": respuesta['result'],
                "trabajos_relacionados": metadata,
                "descripcion": "Descripción de la evaluación basada en la oferta de trabajo y el CV."
            }
            print(f"{VERDE}Asistente:{RESET}", json.dumps(resultado_json, indent=4, ensure_ascii=False), '\n')
        except ValueError as ve:
            print(f"{VERDE}Error:{RESET} {str(ve)}")
        except Exception as e:
            print(f"{VERDE}Error inesperado:{RESET} {str(e)}")

if __name__ == "__main__":
    try:
        oferta, cv_completo = cargar_datos()
        llm, retriever = configurar_modelo()
        qa = crear_qa_chain(llm, retriever)
        iniciar_chat(qa, oferta, cv_completo)
    except Exception as e:
        print(f"{VERDE}Error inicializando el chat:{RESET} {str(e)}")

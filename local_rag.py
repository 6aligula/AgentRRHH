from langchain_community.llms import Ollama

llm = Ollama(model="llama3")

# response = llm.invoke("Hola, quien eres?")

#print(response)

# load pdf in parts
from langchain_community.document_loaders import PyMuPDFLoader

loader = PyMuPDFLoader("src/CV_Andres_2024.pdf")
data_pdf = loader.load()
#print(data_pdf[0])

# chunk pdfs 
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=50)
docs = text_splitter.split_documents(data_pdf)
# print(f"primera parte:\n {docs[0]} \n")
# print("segunnda parte \n")
# print(docs[1])

# create embedings form the last chung
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
embed_model = FastEmbedEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# chroma database for ewmbedings
from langchain_community.vectorstores import Chroma
vs = Chroma.from_documents(
    documents=docs,
    embedding=embed_model,
    persist_directory="chroma_db_dir",  # Local mode with in-memory storage only
    collection_name="cv_data"
)
vectorstore = Chroma(embedding_function=embed_model,
                     persist_directory="chroma_db_dir",
                     collection_name="cv_data")
retriever=vectorstore.as_retriever(search_kwargs={'k': 3}) # numero de chunks que devuelve es 3

#creando el prompt

from langchain.prompts import PromptTemplate

custom_prompt_template = """Usa la siguiente información para responder a la pregunta del usuario.
Si no sabes la respuesta, di que no lo se, no inventes una respuesta.

Contexto: {context}
Pregunta: {question}

Solo devuelve la respuesta útil a continuación y nada más
Respuesta útil:
"""
prompt = PromptTemplate(template=custom_prompt_template,
                        input_variables=['context', 'question'])

# hacer un retreival para construir question y answer contra el modelo ollama 3
from langchain.chains import RetrievalQA

qa = RetrievalQA.from_chain_type(llm=llm,
                                 chain_type="stuff",
                                 retriever=retriever,
                                 return_source_documents=True,
                                 chain_type_kwargs={"prompt": prompt})

response = qa.invoke({"query": "Según el currículum adjunto, ¿puedes listar todos los trabajos y responsabilidades desempeñados por el dueño del currículum? Por favor, incluye detalles sobre las fechas de cada posición y las tareas específicas realizadas en cada una."})
print(response["result"])

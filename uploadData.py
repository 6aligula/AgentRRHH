import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.output_parsers.rail_parser import GuardrailsOutputParser
import PyPDF2


def cargar_documentos(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo {ruta_archivo} no existe.")

    loader = PyMuPDFLoader(ruta_archivo)
    documentos = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=50)
    docs = text_splitter.split_documents(documentos)
    return docs

def crear_vectorstore(docs):
    embed_model = FastEmbedEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embed_model,
        persist_directory="chroma_db_dir",
        collection_name="cv_data"
    )
    return vectorstore

# para openai

def leer_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text += page.extract_text()
                
    except Exception as e:
        print(f"Error al procesar el PDF: {e}")
    
    return text

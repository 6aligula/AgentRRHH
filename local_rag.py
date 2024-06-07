from langchain_community.llms import Ollama

#llm = Ollama(model="llama3")

# response = llm.invoke("Hola, quien eres?")

#print(response)

# load pdf in parts
from langchain_community.document_loaders import PyMuPDFLoader

loader = PyMuPDFLoader("CV_Andres_2024.pdf")
data_pdf = loader.load()
#print(data_pdf[0])

# chunk pdfs 
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=50)
docs = text_splitter.split_documents(data_pdf)
print(f"primera parte:\n {docs[0]} \n")
print("segunnda parte \n")
print(docs[1])
import PyPDF2
import io

def extract_text_from_pdf(pdf_path):
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

# Uso de la función
pdf_path = "src/CV_Andres_2024.pdf"
extracted_text = extract_text_from_pdf(pdf_path)
print(extracted_text)
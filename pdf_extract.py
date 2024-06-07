import openai

openai.api_key = 'api-key'

# Cargar el archivo PDF
file_response = openai.File.create(
    file=open("curriculum_vini_eng_electronic.pdf", "rb"),
    purpose='assistants'
)

file_id = file_response['id']

# Crear un asistente
assistant = openai.Assistant.create(
    name="Assistant",
    instructions="You are a helpful assistant that can read PDFs.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview"
)

# Crear un hilo para interactuar con el asistente
thread = openai.Thread.create()

# Enviar un mensaje al asistente para extraer texto de la primera página del PDF
message = openai.Message.create(
    thread_id=thread['id'],
    role="user",
    content="extract text from page 1",
    file_ids=[file_id]
)

# Ejecutar la solicitud
run = openai.Run.create(
    thread_id=thread['id'],
    assistant_id=assistant['id']
)

# Obtener la respuesta del asistente
while run['status'] != "completed":
    run = openai.Run.retrieve(
        thread_id=thread['id'],
        run_id=run['id']
    )

messages = openai.Message.list(
    thread_id=thread['id']
)

print(messages)

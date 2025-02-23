import streamlit as st
import PyPDF2
import docx
import websocket
import json

def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

def read_docx(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def read_txt(file):
    return file.read().decode("utf-8")

def send_request(task, content, question):
    ws = websocket.WebSocket()
    ws.connect('wss://backend.buildpicoapps.com/ask_ai_streaming_v2')
    ws.send(json.dumps({
        "appId": "mouth-executive",
        "prompt": f"Generate responses based on the document content. Task: {task}, Question: {question}",
        "documentContent": content
    }))
    response = ""
    while True:
        message = ws.recv()
        if not message:
            break
        response += message
    ws.close()
    return response

st.title("Chat Bot App")
st.write("### Ask Me Anything!")

uploaded_file = st.file_uploader("Upload your document", type=["pdf", "docx", "txt"])
task = st.text_input("What do you want me to do today? (e.g., summarize, extract key points, etc.)")
question = st.text_input("Ask a specific question about the document")

if st.button("Let's Do This!"):
    if uploaded_file is None:
        st.warning("Please upload a document.")
    else:
        file_type = uploaded_file.type
        if file_type == "application/pdf":
            content = read_pdf(uploaded_file)
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            content = read_docx(uploaded_file)
        elif file_type == "text/plain":
            content = read_txt(uploaded_file)
        else:
            st.error("Unsupported file type. Please upload a .pdf, .docx, or .txt document.")
            st.stop()

        st.write("### Processing...")
        response = send_request(task, content, question)
        st.write("### Response:")
        st.write(response)

import streamlit as st
import openai
import PyPDF2
import docx
import json

# Function to read PDF
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

# Function to read DOCX
def read_docx(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# Function to read TXT
def read_txt(file):
    return file.read().decode("utf-8")

# Function to process the document with OpenAI
def ask_openai(api_key, task, content, question):
    client = openai.OpenAI(api_key=api_key)  # Use the API key

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI assistant that helps analyze documents."},
            {"role": "user", "content": f"Task: {task}\nQuestion: {question}\nDocument:\n{content}"}
        ]
    )
    
    return response.choices[0].message.content

# Streamlit UI
st.title("Chat Bot App")
st.write("### Ask Me Anything About Your Document!")

# User inputs
api_key = st.text_input("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", type="password")  # Secure API key input
uploaded_file = st.file_uploader("Upload your document", type=["pdf", "docx", "txt"])
task = st.text_input("What do you want me to do? (e.g., summarize, extract key points)")
question = st.text_input("Ask a specific question about the document")

if st.button("Process Document"):
    if not api_key:
        st.error("Please enter your OpenAI API key.")
    elif not uploaded_file:
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
            st.error("Unsupported file type. Please upload a .pdf, .docx, or .txt file.")
            st.stop()

        st.write("### Processing...")
        response = ask_openai(api_key, task, content, question)
        st.write("### Response:")
        st.write(response)

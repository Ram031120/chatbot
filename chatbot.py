import streamlit as st
import openai
import PyPDF2
import docx

# Set OpenAI API key directly
openai.api_key = "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"  # Replace this with your OpenAI API Key

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

# Function to process the document with OpenAI (ChatGPT API)
def ask_chatgpt(content, question):
    # Use the ChatGPT API (gpt-3.5-turbo model)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI assistant that helps analyze documents."},
            {"role": "user", "content": f"Question: {question}\nDocument:\n{content}"}
        ]
    )
    return response['choices'][0]['message']['content']

# Streamlit UI
st.title("Chat Bot App")
st.write("### Ask Me Anything About Your Document!")

# User inputs
uploaded_file = st.file_uploader("Upload your document", type=["pdf", "docx", "txt"])
user_input = st.text_input("Ask a question or describe the task you want done")

if st.button("Process Document"):
    if not uploaded_file:
        st.warning("Please upload a document.")
    elif not user_input:
        st.warning("Please enter a question or task.")
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
        response = ask_chatgpt(content, user_input)
        st.write("### Response:")
        st.write(response)

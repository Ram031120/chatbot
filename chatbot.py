import streamlit as st
import PyPDF2
import docx
import openai

# Function to read PDF files
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

# Function to read DOCX files
def read_docx(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# Function to read TXT files
def read_txt(file):
    return file.read().decode("utf-8")

# Function to send requests to OpenAI API
def send_request(task, content, question):
    openai.api_key = "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"  # Replace with your API key

    prompt = f"""
    Task: {task}
    Question: {question}
    Document Content:
    {content}

    Provide a detailed response based on the given document.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use "gpt-3.5-turbo" if you prefer a cheaper option
        messages=[
            {"role": "system", "content": "You are an AI assistant that helps summarize and analyze documents."},
            {"role": "user", "content": prompt}
        ]
    )

    return response["choices"][0]["message"]["content"]

# Streamlit UI
st.title("Chat Bot App")
st.write("### Ask Me Anything About Your Document!")

# File uploader
uploaded_file = st.file_uploader("Upload your document", type=["pdf", "docx", "txt"])
task = st.text_input("What do you want me to do today? (e.g., summarize, extract key points, etc.)")
question = st.text_input("Ask a specific question about the document")

if st.button("Let's Do This!"):
    if uploaded_file is None:
        st.warning("Please upload a document.")
    else:
        # Determine file type and extract text
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

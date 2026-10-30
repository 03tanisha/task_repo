# first uplaod the pdf -> Extract the text from pdf -> split the text into the chunks 
# create embeddings of the chunks -> store them in chromadb -> retrive the text -> ans the ques using llm in a human like text



import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import tempfile
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()  



# main heading
st.markdown("""
     <h1 style = "
        font-family: 'Arial, sans-serif';
        font-size: 42px;
        font-weight: bold;
        color: #6C63FF;
        text-align: center;
        margin-bottom: 20px;
    "> 
      AI ASSISTANT
    </h1>
    """, unsafe_allow_html = True)


# upload button for uploading the pdf file 
uploaded_file = st.file_uploader(
    "Upload a PDF file",
    type = ["pdf"]
)

if uploaded_file is not None:

    with tempfile.NamedTemporaryFile(
        delete = False, suffix = ".pdf"
    ) as temp_file:
        temp_file.write(uploaded_file.getvalue())
        pdf_path = temp_file.name

    # load the pdf 
    load_pdf = PyPDFLoader(pdf_path)
    doc = load_pdf.load()
    st.success("File uploaded successfully!")

    # text splitting
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200,
        separators = ["\n\n", "\n", ".", " "]
    )

    chunks = text_splitter.split_documents(doc)
    if not chunks:
        st.error("No text found in this PDF.")
        st.stop()

    st.info("Processing PDF and creating embeddings...")

    # create embeddings of the chunks
    embedding = HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
    )

    # storing the embeddigns in chromadb
    chroma_db = Chroma.from_documents(
        documents = chunks,
        embedding = embedding,
        persist_directory = "./chroma_db"
    )

    st.success("PDF is ready! Ask your question below.")

    # retrieval searching
    retriever = chroma_db.as_retriever(
        search_kwargs = {
            "k" : 3
        }
    )

    # query input 
    query = st.text_input("Ask a question:")

    if query:

        # relevant chunks 
        retriever_chunks = retriever.invoke(query)


        context = "\n\n".join(
                chunk.page_content for chunk in retriever_chunks
            )


        prompt = ChatPromptTemplate.from_template("""
                    You are a helpful assistant.
                    Use the provided context to answer the question,if the answer is not found in the context,
                    say "I don't know". 
                    DO NOT make up an answer.

                    Context : {context}
                    Question : {question}
                    """)


        llm = ChatGroq(
            model = "openai/gpt-oss-120b",
            temperature = 0)

        chain = prompt | llm

        response = chain.invoke({
            "context" : context,
            "question" : query
        })

        # st.write("### Answer")
        # st.write(response.content)
        st.markdown("""
            <style>
            .answer-box {
                 background-color: #1E1E2F;
                padding: 20px;
                border-radius: 12px;
                border: 1px solid #444466;
                color: white;
                font-family: Arial, sans-serif;
                font-size: 16px;
                line-height: 1.7;
            }
            </style>
            """, unsafe_allow_html=True)

        st.markdown("### AI Answer")

        st.markdown(
            f'<div class="answer-box">{response.content}</div>',
            unsafe_allow_html=True
        )
                



            




import streamlit as st
import os
from dotenv import load_dotenv 
# from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain_community.document_loaders import WebBaseLoader
from langchain.document_loaders import UnstructuredPDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain.embeddings import SentenceTransformerEmbeddings
import time

## Don't reload the below info everytime streamlit server runs on user interaction

if "vectorstore" not in st.session_state:

    st.session_state.embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    # st.session_state.loader = WebBaseLoader("https://en.wikipedia.org/wiki/Artificial_intelligence")
    st.session_state.loader = UnstructuredPDFLoader(r"data/Corporate Sales deck.pdf", strategy="ocr_only")
    st.session_state.documents = st.session_state.loader.load()

    st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
    st.session_state.docs = st.session_state.text_splitter.split_documents(st.session_state.documents)
    st.session_state.vectorstore = FAISS.from_documents(st.session_state.docs, st.session_state.embeddings)

st.title("SOLOS Chatbot for generic user queries")

input_text = st.text_input("Enter any query you have regarding SOLOS")

llm = ChatOllama(model="gemma2:2b", base_url="http://127.0.0.1:11434", temperature=0, max_tokens=1000)

prompt=ChatPromptTemplate.from_template("Answer the question based on the context below.\n\nContext: {context}\n\nQuestion: {input}\n\nAnswer:")


retriever = st.session_state.vectorstore.as_retriever(search_type="similarity", search_kwargs={"k":3})
chain = create_retrieval_chain(retriever, create_stuff_documents_chain(llm, prompt))

if input_text:
    start=time.time()
    response = chain.invoke({"input": input_text})
    st.write(response['answer'])

    end=time.time()
    st.write(f"Response time: {end-start} seconds")

    #Hopefully runs without error

   









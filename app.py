import os
import streamlit as st
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document
from persona import get_enhanced_system_prompt, COMMON_RESPONSES, PERSONA


# Load environment variables
load_dotenv()


# Get the Google API key
api_key = os.getenv('GOOGLE_API_KEY')

if not api_key:
    print("Google API key not found in .env file.")
    exit(1)


# Streamlit app title
st.title("Chat with Prabhu Nithin Gollapudi")
intro_line = "AI/ML Engineer with 5+ years of IT experience, currently freelancing in Vibe Coding AI/ML Services. Specializing in AI agents, LLMs, medical robotics research, and full-stack development. Master's in AI at FAU (expected March 2026)."
st.markdown(f"#### {intro_line}")
st.write(COMMON_RESPONSES["contact"])

# Add a profile image if available
try:
    from PIL import Image
    import base64
    from pathlib import Path
    
    # Check if a profile image exists
    image_path = Path("profile_image.png")
    if image_path.exists():
        image = Image.open(image_path)
        st.image(image, width=150)
except ImportError:
    pass

st.markdown("---")


# Cache the vectorstore for efficiency (loads once)
@st.cache_resource
def load_vectorstore():
    # Check for both markdown
    markdown_path = "resume.md"
    
    if os.path.exists(markdown_path):
        return load_from_markdown(markdown_path)
    else:
        st.error("No resume file found! Add 'resume.md' to the project directory.")
        return None

def load_from_markdown(file_path):
    """Load and process markdown resume file."""
    with st.spinner("Loading resume from markdown..."):
        try:
            # Use MarkdownHeaderTextSplitter for better structure awareness
            headers_to_split_on = [
                ("#", "Header 1"),
                ("##", "Header 2"),
                ("###", "Header 3"),
                ("####", "Header 4"),
            ]
            
            markdown_splitter = MarkdownHeaderTextSplitter(
                headers_to_split_on=headers_to_split_on,
                strip_headers=False
            )
            
            # Read the markdown file
            with open(file_path, 'r', encoding='utf-8') as file:
                markdown_content = file.read()
            
            # Split by headers first
            md_header_splits = markdown_splitter.split_text(markdown_content)
            
            # Further split if chunks are too large
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, 
                chunk_overlap=200,
                separators=["\n\n", "\n", " ", ""]
            )
            
            # Process the documents
            all_splits = []
            for doc in md_header_splits:
                if len(doc.page_content) > 1000:
                    # Split large sections further
                    sub_splits = text_splitter.split_documents([doc])
                    all_splits.extend(sub_splits)
                else:
                    all_splits.append(doc)
            
            # Create embeddings and vectorstore
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            vectorstore = FAISS.from_documents(all_splits, embeddings)
            
            return vectorstore
            
        except Exception as e:
            st.error(f"Error loading markdown file: {str(e)}")
            return None

# Load vectorstore
vectorstore = load_vectorstore()

# Session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Set up RAG chain if vectorstore loaded
if vectorstore:
    # Free HF LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",  # Trying gemini-2.0-flash-exp
        temperature=0.1,
        max_output_tokens=512,
        google_api_key=api_key
    )
    
    # Use the enhanced system prompt from persona module
    system_prompt = get_enhanced_system_prompt()
    prompt = ChatPromptTemplate.from_template(system_prompt)
    
    # Create chains
    question_answering_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(vectorstore.as_retriever(), question_answering_chain)

    # Display welcome message if chat history is empty
    if not st.session_state.chat_history:
        welcome_message = COMMON_RESPONSES["greeting"]
        research_intro = f"\n\nI'm actively job hunting for full-time opportunities in 2026! Currently, I'm freelancing in Vibe Coding AI/ML Services, building AI agents and LLM applications. This chatbot is a hobby project I built to showcase my AI skills. What would you like to know about my journey, technical projects, research experience, or career goals?"
        st.session_state.chat_history.append({"role": "assistant", "content": welcome_message + research_intro})
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("Ask me about my AI/ML experience, projects, freelance work, research, or career goals..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = rag_chain.invoke({"input": prompt})
                answer = response["answer"] if "answer" in response else COMMON_RESPONSES["not_in_resume"]
                st.markdown(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

else:
    st.info("Resume not loaded. Check the project setup.")
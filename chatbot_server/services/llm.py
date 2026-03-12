import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from services.key_manager import key_manager

load_dotenv()

# def get_llm():
#     # low-level endpoint (provider connection)
#     endpoint = HuggingFaceEndpoint(
#         repo_id="meta-llama/Llama-3.2-3B-Instruct",
#         task="text-generation",          # IMPORTANT
#         huggingfacehub_api_token=os.getenv("HF_TOKEN"),
#         temperature=0.2,
#         max_new_tokens=400,
#     )

#     # chat wrapper (what LangChain expects)
#     chat_model = ChatHuggingFace(llm=endpoint)

#     return chat_model

def get_llm_summary():
    # low-level endpoint (provider connection)
    endpoint = HuggingFaceEndpoint(
        repo_id="meta-llama/Llama-3.1-8B-Instruct",
        task="text-generation",          # IMPORTANT
        huggingfacehub_api_token=os.getenv("HF_TOKEN"),
        temperature=0,
        max_new_tokens=500
    )

    # chat wrapper (what LangChain expects)
    chat_model = ChatHuggingFace(llm=endpoint)

    return chat_model
    

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0,
        max_output_tokens=512,  
        google_api_key=key_manager.get_key()
    )
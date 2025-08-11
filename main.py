import streamlit as st
from faq import ingest_faq_data, faq_chain
from sql import sql_chain
from smalltalk import talk
import chromadb
from dotenv import load_dotenv
import os

load_dotenv()  # This reads your .env file and loads env variables into os.environ
groq_model = os.getenv('GROQ_MODEL')
groq_api_key = os.getenv('GROQ_API_KEY')

if not groq_model or not groq_api_key:
    st.error("Environment variables GROQ_MODEL or GROQ_API_KEY are missing.")


from pathlib import Path
from router import router
client = chromadb.Client()

faqs_path = Path(__file__).parent /"resources"/"FAQs.csv"
try:
    ingest_faq_data(faqs_path)
except FileNotFoundError:
    print(f"FAQ data file not found at {faqs_path}. Please check the path.")



# List all collection names
existing_collections = [c.name for c in client.list_collections()]

if "faqs" not in existing_collections:
    client.create_collection("faqs")
else:
    client.get_collection("faqs")



    


def ask(query):
    route_obj = router(query)
    if route_obj is None:
        return "Sorry, I couldn't understand your query."
    
    route_name = route_obj.name
    
    if route_name == 'faq':
        return faq_chain(query)
    elif route_name == 'sql':
        return sql_chain(query)
    elif route_name == 'smalltalk':
        return talk(query)
    else:
        return f"Route '{route_name}' not implemented yet"


st.title("E-commerce Bot")

query = st.chat_input("Write your query")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if query:
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.messages.append({"role":"user", "content":query})

    response = ask(query)
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
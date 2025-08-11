import os

import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
import pandas
from dotenv import load_dotenv

load_dotenv()


ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name='sentence-transformers/all-MiniLM-L6-v2'
        )

chroma_client = chromadb.Client()
groq_client = Groq()
collection_name_faq = 'faqs'


def ingest_faq_data(path):
    try:
        if collection_name_faq not in [c.name for c in chroma_client.list_collections()]:
            print("Ingesting FAQ data into Chromadb...")
            collection = chroma_client.create_collection(
                name=collection_name_faq,
                embedding_function=ef
            )
            df = pandas.read_csv(path)
            # Try to find the question and answer columns, case-insensitive
            question_col = None
            answer_col = None
            for col in df.columns:
                if col.strip().lower() in ["question", "q"]:
                    question_col = col
                if col.strip().lower() in ["answer", "a"]:
                    answer_col = col
            # Fallback: handle single column with both values (e.g., 'Question,Answer')
            if question_col is None or answer_col is None:
                if len(df.columns) == 1 and ',' in df.columns[0]:
                    # Split the single column into two
                    new_cols = [c.strip() for c in df.columns[0].split(',')]
                    df = df[df.columns[0]].str.split(',', n=1, expand=True)
                    df.columns = new_cols
                    question_col = new_cols[0]
                    answer_col = new_cols[1]
                else:
                    raise ValueError(f"Could not find 'Question' and 'Answer' columns in the CSV. Found columns: {list(df.columns)}")
            docs = df[question_col].astype(str).to_list()
            metadata = [{"answer": ans} for ans in df[answer_col].astype(str).to_list()]
            ids = [f"id_{i}" for i in range(len(docs))]
            collection.add(
                documents=docs,
                metadatas=metadata,
                ids=ids
            )
            print(f"FAQ Data successfully ingested into Chroma collection: {collection_name_faq}")
        else:
            print(f"Collection: {collection_name_faq} already exist")
    except chromadb.errors.InternalError as e:
        if "already exists" in str(e):
            print(f"Collection: {collection_name_faq} already exist (handled)")
        else:
            raise
    # (No code here; removed duplicate and mis-indented block)
    else:
        print(f"Collection: {collection_name_faq} already exist")


def get_relevant_qa(query):
    collection = chroma_client.get_collection(
        name=collection_name_faq,
        embedding_function=ef
    )
    result = collection.query(
        query_texts=[query],
        n_results=2
    )
    return result


def generate_answer(query, context):
    prompt = f'''Given the following context and question, generate answer based on this context only.
    If the answer is not found in the context, kindly state "I don't know". Don't try to make up an answer.
    
    CONTEXT: {context}
    
    QUESTION: {query}
    '''
    # Use GROQ_MODEL from environment, or try a list of fallback models
    # Use GROQ_MODEL from environment, or default to 'llama-3.3-70b-versatile'
    model_name = os.environ.get('GROQ_MODEL', 'llama-3.3-70b-versatile')
    completion = groq_client.chat.completions.create(
        model=model_name,
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )
    return completion.choices[0].message.content


def faq_chain(query):
    result = get_relevant_qa(query)
    # Use the correct metadata key ('answer'), and skip None values
    context = "".join([r.get('answer') for r in result['metadatas'][0] if r.get('answer') is not None])
    print("Context:", context)
    answer = generate_answer(query, context)
    return answer


if __name__ == '__main__':
    ingest_faq_data(r"C:\Users\prasa\OneDrive\Documents\FAQs.csv")
    query = "what's your policy on defective products?"
   
    # result = get_relevant_qa(query)
    answer = faq_chain(query)
    print("Answer:",answer)
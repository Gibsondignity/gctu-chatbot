from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import requests
import os

# === Embedding Model ===
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# === ChromaDB Setup ===
client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chroma"))
collection = client.get_or_create_collection(name="gctu")

# === Groq API Setup ===
GROQ_API_KEY = "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" 



def call_groq_llm(prompt):
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        json={
            "model": "llama3-70b-8192", 
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    # print("Groq API response:", response.status_code, response.text)
    try:
        data = response.json()
    except ValueError:
        raise Exception(f"Failed to parse JSON response: {response.text}")

    if "choices" not in data:
        raise Exception(f"Unexpected response from Groq API: {data}")

    return data["choices"][0]["message"]["content"]




def ask_bot(question):
    embedding = embedding_model.encode(question).tolist()
    results = collection.query(query_embeddings=[embedding], n_results=3)

    context = "\n".join(results["documents"][0])

    prompt = f"""You are a helpful assistant for students at GCTU. Answer the question using the context below.

Context:
{context}

Question: {question}
Answer:"""

    return call_groq_llm(prompt)

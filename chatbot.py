from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import os
from groq import Groq
from serpapi import GoogleSearch
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# === Embedding Model ===
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# === ChromaDB Setup ===
client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chroma"))
collection = client.get_or_create_collection(name="gctu")

# === Groq API Setup ===
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))




def call_groq_llm(prompt):
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error calling Groq API: {str(e)}")


def search_web(query):
    """Search the web using SerpAPI for additional information"""
    try:
        search = GoogleSearch({
            "q": query + " GCTU Ghana Communication Technology University",
            "api_key": os.environ.get("SERPAPI_API_KEY", ""),
            "num": 3  # Get top 3 results
        })
        results = search.get_dict()

        if "organic_results" in results:
            search_context = ""
            for result in results["organic_results"][:3]:
                title = result.get("title", "")
                snippet = result.get("snippet", "")
                link = result.get("link", "")
                search_context += f"Title: {title}\nSnippet: {snippet}\nSource: {link}\n\n"
            return search_context
        return ""
    except Exception as e:
        print(f"Web search failed: {e}")
        return ""



def ask_bot(question):
    embedding = embedding_model.encode(question).tolist()
    results = collection.query(query_embeddings=[embedding], n_results=5)

    context = "\n".join(results["documents"][0])

    # Always search web for additional current information
    web_results = search_web(question)
    if web_results:
        context += "\n\nAdditional current information from web search:\n" + web_results

    prompt = f"""You are a helpful assistant for students at GCTU, specifically focused on the IT department. Answer the question using the context below, prioritizing the most current and relevant information.

Format your response using Markdown:
- Use **bold** for emphasis
- Use *italics* for subtle emphasis
- Use paragraphs for long explanations (separate with blank lines)
- Use bullet points (- item) or numbered lists (1. item) for lists
- Use headings if needed (# Heading)
- Keep responses concise but informative
- Structure answers like ChatGPT: natural, well-organized, and easy to read

Context:
{context}

Question: {question}
Answer:"""

    return call_groq_llm(prompt)

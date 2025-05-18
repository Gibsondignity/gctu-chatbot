import os
import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import uuid 

# === PDF Extraction ===
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    return " ".join(page.get_text() for page in doc)

# === URL Extraction ===
def extract_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        # Remove scripts/styles
        for tag in soup(["script", "style"]): tag.decompose()
        return soup.get_text(separator=" ", strip=True)
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return ""

# === Preprocess and Chunk ===
def preprocess_text(text, chunk_size=500):
    cleaned = ' '.join(text.split())
    return [cleaned[i:i+chunk_size] for i in range(0, len(cleaned), chunk_size)]

# === Embed and Store ===
def embed_and_store(chunks, collection):
    for chunk in chunks:
        unique_id = f"doc_{uuid.uuid4()}"
        collection.add(documents=[chunk], ids=[unique_id])

# === Main Entry Point ===
def main():
    client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chroma"))
    collection = client.get_or_create_collection(name="gctu")


    # === Load PDFs ===
    # pdfs = [
    #     "gctu_docs/GCTU-Basic-Laws.pdf",
    #     "gctu_docs/2022-2030-STRATEGIC-PLAN.pdf",
    #     "gctu_docs/Undergraduate-Students-Handbook-Final-Accepted.pdf",
    #     "gctu_docs/ICDE-ACADEMIC-CALENDAR-2025.pdf",
    #     # Add other PDF paths here
    # ]
    
    folder = "gctu_docs"  
    for filename in os.listdir(folder):
        if filename.endswith(".pdf"):
            print(f"Processing PDF: {filename}")
            text = extract_text_from_pdf(os.path.join(folder, filename))
            chunks = preprocess_text(text)
            embed_and_store(chunks, collection)


    # === Load URLs ===
    urls = [
        "https://site.gctu.edu.gh/undergraduate-programmes/",
        "https://site.gctu.edu.gh/undergraduate-programmes"
        "https://site.gctu.edu.gh/academic-calendar/",
        "https://site.gctu.edu.gh/",
        "https://site.gctu.edu.gh/undergraduate-admission-requirement",
        "https://site.gctu.edu.gh/",
        "https://site.gctu.edu.gh/admissions-office",
        "https://site.gctu.edu.gh/how-to-apply",
        "https://site.gctu.edu.gh/admission-policy",
        "https://site.gctu.edu.gh/undergraduate-programmes",
        "https://gs.gctu.edu.gh/academics/masters-programmes/",
        "https://site.gctu.edu.gh/gtuc/administration/about-gtuc/",
        "https://site.gctu.edu.gh/gtuc/administration/organogram/",
        "https://site.gctu.edu.gh/gtuc/administration/gtuc-history/",
        "https://site.gctu.edu.gh/gtuc/administration/our-mission/",
        "https://site.gctu.edu.gh/gtuc/administration/gtuc-anthem/",
        "https://site.gctu.edu.gh/partners-and-affiliates",
        "https://site.gctu.edu.gh/category/staff/council-members",
        "https://gs.gctu.edu.gh/",
        "https://gs.gctu.edu.gh/academics/phd-programmes/",
    ]
    for url in urls:
        print(f"Processing URL: {url}")
        text = extract_text_from_url(url)
        chunks = preprocess_text(text)
        embed_and_store(chunks, collection)

    client.persist()
    print("✅ All documents and URLs embedded and stored.")

if __name__ == "__main__":
    main()

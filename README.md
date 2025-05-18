📚 GCTU Smart Student Chatbot – AI-Powered Assistant
This is an AI-powered chatbot designed to assist students of Ghana Communication Technology University (GCTU) by answering questions based on official university documents like the academic calendar, undergraduate handbook, and relevant website pages.



✅ Features
💬 Ask GCTU-specific questions (e.g., "When does the semester start?")
🧠 Context-aware answers using embedded university documents
📄 Load and parse PDFs (e.g., handbook, calendar)
🌐 Read content from GCTU website pages
🔍 Semantic search using ChromaDB
⚡ Uses free, fast LLM via Groq API (Mixtral, LLaMA3)
🧠 Embedding model: sentence-transformers/all-MiniLM-L6-v2



📦 Tech Stack
Python 3.10+
Django
ChromaDB
Sentence Transformers
Groq API
BeautifulSoup (for HTML parsing)
PyMuPDF (for PDF extraction)




🚀 Getting Started
1. Clone the Project
git clone https://github.com/gibsondignity/gctu-chatbot.git
cd gctu-chatbot


2. Set Up Python Environment
Install pyenv if needed, then:
pyenv install 3.10.13
pyenv local 3.10.13
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


3. Set Up Environment Variables
Create a .env file and add your Groq API key:
Visit: https://console.groq.com/home
GROQ_API_KEY=your-groq-api-key-here


4. Add Your GCTU PDFs
Create a folder called gctu_docs in the project root and place your PDFs inside (e.g., Academic Calendar, Handbook).

5. Load Data into ChromaDB
Run the ingestion script:
python load_gctu_docs.py
This will embed both PDF and online content into your local vector store.


6. Run the Django Server
python manage.py runserver
Open http://localhost:8000 and chat with your GCTU bot.




🧠 How It Works
Text Extraction
Extracts content from PDFs and GCTU URLs
Splits them into text chunks for semantic similarity
Embedding & Storage
Uses sentence-transformers to embed chunks
Stores them in ChromaDB locally
Question Answering
When a question is asked, the bot:
Embeds the question
Retrieves top relevant chunks from ChromaDB
Sends the prompt and context to Groq API (Mixtral or LLaMA 3)
Returns a natural-language answer



🛠️ Example URLs Supported
https://site.gctu.edu.gh/academic-calendar/
https://site.gctu.edu.gh/undergraduate-programmes/

Add more in load_gctu_docs.py.
🧪 Example Questions to Try
"When does the second semester start?"
"What are the undergraduate programmes?"
"How do I defer my course at GCTU?"
"What is the grading system?"


📂 Project Structure
.
├── chatbot.py              # Core logic for question answering
├── chat/                   # Django app
│   ├── views.py            # Handles user requests
├── load_gctu_docs.py       # Extract and store PDF/URL data
├── gctu_docs/              # Place your PDFs here
├── .env                    # Add your GROQ_API_KEY here
├── requirements.txt
└── README.md



🙌 Contributions
Contributions are welcome — feel free to open issues or submit pull requests!


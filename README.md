# 🏎️ Local F1 RAG (Retrieval-Augmented Generation) System

A fully local, modular command-line application built on a Retrieval-Augmented Generation (RAG) architecture. The primary goal of this system is to accurately answer questions regarding the history and achievements of 10 legendary Formula 1 drivers based on external documents, completely eliminating hallucinations.

The application relies exclusively on open-source models and runs 100% locally on the user's machine—requiring no connection to external, paid APIs.

### 👥 Supported Drivers (Knowledge Base [10]):
1. Alain Prost
2. Ayrton Senna
3. Fernando Alonso
4. Jackie Stewart
5. Juan Manuel Fangio
6. Lewis Hamilton
7. Max Verstappen
8. Michael Schumacher
9. Niki Lauda
10. Sebastian Vettel

---

## 🛠️ Tech Stack & Architecture

* **LLM (Model AI):** `TinyLlama-1.1B-Chat-v1.0` (HuggingFace Transformers).
* **Vector Database:** `Qdrant` (Dockerized).
* **Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2`.
* **Data Chunking & ETL:** `LangChain` (`RecursiveCharacterTextSplitter`) & `PyMuPDF`.
* **User Interface:** `Rich`.

### 🔓 Why an Open-Source LLM? (The Local Advantage)
Unlike many wrapper applications that rely on paid cloud APIs (e.g., OpenAI, Anthropic), this project was intentionally built using a local open-source model (`TinyLlama`). This architectural choice guarantees:
* **100% Data Privacy:** Your F1 queries and retrieved documents never leave your machine.
* **Zero Cost Architecture:** No API keys, no hidden token fees, and no rate limits.
* **Offline Inference:** Once the model weights are downloaded, the entire RAG pipeline runs locally on your hardware.

---

## 🚀 Setup & Installation (WSL / Linux)

Follow these steps to recreate the project locally on your machine.

### Step 1: Project Setup & Virtual Environment (`.venv`)
First, open your WSL terminal, create a new directory for the project, and navigate into it.

```bash
# Create the main folder and navigate into it
mkdir f1-rag-project
cd f1-rag-project
```

Next, we must create a **Python Virtual Environment**. In the Python ecosystem, installing dependencies globally is considered a bad practice, as it leads to version conflicts between different projects. We isolate our project's libraries using `.venv`.

```bash
# Create a virtual environment named '.venv'
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate
```
*(You should now see `(.venv)` at the beginning of your terminal prompt, indicating that isolation is active).*

### Step 2: Populate the Data Directory (PDFs)
Create the data folder and move your downloaded Wikipedia PDF articles into it.

```bash
# Create the data directory
mkdir -p data/pdfs

# Copy your downloaded PDFs into the project directory
# (Replace '/path/' with the actual path to your PDF files)
cp /path/*.pdf data/pdfs/
```

### Step 3: Create Project Files
You can create the necessary files using your preferred code editor, or directly in the terminal using the `cat` command. 

Here is a universal example of how to create a file and paste its content via terminal:
```bash
cat > filename.ext << 'EOF'
# [PASTE THE CORRESPONDING CODE FROM THIS REPOSITORY HERE]
EOF
```

Use this method (or your editor) to create the following files and populate them with the code provided in this repository:

**Root Directory Files:**
* `docker-compose.yml` - *Vector database configuration*
* `requirements.txt` - *Python dependencies*

**Source Code Files (`src/`):**
First, create the source directory: `mkdir -p src`
* `src/ingest.py` - *ETL pipeline script*
* `src/llm.py` - *Local LLM configuration*
* `src/retriever.py` - *Qdrant database connection*
* `src/cli.py` - *Terminal interface logic*

### Step 4: Install Dependencies & Run Database
Make sure your virtual environment is active, then install the required libraries and start the database:
```bash
# Activate the virtual environment (if you closed the terminal)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start Qdrant in the background
docker-compose up -d
```

### Step 5: Run the Ingestion Pipeline & CLI
With the database running and the `.venv` active, process the documents and start the conversational agent:
```bash
# Ensure .venv is active
source .venv/bin/activate

# Upload documents and generate embeddings in Qdrant
python src/ingest.py

# Launch the Agent!
python src/cli.py
```

---

## ⚖️ Data Source & Licensing
* **Data Copyright:** The PDF documents in the `data/` directory were generated from **Wikipedia**.
* **Data License:** Distributed under the **Creative Commons Attribution-ShareAlike License (CC BY-SA 3.0)**.

# 🏎️ Local F1 RAG (Retrieval-Augmented Generation) System

A fully local, modular command-line application built on a Retrieval-Augmented Generation (RAG) architecture. The primary goal of this system is to accurately answer questions regarding the history and achievements of 10 legendary Formula 1 drivers based on external documents, completely eliminating hallucinations.

The application relies exclusively on open-source models and runs 100% locally on the user's machine—requiring no connection to external, paid APIs.

### 👥 Supported Drivers (Knowledge Base):
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

---

## 🚀 Setup & Installation (WSL / Linux)

Follow these steps to recreate the project locally on your machine.

### Step 1: Project Setup & Virtual Environment (`.venv`)
```bash
# Create the main folder and navigate into it
mkdir f1-rag-project
cd f1-rag-project

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate
```

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
Create the following files in your project directory and paste the corresponding code from this repository.

**1. `docker-compose.yml`** (Root directory)
```yaml
# Paste the contents of docker-compose.yml here
```

**2. `requirements.txt`** (Root directory)
```text
# Paste the contents of requirements.txt here
```

**3. Source Code** (Inside the `src/` directory)
```bash
mkdir -p src
```
Create the following Python scripts inside the `src/` folder:
* `src/ingest.py` - *ETL pipeline script*
* `src/llm.py` - *Local LLM configuration*
* `src/retriever.py` - *Qdrant database connection*
* `src/cli.py` - *Terminal interface logic*

### Step 4: Install Dependencies & Run Database
Once your files are in place, install the required libraries and start the vector database:
```bash
pip install -r requirements.txt
docker-compose up -d
```

### Step 5: Run the Ingestion Pipeline & CLI
Process the documents and start the conversational agent:
```bash
# Upload documents and generate embeddings in Qdrant
python src/ingest.py

# Launch the Agent!
python src/cli.py
```

---

## ⚖️ Data Source & Licensing
* **Data Copyright:** The PDF documents in the `data/` directory were generated from **Wikipedia**.
* **Data License:** Distributed under the **Creative Commons Attribution-ShareAlike License (CC BY-SA 3.0)**.

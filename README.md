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

### Step 3: Create Project Files via Terminal (`cat`)
You can generate all necessary configuration and source files directly from the command line using the `cat << 'EOF'` syntax. Paste these blocks sequentially into your terminal.

**1. Root Configuration Files**
```bash
# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: "3.8"
services:
  qdrant:
    image: qdrant/qdrant:latest
    container_name: qdrant
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage
    restart: unless-stopped
volumes:
  qdrant_data:
EOF

# Create requirements.txt
cat > requirements.txt << 'EOF'
qdrant-client>=1.9.0
sentence-transformers>=3.0.0
transformers>=4.40.0
torch>=2.2.0
accelerate>=0.29.0
pymupdf>=1.24.0
langchain-text-splitters>=0.2.0
rich>=13.7.0
typer>=0.12.0
EOF
```

**2. Source Code Layer (`src/` directory)**
First, create the source directory:
```bash
mkdir -p src
```

*Note: For the Python scripts below, you can copy the full code blocks from this repository's `src/` folder and paste them into your terminal using the same `cat > filename.py << 'EOF'` method, or simply download the repository directly using `git clone`.*

To manually generate the main application logic via terminal, run the following commands and paste the respective script contents from the repository before typing `EOF`:

```bash
# 1. Create the Database Retriever module
cat > src/retriever.py << 'EOF'
# [PASTE FULL CONTENT OF src/retriever.py HERE]
EOF

# 2. Create the LLM configuration module
cat > src/llm.py << 'EOF'
# [PASTE FULL CONTENT OF src/llm.py HERE]
EOF

# 3. Create the Data Ingestion pipeline
cat > src/ingest.py << 'EOF'
# [PASTE FULL CONTENT OF src/ingest.py HERE]
EOF

# 4. Create the Command Line Interface
cat > src/cli.py << 'EOF'
# [PASTE FULL CONTENT OF src/cli.py HERE]
EOF
```

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

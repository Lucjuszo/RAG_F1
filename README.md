# 🏎️ Local F1 RAG (Retrieval-Augmented Generation) System

A fully local, modular command-line application built on a Retrieval-Augmented Generation (RAG) architecture. The primary goal of this system is to accurately answer questions regarding the history and achievements of 10 legendary Formula 1 drivers based on external documents, completely eliminating hallucinations.

The application relies exclusively on open-source models and runs 100% locally on the user's machine—requiring no connection to external, paid APIs (such as OpenAI or Anthropic).

### 👥 Supported Drivers (Knowledge Base [10]):
The system is populated with comprehensive biographical and statistical data for the following drivers:
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

This project demonstrates a complete data engineering pipeline (ETL) and the deployment of a local large language model:

* **LLM (Model AI):** `TinyLlama-1.1B-Chat-v1.0` – A lightweight, compact model optimized for local inference using HuggingFace Transformers.
* **Vector Database:** `Qdrant` – Running inside a Docker container, responsible for storing vector embeddings and performing fast cosine similarity searches.
* **Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2` – Maps text segments into 384-dimensional vectors representing their semantic meaning.
* **Data Chunking & ETL:** `LangChain` (`RecursiveCharacterTextSplitter`) for intelligently splitting documents into overlapping chunks, and `PyMuPDF` (`fitz`) for extracting text from PDF files.
* **User Interface:** `Rich` – A powerful library for rich text formatting in the terminal, providing clean tables, panels, and progress bars.

### Project Structure (Separation of Concerns)
The system logic is divided into independent, decoupled modules:
* `src/ingest.py` – The ETL script: loads PDFs, processes text, generates embeddings, and populates the Qdrant database.
* `src/retriever.py` – Data access layer: handles querying Qdrant and filtering results.
* `src/llm.py` – Generative layer: configures the HuggingFace pipeline, constructs prompts, and generates answers.
* `src/cli.py` – Main system orchestrator managing user interactions within the terminal interface.

---

## 🚀 Installation & Setup (Step-by-Step for WSL / Linux)

Follow these steps to recreate and run the entire environment on your local machine.

### Step 1: Clone and Prepare the Project Directory
Open your WSL terminal, create a working directory, and navigate into it:
```bash
mkdir f1-rag-project
cd f1-rag-project
```

### Step 2: Configure a Virtual Environment (`.venv`)
In the Python ecosystem, installing packages globally is a bad practice that leads to version conflicts between projects. We isolate our project's libraries using a virtual environment:
```bash
# Create a virtual environment named .venv
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate
```
*(Once activated, a `(.venv)` indicator will appear at the beginning of your terminal prompt).*

### Step 3: Install Required Dependencies
With the `.venv` layer active, install all the necessary data engineering and AI libraries:
```bash
pip install -r requirements.txt
```

### Step 4: Start the Qdrant Vector Database
Ensure that Docker Desktop (or Docker within WSL) is running. We will use the configuration file to spin up the database in the background:
```bash
# Start the Qdrant container in detached mode (background)
docker-compose up -d
```

### Step 5: Prepare the Document Base
The source PDF files for the 10 drivers should be placed in the following directory structure: `data/pdfs/`. If you are setting up the project on a clean system, ensure these folders exist and contain the respective `.pdf` files.

### Step 6: Run the Data Processing Pipeline (ETL Ingestion)
Process the PDF files, generate vector embeddings, and upload them to the database:
```bash
python src/ingest.py
```
*(The screen will display loading logs and progress bars tracking the batch data ingestion into Qdrant).*

### Step 7: Launch the Assistant CLI
Once the data is securely indexed, you can launch the conversational interface:
```bash
python src/cli.py
```
> **Important:** On the very first run, the system will automatically download the local `TinyLlama` model (approx. 2.2 GB) from the HuggingFace repository. This process is skipped on subsequent launches, and the application will start instantly.

---

## ⚖️ Data Source & Licensing

* **Data Copyright:** The text files and PDF documents located in the `data/` directory were generated based on public articles from **Wikipedia**.
* **Data License:** This content is shared and distributed under the terms of the **Creative Commons Attribution-ShareAlike License (CC BY-SA 3.0)**.

# 🏎️ F1 RAG (Retrieval-Augmented Generation) System

A fully local, modular Retrieval-Augmented Generation (RAG) command-line application built to answer complex questions about Formula 1 drivers. The system relies entirely on open-source models and runs locally without the need for external API calls.

## 🛠️ Tech Stack & Architecture
This project demonstrates a complete data engineering and AI pipeline:
* **LLM:** `TinyLlama-1.1B-Chat-v1.0` (HuggingFace, Local Inference)
* **Vector Database:** Qdrant (Dockerized)
* **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`
* **Data Processing Pipeline (ETL):** LangChain (`RecursiveCharacterTextSplitter`), PyMuPDF
* **CLI Interface:** Rich

### Project Structure (Separation of Concerns)
The logic is divided into modular, highly decoupled components:
* `src/ingest.py` - ETL pipeline: loads PDFs, chunks text, generates embeddings, and populates the Qdrant database.
* `src/retriever.py` - Handles vector similarity search and database connections.
* `src/llm.py` - Manages local model initialization, tokenization, and prompt engineering.
* `src/cli.py` - The main orchestrator connecting the retriever and LLM within a rich terminal interface.

---

## 🚀 How to Run the F1 RAG Project from Scratch (WSL / Linux)

Follow these steps to recreate and run the project locally on your machine.

### Step 1: Project Setup & Virtual Environment (`.venv`)
First, open your WSL terminal, create a new directory for the project, and navigate into it.

```bash
# Create the main folder and navigate into it
mkdir f1-rag-project
cd f1-rag-project

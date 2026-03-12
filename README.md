# RAG Demo Project

This project is a demo of a simple Retrieval-Augmented Generation (RAG) system, featuring a FastAPI backend with document ingestion and querying, and a React + Vite frontend for user interaction.

## Features

- **Backend (FastAPI, ChromaDB, Transformers):**
  - Ingest plain text documents into a vector database (ChromaDB)
  - Query the database for relevant documents using semantic search
  - Generate answers to user questions using a GPT-2 model, augmented with retrieved context

- **Frontend (React, Vite):**
  - Upload and ingest text files
  - Ask questions and receive answers with supporting context
  - Simple, modern UI for demo purposes

---

## Project Structure

```
backend/
  main.py              # FastAPI app, ChromaDB, GPT-2 integration
  send_txt_to_api.py   # CLI utility to ingest .txt files via API
  requirements.txt     # Python dependencies

frontend/
  src/App.tsx          # Main React app (UI for ingest/query)
  index.html           # HTML entry point
  package.json         # Frontend dependencies
  vite.config.mts      # Vite config
```

---

## Getting Started

### Backend Setup

1. **Install Python dependencies:**
	```bash
	cd backend
	pip install -r requirements.txt
	```

2. **Run the FastAPI server:**
	```bash
	uvicorn main:app --reload
	```
	The API will be available at `http://localhost:8000`.

3. *(Optional)* **Ingest .txt files via CLI:**
	```bash
	python send_txt_to_api.py <directory_with_txt_files>
	# Or specify a custom API URL:
	python send_txt_to_api.py <dir> --api-url http://localhost:8000/ingest
	```

### Frontend Setup

1. **Install Node dependencies:**
	```bash
	cd frontend
	npm install
	```

2. **Start the development server:**
	```bash
	npm run dev
	```
	The app will be available at `http://localhost:3000`.

---

## Usage

1. **Ingest Documents:**
	- Use the web UI to upload `.txt` files, then click "Ingest".
	- Or use the CLI utility to batch-ingest files.

2. **Ask Questions:**
	- Enter a question in the web UI and click "Query".
	- The backend retrieves relevant documents and generates an answer using GPT-2.

---

## Tech Stack

- **Backend:** FastAPI, ChromaDB, Transformers (GPT-2), Torch
- **Frontend:** React, Vite, TypeScript

---

## Notes

- This demo uses GPT-2 for simplicity; for production, use a more capable model.
- ChromaDB is used for vector search; you can swap for other vector DBs as needed.

---

## License

MIT License. See LICENSE file if present.

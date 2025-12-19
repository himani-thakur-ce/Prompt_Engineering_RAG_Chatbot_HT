# PROMPT ENGINEERING RAG ASSISTANT

This project is a **Retrieval-Augmented Generation (RAG)** chatbot designed to assist with Prompt Engineering concepts. It uses **Google Gemini** for both embeddings and content generation, wrapped in a **Streamlit** interface.

The assistant acts as a university-level tutor, helping students prepare for exams on prompt engineering by answering questions based on a provided knowledge base (`pe_notes.txt`).

## Features
- **RAG Architecture**: Retrieves relevant context from a local knowledge base before answering.
- **Google Gemini Integration**:
    - **Embeddings**: Uses `models/text-embedding-004` to vectorise the knowledge base.
    - **Generation**: Uses `models/gemini-2.0-flash` for high-quality, fast responses.
- **Custom Knowledge Base**: Easily update the `pe_notes.txt` file with your own notes.
- **Streamlit UI**: Simple and interactive chat interface.

## Prerequisites
- Python 3.8+
- A Google Cloud API Key with access to Gemini models.

## Installation

1.  **Clone the repository** (or download the files).
2.  **Install dependencies**:
    ```bash
    pip install streamlit google-generativeai
    ```
3.  **Set up API Key**:
    - Create a file named `gemini_api.txt` in the root directory.
    - Paste your Google Gemini API key into this file (ensure there are no extra spaces or newlines).

## Usage

### 1. Prepare the Knowledge Base
Edit `pe_notes.txt` and add the content you want the chatbot to know. Separate distinct sections or topics with double newlines (`\n\n`) for better chunking.

### 2. Build the Index
Run the indexing script to generate embeddings for your knowledge base. This must be done whenever `pe_notes.txt` is updated.

```bash
python build_index.py
```
This will create (or overwrite) `pe_index.json`.

### 3. Run the Application
Start the Streamlit app:

```bash
streamlit run app.py
```
The application will open in your default web browser. You can now ask questions about the content in your notes!

## File Structure

- **`app.py`**: The main Streamlit application. Handles the UI, retrieval logic, and generation.
- **`build_index.py`**: Script to process `pe_notes.txt`, generate embeddings, and save them to `pe_index.json`.
- **`check_models.py`**: Utility script to list available Gemini models that support content generation.
- **`pe_notes.txt`**: The source text file containing the knowledge base.
- **`gemini_api.txt`**: File storing the API key (should not be committed to version control).
- **`pe_index.json`**: The generated vector index containing text chunks and their embeddings.

## Troubleshooting

- **`gemini_api.txt` is empty**: Make sure you have created the file and pasted your API key inside.
- **`pe_index.json` not found**: You must run `python build_index.py` before starting the app.
- **Model not found**: Ensure you have access to `models/gemini-2.0-flash` and `models/text-embedding-004`. You can run `python check_models.py` to see what models are available to you.

---
Made by Himani Thakur, Computer Engineering, DBATU-Lonere.

import os
import fitz  # PyMuPDF
import pickle
import faiss
from sentence_transformers import SentenceTransformer

def chunk_text(text, chunk_size=300, chunk_overlap=100):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - chunk_overlap

    return chunks

def upload_and_process_pdf(pdf_file, subject):
    subject_path = f"subjects/{subject}"
    os.makedirs(subject_path, exist_ok=True)

    # Extract and smart-chunk PDF text
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "\n".join([page.get_text() for page in doc])
    chunks = chunk_text(text)

    # Create embeddings
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(chunks, normalize_embeddings=True).astype("float32")

    texts_path = f"{subject_path}/texts.pkl"
    index_path = f"{subject_path}/faiss_index.pkl"

    if os.path.exists(texts_path) and os.path.exists(index_path):
        with open(texts_path, "rb") as f:
            existing_chunks = pickle.load(f)
            if not isinstance(existing_chunks, list):
                existing_chunks = []

        # Load and update FAISS index
        index = faiss.read_index(index_path)
        index.add(embeddings)

        all_chunks = existing_chunks + chunks
    else:
        index = faiss.IndexFlatIP(embeddings.shape[1])
        index.add(embeddings)
        all_chunks = chunks

    # Save updated chunks and index
    with open(texts_path, "wb") as f:
        pickle.dump(all_chunks, f)

    faiss.write_index(index, index_path)

    return len(chunks)

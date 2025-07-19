# setup_manual_pdfs.py
import os
from backend.pdf_utils import extract_text_from_pdf, chunk_text
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import fitz

model = SentenceTransformer("all-MiniLM-L6-v2")

def process_subject(subject_name):
    subject_path = f"subjects/{subject_name}"
    all_chunks = []

    for file in os.listdir(subject_path):
        if file.endswith(".pdf"):
            print(f"📄 Processing: {file}")
            with open(os.path.join(subject_path, file), "rb") as f:
                text = extract_text_from_pdf(f)
                chunks = chunk_text(text)
                all_chunks.extend(chunks)

    if not all_chunks:
        print(f"❌ No chunks extracted for {subject_name}")
        return

    embeddings = model.encode(all_chunks, normalize_embeddings=True).astype("float32")

    # Save text chunks
    with open(os.path.join(subject_path, "texts.pkl"), "wb") as f:
        pickle.dump(all_chunks, f)

    # Save FAISS index
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, os.path.join(subject_path, "faiss_index.pkl"))

    print(f"✅ Completed: {subject_name}")

if __name__ == "__main__":
    process_subject("oop")

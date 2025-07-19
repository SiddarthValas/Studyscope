# --- search_engine.py ---
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_answer_from_notes(question, subject, top_k=3, similarity_threshold=0.6):
    subject_path = f"subjects/{subject}"

    try:
        with open(f"{subject_path}/texts.pkl", "rb") as f:
            chunks = pickle.load(f)
        index = faiss.read_index(f"{subject_path}/faiss_index.pkl")
    except Exception as e:
        print(f"❌ Error loading subject data: {e}")
        return None

    # Embed the question
    query_embedding = model.encode([question], normalize_embeddings=True).astype("float32")

    # Search for top K matches
    distances, indices = index.search(query_embedding, k=top_k)

    # Filter results above the similarity threshold
    valid_results = [(chunks[i], distances[0][idx]) for idx, i in enumerate(indices[0]) if distances[0][idx] >= similarity_threshold]

    if not valid_results:
        print(f"❌ No good match (best similarity {distances[0][0]:.2f}) for: {question}")
        return None

    # Combine top matching chunks for better context
    combined_text = "\n\n".join([chunk for chunk, score in valid_results])
    top_score = valid_results[0][1]

    # ✅ Show full matched note chunk
    print(f"✅ Top match (score {top_score:.2f}):\n{combined_text}\n")

    return combined_text, top_score
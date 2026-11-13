from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from database.db_connection import get_connection

def search_knowledge(query, top_k=3):
    with get_connection() as conn:
        rows = conn.execute("SELECT topic,content FROM travel_knowledge").fetchall()
    if not rows:
        return []
    docs = [f"{r['topic']}. {r['content']}" for r in rows]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(docs + [query])
    scores = cosine_similarity(matrix[-1], matrix[:-1]).flatten()
    ranked = scores.argsort()[::-1][:top_k]
    results = []
    for idx in ranked:
        if scores[idx] > 0:
            results.append({
                "topic": rows[idx]["topic"],
                "content": rows[idx]["content"],
                "score": round(float(scores[idx]), 3)
            })
    return results

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import send_file
import os
import math
from collections import defaultdict

app = Flask(__name__)
CORS(app)

TFIDF_FOLDER = "tfidf_terms"

@app.route("/")
def home():
    return send_file("index.html")


# ---------------------------
# Load documents
# ---------------------------
def load_documents():
    documents = {}

    for filename in os.listdir(TFIDF_FOLDER):
        path = os.path.join(TFIDF_FOLDER, filename)
        doc_id = filename.replace(".txt", "")

        vector = {}

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) != 3:
                    continue

                term, _, tfidf = parts
                vector[term] = float(tfidf)

        documents[doc_id] = vector

    return documents


DOCUMENTS = load_documents()


# ---------------------------
# Query vector
# ---------------------------
def build_query_vector(query):
    words = query.lower().split()
    vec = defaultdict(int)

    for w in words:
        vec[w] += 1

    return dict(vec)


# ---------------------------
# Cosine similarity
# ---------------------------
def cosine_similarity(v1, v2):
    dot = 0
    n1 = 0
    n2 = 0

    keys = set(v1.keys()) | set(v2.keys())

    for k in keys:
        a = v1.get(k, 0)
        b = v2.get(k, 0)

        dot += a * b
        n1 += a * a
        n2 += b * b

    if n1 == 0 or n2 == 0:
        return 0

    return dot / (math.sqrt(n1) * math.sqrt(n2))


# ---------------------------
# Search
# ---------------------------
def search(query):
    q_vec = build_query_vector(query)
    scores = []

    for doc_id, doc_vec in DOCUMENTS.items():
        score = cosine_similarity(q_vec, doc_vec)
        scores.append((doc_id, score))

    scores.sort(key=lambda x: x[1], reverse=True)

    return scores[:10]


# ---------------------------
# API endpoint
# ---------------------------
@app.route("/search")
def search_api():
    query = request.args.get("q", "")
    results = search(query)

    return jsonify([
        {"doc": doc_id, "score": round(score, 4)}
        for doc_id, score in results if score > 0
    ])


# ---------------------------
# Run server
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
import os
import math
from collections import defaultdict

TFIDF_FOLDER = "tfidf_terms"



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

                term, idf, tfidf = parts
                vector[term] = float(tfidf)

        documents[doc_id] = vector

    return documents



def build_query_vector(query):
    words = query.lower().split()
    vector = defaultdict(int)

    for word in words:
        vector[word] += 1

    return dict(vector)



def cosine_similarity(vec1, vec2):
    dot_product = 0
    norm1 = 0
    norm2 = 0

    all_keys = set(vec1.keys()) | set(vec2.keys())

    for key in all_keys:
        v1 = vec1.get(key, 0)
        v2 = vec2.get(key, 0)

        dot_product += v1 * v2
        norm1 += v1 * v1
        norm2 += v2 * v2

    if norm1 == 0 or norm2 == 0:
        return 0

    return dot_product / (math.sqrt(norm1) * math.sqrt(norm2))



# Search

def search(query, documents):
    query_vec = build_query_vector(query)

    scores = []

    for doc_id, doc_vec in documents.items():
        score = cosine_similarity(query_vec, doc_vec)
        scores.append((doc_id, score))

    # sort by score descending
    scores.sort(key=lambda x: x[1], reverse=True)

    return scores


def main():
    print("Loading documents...")
    documents = load_documents()

    while True:
        query = input("\nEnter query (or 'exit'): ")

        if query.lower() == "exit":
            break

        results = search(query, documents)

        print("\nTop results:")
        for doc_id, score in results[:10]:
            if score > 0:
                print(f"Doc {doc_id} → {score:.4f}")


if __name__ == "__main__":
    main()
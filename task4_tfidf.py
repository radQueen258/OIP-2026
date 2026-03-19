import os
import math
import re
from collections import Counter

PAGES_DIR = "pages"
TOKENS_FILE = "tokens.txt"
LEMMAS_FILE = "lemmas.txt"

TFIDF_TERMS_DIR = "tfidf_terms"
TFIDF_LEMMAS_DIR = "tfidf_lemmas"


os.makedirs(TFIDF_TERMS_DIR, exist_ok=True)
os.makedirs(TFIDF_LEMMAS_DIR, exist_ok=True)



def tokenize(text):
    text = text.lower()
    return re.findall(r"[a-z]+", text)


def load_list(filename):
    items = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            items.append(line.strip())
    return items



def load_documents():
    docs = {}

    for file in os.listdir(PAGES_DIR):
        doc_id = file.split(".")[0]

        with open(os.path.join(PAGES_DIR, file), "r", encoding="utf-8") as f:
            text = f.read()

        tokens = tokenize(text)

        docs[doc_id] = tokens

    return docs


def compute_idf(terms, docs):

    N = len(docs)
    df_count = {term: 0 for term in terms}

    for tokens in docs.values():
        unique_terms = set(tokens)

        for term in unique_terms:
            if term in df_count:
                df_count[term] += 1

    idf = {}

    for term, df in df_count.items():
        if df == 0:
            idf[term] = 0
        else:
            idf[term] = math.log(N / df)

    return idf


# -----------------------------
# TF
# -----------------------------
def compute_tf(tokens):
    total = len(tokens)
    counts = Counter(tokens)
    return {term: count / total for term, count in counts.items()}


# -----------------------------
# SAVE TF-IDF
# -----------------------------
def save_tfidf(doc_id, terms, tf, idf, output_dir):

    output_path = os.path.join(output_dir, f"{doc_id}.txt")

    results = []

    for term in terms:
        tf_val = tf.get(term, 0)
        idf_val = idf.get(term, 0)
        tfidf = tf_val * idf_val

        results.append((term, idf_val, tfidf))

  
    results.sort(key=lambda x: x[2], reverse=True)

    with open(output_path, "w", encoding="utf-8") as f:
        for term, idf_val, tfidf in results:
            f.write(f"{term} {idf_val} {tfidf}\n")


def main():

    print("Loading data...")

    terms = load_list(TOKENS_FILE)
    lemmas = load_list(LEMMAS_FILE)

    docs = load_documents()

    print("Computing IDF...")

    idf_terms = compute_idf(terms, docs)
    idf_lemmas = compute_idf(lemmas, docs)

    print("Computing TF-IDF...")

    for doc_id, tokens in docs.items():

        tf = compute_tf(tokens)

        save_tfidf(doc_id, terms, tf, idf_terms, TFIDF_TERMS_DIR)
        save_tfidf(doc_id, lemmas, tf, idf_lemmas, TFIDF_LEMMAS_DIR)

    print("TF-IDF calculation finished.")


if __name__ == "__main__":
    main()
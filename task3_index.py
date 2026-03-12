import os
import json
import re
from collections import defaultdict

PAGES_DIR = "pages"
INDEX_FILE = "inverted_index.json"


def tokenize(text):
    text = text.lower()
    tokens = re.findall(r"[a-z]+", text)
    return tokens


def build_index():
    inverted_index = defaultdict(set)

    files = sorted(os.listdir(PAGES_DIR))

    for file in files:
        doc_id = file.split(".")[0]

        with open(os.path.join(PAGES_DIR, file), "r", encoding="utf-8") as f:
            text = f.read()

        tokens = tokenize(text)

        for token in tokens:
            inverted_index[token].add(doc_id)

    # convert sets → lists (for JSON)
    inverted_index = {k: sorted(list(v)) for k, v in inverted_index.items()}

    return inverted_index


def save_index(index):
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)


if __name__ == "__main__":
    index = build_index()
    save_index(index)

    print("Inverted index created.")
    print("Total terms:", len(index))

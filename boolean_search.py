import json
import re

INDEX_FILE = "inverted_index.json"


def load_index():
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def tokenize_query(query):
    tokens = re.findall(r'\w+|AND|OR|NOT|\(|\)', query)
    return tokens


def search(query, index):
    tokens = tokenize_query(query)
    stack = []

    all_docs = set()
    for docs in index.values():
        all_docs.update(docs)

    for token in tokens:

        if token == "AND":
            b = stack.pop()
            a = stack.pop()
            stack.append(a & b)

        elif token == "OR":
            b = stack.pop()
            a = stack.pop()
            stack.append(a | b)

        elif token == "NOT":
            a = stack.pop()
            stack.append(all_docs - a)

        elif token not in ["(", ")"]:
            docs = set(index.get(token.lower(), []))
            stack.append(docs)

    return stack.pop()


def main():
    index = load_index()

    query = input("Enter query: ")

    result = search(query, index)

    print("Documents:", sorted(result))


if __name__ == "__main__":
    main()

import json
import re

INDEX_FILE = "inverted_index.json"


def load_index():
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_all_docs(index):
    docs = set()
    for d in index.values():
        docs.update(d)
    return docs


def tokenize(query):
    return re.findall(r'\(|\)|AND|OR|NOT|\w+', query)


def to_postfix(tokens):
    precedence = {"NOT": 3, "AND": 2, "OR": 1}
    output = []
    stack = []

    for token in tokens:
        if token not in ("AND", "OR", "NOT", "(", ")"):
            output.append(token)

        elif token == "(":
            stack.append(token)

        elif token == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            stack.pop()

        else:
            while (stack and stack[-1] != "(" and
                   precedence.get(stack[-1], 0) >= precedence[token]):
                output.append(stack.pop())
            stack.append(token)

    while stack:
        output.append(stack.pop())

    return output


def evaluate(postfix, index):

    all_docs = get_all_docs(index)
    stack = []

    for token in postfix:

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

        else:
            stack.append(set(index.get(token.lower(), [])))

    return stack.pop()


def search(query, index):
    tokens = tokenize(query)
    postfix = to_postfix(tokens)
    return evaluate(postfix, index)


def main():

    index = load_index()

    query = input("Enter query: ")

    result = search(query, index)

    print("Documents:", sorted(result))


if __name__ == "__main__":
    main()
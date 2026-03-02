!pip install spacy beautifulsoup4
!python -m spacy download en_core_web_sm

import os
import re
from bs4 import BeautifulSoup
import spacy
from collections import defaultdict

nlp = spacy.load("en_core_web_sm")

import os
import requests
import time

OUTPUT_DIR = "pages"
os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; OIP-2026-Crawler)"
}

with open("/content/OIP-2026/links", "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]

print("Total URLs:", len(urls))

index_lines = []

for i, url in enumerate(urls, start=1):
    try:
        print(f"Downloading {i}: {url}")
        response = requests.get(url, headers=HEADERS, timeout=15)

        if "text/html" in response.headers.get("Content-Type", ""):
            file_path = os.path.join(OUTPUT_DIR, f"{i}.txt")

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(response.text)

            index_lines.append(f"{i} {url}")

        time.sleep(1)

    except Exception as e:
        print("Error:", e)

with open("index.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(index_lines))

print("Download complete.")

PAGES_DIR = "pages"

def extract_text(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    
    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    return text

def clean_token(token):
    token = token.lower()

    
    if not token.isalpha():
        return None

    return token

all_tokens = set()

for filename in os.listdir(PAGES_DIR):
    file_path = os.path.join(PAGES_DIR, filename)

    if os.path.isfile(file_path):
        text = extract_text(file_path)

        doc = nlp(text)

        for token in doc:
            if token.is_stop:
                continue

            word = token.text.lower()

            if word.isalpha():      
                all_tokens.add(word)

print("Total unique clean tokens:", len(all_tokens))

lemma_dict = defaultdict(set)

for word in all_tokens:
    doc = nlp(word)
    lemma = doc[0].lemma_

    if lemma.isalpha():
        lemma_dict[lemma].add(word)

print("Total lemmas:", len(lemma_dict))

with open("tokens.txt", "w", encoding="utf-8") as f:
    for token in sorted(all_tokens):
        f.write(token + "\n")



with open("lemmas.txt", "w", encoding="utf-8") as f:
    for lemma in sorted(lemma_dict.keys()):
        forms = sorted(lemma_dict[lemma])
        line = lemma + " " + " ".join(forms)
        f.write(line + "\n")



from google.colab import files
files.download("tokens.txt")
files.download("lemmas.txt")

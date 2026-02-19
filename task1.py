import os
import time
import requests

URLS_FILE = "/content/links.txt"
OUTPUT_DIR = "/content/sample_data/pages"
INDEX_FILE = "/content/source.txt"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ColabCrawler/1.0)"
}

TIMEOUT = 15
DELAY_SECONDS = 1


def read_urls(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def is_html(response):
    content_type = response.headers.get("Content-Type", "")
    return "text/html" in content_type


def download_page(url):
    response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    if not is_html(response):
        raise ValueError("Non-HTML content")
    return response.text


def main():
    urls = read_urls(URLS_FILE)

    if len(urls) < 100:
        print("ERROR: urls.txt must contain at least 100 URLs")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    index_lines = []
    file_number = 1

    for url in urls:
        print(f"[{file_number}] Downloading: {url}")

        try:
            html = download_page(url)

            file_path = os.path.join(OUTPUT_DIR, f"{file_number}.txt")

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html)

            index_lines.append(f"{file_number} {url}")
            print("   Saved successfully.")

            file_number += 1

        except Exception as e:
            print(f"   Skipped: {e}")

        time.sleep(DELAY_SECONDS)

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(index_lines))

    print("\nDONE!")
    print(f"Downloaded pages: {file_number - 1}")
    print(f"Index file saved as: {INDEX_FILE}")


main()

import csv
import requests
from bs4 import BeautifulSoup

URL = "https://quotes.toscrape.com/"

def scrape_quotes():
    response = requests.get(URL, timeout=10, headers={"User-Agent": "CodingSamuraiInternship/1.0"})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    rows = []
    for quote in soup.select(".quote"):
        text = quote.select_one(".text").get_text(strip=True)
        author = quote.select_one(".author").get_text(strip=True)
        rows.append({"quote": text, "author": author})
    return rows

def save_csv(rows, filename="quotes.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["quote", "author"])
        writer.writeheader()
        writer.writerows(rows)

def main():
    try:
        rows = scrape_quotes()
        save_csv(rows)
        print(f"Scraped {len(rows)} quotes and saved them to quotes.csv")
    except requests.RequestException as exc:
        print(f"Request failed: {exc}")

if __name__ == "__main__":
    main()

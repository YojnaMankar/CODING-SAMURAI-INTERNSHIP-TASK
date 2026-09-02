import csv
import json
import time
import requests
from bs4 import BeautifulSoup


BASE_URL = "https://quotes.toscrape.com/"
HEADERS = {
    "User-Agent": "CodingSamuraiInternship/1.0"
}


def scrape_page(url):
    """Scrape quotes from one page."""

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=10
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    quotes = []

    for quote in soup.select(".quote"):
        text = quote.select_one(".text").get_text(strip=True)
        author = quote.select_one(".author").get_text(strip=True)

        tag_elements = quote.select(".tags .tag")
        tags = [
            tag.get_text(strip=True)
            for tag in tag_elements
        ]

        quotes.append({
            "quote": text,
            "author": author,
            "tags": ", ".join(tags)
        })

    next_button = soup.select_one(".next a")

    if next_button:
        next_url = BASE_URL.rstrip("/") + next_button["href"]
    else:
        next_url = None

    return quotes, next_url


def scrape_quotes(max_pages):
    """Scrape quotes from multiple pages."""

    all_quotes = []
    url = BASE_URL

    for page_number in range(1, max_pages + 1):

        print(f"\n🔎 Scraping page {page_number}...")

        try:
            quotes, next_url = scrape_page(url)

            all_quotes.extend(quotes)

            print(f"   ✅ Found {len(quotes)} quotes")

            if not next_url:
                print("   ℹ️ No more pages available.")
                break

            url = next_url

            # Polite delay between requests
            time.sleep(1)

        except requests.exceptions.Timeout:
            print("❌ Request timed out.")
            break

        except requests.exceptions.ConnectionError:
            print("❌ Internet connection error.")
            break

        except requests.exceptions.HTTPError as error:
            print(f"❌ HTTP error: {error}")
            break

        except requests.exceptions.RequestException as error:
            print(f"❌ Request failed: {error}")
            break

    return remove_duplicates(all_quotes)


def remove_duplicates(quotes):
    """Remove duplicate quotes."""

    unique_quotes = []
    seen = set()

    for item in quotes:
        quote_text = item["quote"]

        if quote_text not in seen:
            seen.add(quote_text)
            unique_quotes.append(item)

    return unique_quotes


def filter_quotes(quotes, keyword=None, author=None):
    """Filter quotes by keyword or author."""

    filtered = quotes

    if keyword:
        keyword = keyword.lower()

        filtered = [
            item for item in filtered
            if keyword in item["quote"].lower()
            or keyword in item["tags"].lower()
        ]

    if author:
        author = author.lower()

        filtered = [
            item for item in filtered
            if author in item["author"].lower()
        ]

    return filtered


def save_csv(quotes, filename="quotes.csv"):
    """Save scraped data as CSV."""

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["quote", "author", "tags"]
        )

        writer.writeheader()
        writer.writerows(quotes)


def save_json(quotes, filename="quotes.json"):
    """Save scraped data as JSON."""

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            quotes,
            file,
            indent=4,
            ensure_ascii=False
        )


def display_quotes(quotes, limit=10):
    """Display quotes in terminal."""

    print("\n" + "=" * 70)
    print("                 SCRAPED QUOTES")
    print("=" * 70)

    if not quotes:
        print("📭 No quotes found.")
        return

    for index, item in enumerate(quotes[:limit], start=1):

        print(f"\n{index}. {item['quote']}")
        print(f"   👤 Author : {item['author']}")
        print(f"   🏷️ Tags   : {item['tags']}")

    if len(quotes) > limit:
        print(
            f"\n... and {len(quotes) - limit} more quotes."
        )


def main():

    print("\n" + "=" * 70)
    print("             🕷️ ADVANCED WEB SCRAPER")
    print("=" * 70)

    while True:

        try:
            pages_input = input(
                "\nHow many pages do you want to scrape? (1-10): "
            ).strip()

            pages = int(pages_input)

            if 1 <= pages <= 10:
                break

            print("❌ Please enter a number between 1 and 10.")

        except ValueError:
            print("❌ Please enter a valid number.")

    quotes = scrape_quotes(pages)

    print("\n" + "=" * 70)
    print("                 SCRAPING COMPLETE")
    print("=" * 70)

    print(f"📄 Pages requested : {pages}")
    print(f"💬 Total quotes    : {len(quotes)}")

    if not quotes:
        print("❌ No data was scraped.")
        return

    save_csv(quotes)
    save_json(quotes)

    print("\n💾 Data saved successfully:")
    print("   📄 quotes.csv")
    print("   📄 quotes.json")

    keyword = input(
        "\n🔍 Enter keyword to filter (or press Enter to skip): "
    ).strip()

    author = input(
        "👤 Enter author to filter (or press Enter to skip): "
    ).strip()

    filtered_quotes = filter_quotes(
        quotes,
        keyword=keyword if keyword else None,
        author=author if author else None
    )

    print(
        f"\n🔎 Matching quotes: {len(filtered_quotes)}"
    )

    display_quotes(filtered_quotes)

    print("\n🎉 Web Scraper finished successfully!")


if __name__ == "__main__":
    main()
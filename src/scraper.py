import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://books.toscrape.com/"

def get_page_content(url):
    """
    Fetch HTML content from a given URL.
    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text

def parse_books(html):
    """
    Parse book data from HTML content.
    """
    soup = BeautifulSoup(html, "html.parser")
    books = []

    for book in soup.select(".product_pod"):
        title = book.h3.a["title"]
        price = book.select_one(".price_color").text.strip()
        availability = book.select_one(".availability").text.strip()
        link = BASE_URL + book.h3.a["href"]

        books.append({
            "Title": title,
            "Price": price,
            "Availability": availability,
            "Link": link
        })

    return books

def save_to_csv(data, filename):
    """
    Save scraped data to a CSV file.
    """
    if not data:
        print("No data to save.")
        return

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    print(f"Saved {len(data)} records to {filename}")

def main():
    print("Starting web scrape...")
    html = get_page_content(BASE_URL)
    books = parse_books(html)
    save_to_csv(books, "output/books.csv")

if __name__ == "__main__":
    main()

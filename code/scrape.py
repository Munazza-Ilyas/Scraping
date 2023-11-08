import os
import json
import csv

from scrape_pages import scrape_all_pages
from scrape_books import scrape_books


def scrape():
    """Scrape everything and return a list of books."""
    
    book_urls = scrape_all_pages()

    books_info = scrape_books(book_urls)

    return books_info

def write_books_to_csv(books, path):
    with open(path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=books[0].keys())
        writer.writeheader()
        writer.writerows(books)


def write_books_to_jsonl(books, path):
    with open(path, 'w', encoding='utf-8') as jsonl_file:
        for book in books:
            jsonl_file.write(json.dumps(book) + '\n')

if __name__ == "__main__":

    BASE_DIR = "artifacts"
    CSV_PATH = os.path.join(BASE_DIR, "results.csv")
    JSONL_PATH = os.path.join(BASE_DIR, "results.jsonl")

    os.makedirs(BASE_DIR, exist_ok=True)

    books = scrape()

    write_books_to_csv(books, CSV_PATH)
    write_books_to_jsonl(books, JSONL_PATH)

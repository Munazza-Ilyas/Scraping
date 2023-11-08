from common import get_soup
import re


def extract_price(price_str):
    """Extracts the price form the string in the product description as a float."""
    pattern = r"£(\d+\.\d+)"
    match = re.search(pattern, price_str)
    
    if match:
        return float(match.group(1))
    
    return None

def extract_stock(stock_str):
    """Extracts the count form the string in the product description as an int."""
    pattern = r"(\d+)"
    match = re.search(pattern, stock_str)
    
    if match:
        return int(match.group(1))
    return None


def get_category(soup):
    """Extracts the category from the BeautifulSoup instance representing a book page as a string."""

    breadcrumb_tag = soup.find_all("ul", class_="breadcrumb")[0]
    a_tags = breadcrumb_tag.find_all("a")

    return a_tags[2].text.strip() if len(a_tags) > 2 else None



def get_title(soup):
    """Extracts the title from the BeautifulSoup instance representing a book page as a string."""

    title = soup.find("h1")
    return title.text.strip() if title else None


def get_description(soup):
    """Extracts the description from the BeautifulSoup instance representing a book page as a string."""

    meta_description = soup.find("meta", {"name": "description"})
    return meta_description['content'].strip() if meta_description else None


def get_product_information(soup):
    """Extracts the product information from the BeautifulSoup instance representing a book page as a dict."""

    product_info = {}

    product_info['upc'] = soup.find('th', text='UPC').find_next('td').text.strip()
    price_str = soup.find('p', class_='price_color').text
    product_info['price_gbp'] = extract_price(price_str)
    
    stock_str = soup.find('th', text='Availability').find_next('td').text
    product_info['stock'] = extract_stock(stock_str)

    return product_info


def scrape_book(book_url):
    """Extracts all information from a book page and returns a dict."""

    soup = get_soup(book_url)
    if soup:
        book_info = {}
        book_info['upc'] = soup.find('th', text='UPC').find_next('td').text.strip()
        book_info['title'] = get_title(soup)
        book_info['category'] = get_category(soup)
        book_info['description'] = get_description(soup)
        product_info = get_product_information(soup)
        book_info['price_gbp'] = product_info['price_gbp']
        book_info['stock'] = product_info['stock']
        return book_info
    else:
        return None


def scrape_books(book_urls):
    """Extracts all information from a list of book page and returns a list of dicts."""

    books_info = []
    
    for url in book_urls:
        book_info = scrape_book(url)
        if book_info:
            books_info.append(book_info)
    
    return books_info


if __name__ == "__main__":

    # code for testing

    # set up fixtures for testing

    book_url = "http://books.toscrape.com/catalogue/the-secret-of-dreadwillow-carse_944/index.html"
    book_url_no_description = "http://books.toscrape.com/catalogue/the-bridge-to-consciousness-im-writing-the-bridge-between-science-and-our-old-and-new-beliefs_840/index.html"

    soup = get_soup(book_url)
    soup_no_description = get_soup(book_url_no_description)

    # test extract_price

    assert extract_price("£56.13") == 56.13

    # test extract_stock

    assert extract_stock("In stock (16 available)") == 16

    # test get_category

    assert get_category(soup) == "Childrens"

    # test get_title

    assert get_title(soup) == "The Secret of Dreadwillow Carse"

    # test get_description

    assert get_description(soup) is not None
    

    # test get_product_information

    product_information = get_product_information(soup)

    assert set(product_information.keys()) == {"upc", "price_gbp", "stock"}

    assert product_information == {
        "upc": "b5ea0b5dabed25a8",
        "price_gbp": 56.13,
        "stock": 16,
    }

    # test scrape_book

    book = scrape_book(book_url)
    book_no_description = scrape_book(book_url_no_description)

    expected_keys = {"title", "category", "description", "upc", "price_gbp", "stock"}

    assert set(book.keys()) == expected_keys
    assert set(book_no_description.keys()) == expected_keys

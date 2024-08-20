import requests;
from bs4 import BeautifulSoup;
import json;


def fetch_books(page_num):
    url = f"https://books.toscrape.com/catalogue/page-{page_num}.html";
    response = requests.get(url);
    soup = BeautifulSoup(response.text, 'html.parser');
    books = [];
    book_elements = soup.find_all('article', class_='product_pod');

    for book in book_elements:
        # book data to scrape;
        title = book.find('h3').find('a')['title'];
        price = book.find('p', class_='price_color').text;
        availability = 'In Stock' if 'In stock' in book.find('p', class_='instock availability').text else 'Out of Stock';
        rating = book.find('p', class_='star-rating')['class'][1];
        link = book.find('h3').find('a')['href'];

        books.append({
            'title': title,
            'price': price,
            'rating': rating,
            'availability': availability,
            'link': f'https://books.toscrape.com/catalogue/{link}',
        });

    return books;


def main():
    # Pagination
    all_books = [];
    max_pages = 10;
    for current_page in range(1, max_pages + 1):
        books_on_page = fetch_books(current_page);
        all_books.extend(books_on_page);
        print(f'Books on Page: {current_page}: ');

    # Save all_books data to a file
    with open('books.json', 'w') as f:
        json.dump(all_books, f, indent=2);

    print('Data saved to books.json');


if __name__ == "__main__":
    main();
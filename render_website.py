import json
import os
from math import ceil
from more_itertools import ichunked
from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape

BOOKS_FILENAME = 'books.json'


def get_books_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        books = json.loads(file.read())

    for book in books:
        book['image_src'] = book['image_src'].replace('\\', '/')
        book['book_path'] = book['book_path'].replace('\\', '/')

    return books


def on_reload():
    os.makedirs('pages', exist_ok=True)
    books_per_page = 10
    books = get_books_from_json(BOOKS_FILENAME)

    for page, block_books in enumerate(ichunked(books, books_per_page), start=1):
        env = Environment(
            loader=FileSystemLoader('.'),
            autoescape=select_autoescape(['html', 'xml'])
        )

        template = env.get_template('template.html')

        rendered_page = template.render(
            books=block_books,
            page=page,
            max_pages=ceil(len(books) / books_per_page),
        )

        path_page = os.path.join('pages', f'index{str(page)}.html')
        with open(path_page, 'w', encoding="utf8") as file:
            file.write(rendered_page)


if __name__ == '__main__':
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')

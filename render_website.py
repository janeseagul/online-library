import json
from livereload import Server

from jinja2 import Enviroment, FileSystemLoader, select_autoescape


BOOKS_FILENAME = 'books.json'


def get_books_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        books = json.loads(file.read())

    for book in books:
        book['img_src'] = book['img_src'].replace('\\', '/')
        book['book_path'] = book['book_path'].replace('\\', '/')

    return books


def on_reload():
    books = get_books_from_json(BOOKS_FILENAME)

    env = Enviroment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    render_page = template.render(
        books=books
    )
    with open('index.html', 'w', encoding='utf8') as file:
        file.write(render_page)


if __name__=='__main__':
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')
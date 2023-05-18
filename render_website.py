import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Enviroment, FileSystemLoader, select_autoescape


def main(books):
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

    server = HTTPServer(('127.0.0.1', 8000),
                        SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__=='__main__':
    with open ('books.json', 'r', encoding='utf-8') as file:
        books = json.loads(file.read())
    for book in books:
        book['img_src'] = book['img_src'].replace('\\', '/')
        book['book_path'] = book['book_path'].replace('\\', '/')

main(books)
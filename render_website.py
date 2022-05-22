from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_downloaded_books(filepath: str='books.json') -> list:
    '''Load information about already downloaded books from json-file.'''
    if os.path.isfile(filepath):
        with open(filepath, 'r', encoding='utf-8') as books_file:
            return json.load(books_file)
    return list()


def main():
    '''.'''
    books = get_downloaded_books()

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        books=books,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()



if __name__ == '__main__':
    main()

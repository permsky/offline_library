import json
import math
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def get_downloaded_books(filepath: str='books.json') -> list:
    '''
        Load information about already downloaded books from json file.
    '''
    if os.path.isfile(filepath):
        with open(filepath, 'r', encoding='utf-8') as books_file:
            return json.load(books_file)
    return list()


def rebuild() -> None:
    '''Render html file for every page.'''
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    folder = 'pages'
    os.makedirs(folder, exist_ok=True)
    books = get_downloaded_books()
    page_count = math.ceil(len(books) / 10)
    for number, chunk in enumerate(chunked(books, 10)):
        rendered_page = template.render(
            pairs=chunked(chunk, 2),
            current_page=number + 1,
            page_count=page_count,
        )
        filepath = os.path.join(folder, f'index{number + 1}.html')
        with open(filepath, 'w', encoding="utf8") as file:
            file.write(rendered_page)


def on_reload() -> None:
    '''Watch for changes in template.html and rebuild index.html.'''
    server = Server()
    server.watch('template.html', rebuild)
    server.serve(
        root='.',
        port=8000,
        host='localhost',
        default_filename='pages/index1.html'
    )


def main():
    '''Serve library.'''
    rebuild()
    on_reload()


if __name__ == '__main__':
    main()

import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


def get_downloaded_books(filepath: str='books.json') -> list:
    '''Load information about already downloaded books from json-file.'''
    if os.path.isfile(filepath):
        with open(filepath, 'r', encoding='utf-8') as books_file:
            return json.load(books_file)
    return list()


def rebuild() -> None:
    '''Render index.html.'''
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    rendered_page = template.render(
        books=get_downloaded_books(),
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def on_reload() -> None:
    '''Watch for changes in template.html and rebuild index.html.'''
    server = Server()
    server.watch('template.html', rebuild)
    server.serve(root='.', port=8000, host='localhost')


def main():
    '''Serve library.'''
    rebuild()
    on_reload()


if __name__ == '__main__':
    main()

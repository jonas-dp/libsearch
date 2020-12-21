import json
import os
from pathlib import Path

from src.utils.Singleton import Singleton
from src.Book import Book
from src.Catalogue import Catalogue


class Cache(Singleton, object):

    catalogue = None
    tokens = None

    cache_dir = os.path.join(Path(os.path.dirname(__file__)).parent, 'cache')
    tokens_cache_path = os.path.join(cache_dir, '.tokens')
    catalogue_cache_path = os.path.join(cache_dir, '.catalogue.json')

    def __init__(self):
        if not os.path.exists(self.cache_dir):
            os.mkdir(self.cache_dir)

    def load_catalogue(self):
        if os.path.exists(self.catalogue_cache_path):
            with open(self.catalogue_cache_path) as catalogue_cache:
                self.catalogue = json.load(catalogue_cache)

    def save_catalogue(self, catalogue: Catalogue):
        with open(self.catalogue_cache_path, 'w') as catalogue_cache:
            dicts = [
                book.__dict__ for book in catalogue.books if book.frabl is not None]
            catalogue_cache.write(json.dumps(dicts))

        self.catalogue = dicts

    def get_book(self, goodreads_id: str):
        if self.catalogue is None:
            return None

        found_book = next(
            (book for book in self.catalogue if book['goodreads_id'] == goodreads_id), None)
        if found_book is None:
            return None

        book = Book(found_book['author'],
                    found_book['title'], found_book['goodreads_id'])
        book.frabl = found_book['frabl']
        book.cover_url = found_book['cover_url']
        book.isbn = found_book.get('isbn')
        book.pages = found_book.get('pages')
        book.library_page = found_book['library_page']
        book.goodreads_page = found_book['goodreads_page']
        book.status = found_book['status']
        book.formats = found_book.get('formats')
        book.cloudlibrary_id = found_book.get('cloudlibrary_id')

        return book

    def load_tokens(self):
        if os.path.exists(self.tokens_cache_path):
            with open(self.tokens_cache_path) as tokens_cache:
                self.tokens = json.load(tokens_cache)

            return self.tokens

        return None

    def save_access_tokens(self, access_token: str, access_token_secret: str):
        with open(self.tokens_cache_path, 'w') as token_file:
            token_file.write(json.dumps({
                'token': access_token,
                'secret': access_token_secret
            }))

from src.utils.Singleton import Singleton


class Catalogue(Singleton, object):

    books = None

    def set_books(self, books: list):
        self.books = books

    def get_available_books(self):
        return [book for book in self.books if book.is_available]

    def get_unavailable_books(self):
        return [book for book in self.books if not book.is_available and len(book.availabilities) > 0]

    def get_books_with_no_availables(self):
        return [book for book in self.books if not book.is_available and len(book.availabilities) == 0 and book.frabl is not None]

    def get_not_found_books(self):
        return [book for book in self.books if book.frabl is None]

import asyncio

from src.Clients.Cultuurconnect import Cultuurconnect
from src.Clients.Goodreads import Goodreads
from src.HTMLOutput import HTMLOutput
from src.Configuration import Configuration
from src.Cache import Cache
from src.Catalogue import Catalogue

def main():

    Configuration().load()
    books = Goodreads().get_books()

    catalogue = Catalogue()
    catalogue.set_books(books)

    cultuurconnect = Cultuurconnect()
    loop = asyncio.get_event_loop()
    catalogue.books = loop.run_until_complete(cultuurconnect.search_books(catalogue.books))

    Cache().save_catalogue(catalogue)

    books = loop.run_until_complete(cultuurconnect.get_availibities_of_books(catalogue.books))
    loop.close()

    HTMLOutput().createHTML(catalogue)
    HTMLOutput().openHTML()


if __name__ == "__main__":
    main()
    
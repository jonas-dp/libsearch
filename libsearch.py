import asyncio
import webbrowser
from src.Clients.Cultuurconnect import Cultuurconnect

from src.Clients.Goodreads import Goodreads
from src.HTMLOutput import HTMLOutput
from src.JSONOutput import JSONOutput
from src.Configuration import Configuration
from src.Cache import Cache
from src.Catalogue import Catalogue
from src.UI.ProgressBar import ProgressBar
from src.WebServer import WebServer

def main():

    Configuration().load()

    ProgressBar().print(0, 3, 'Retrieving books from Goodreads...')
    books = Goodreads().get_books()

    catalogue = Catalogue()
    catalogue.set_books(books)

    cultuurconnect = Cultuurconnect()
    loop = asyncio.get_event_loop()
    ProgressBar().print(1, 3, 'Retrieving books from library catalogue...')
    catalogue.books = loop.run_until_complete(
        cultuurconnect.search_books(catalogue.books))

    Cache().save_catalogue(catalogue)
    ProgressBar().print(2, 3, 'Retrieving availabilities...              ')
    books = loop.run_until_complete(
        cultuurconnect.get_availibities_of_books(catalogue.books))
    loop.close()

    ProgressBar().print(3, 3, 'Creating output...')
    JSONOutput().dump_info(catalogue)
    webbrowser.open('http://127.0.0.1:8080')
    WebServer().run()
    # HTMLOutput().createHTML(catalogue)
    # HTMLOutput().openHTML()


if __name__ == "__main__":
    main()

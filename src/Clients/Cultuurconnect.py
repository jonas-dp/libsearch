import aiohttp
import asyncio
import xml.etree.ElementTree as et
import datetime

from src.utils.Singleton import Singleton
from src.Book import Book
from src.Availability import Availability
from src.Cache import Cache
from src.Configuration import Configuration

class Cultuurconnect(Singleton, object):

    base_url = 'https://cataloguswebservices.bibliotheek.be'

    def __init__(self):
        self.branches = Configuration().cultuurconnect['branches']

    async def search_book(self, book: Book, session):
        cached_book = Cache().get_book(book.goodreads_id)
        if cached_book is not None:
            return cached_book

        url = '{0}/oostvlaanderen/search/?q=title:{1} AND author:{2}&authorization={3}'.format(self.base_url, book.title, book.author, Configuration().cultuurconnect['auth_key'])
        async with session.get(url) as response:
            tree = et.fromstring(await response.text())

            if not tree.find('.//results'):
                print('\033[91m {} by {} not found\033[00m'.format(book.title, book.author))
                return book
            else:
                print('{} by {} found'.format(book.title, book.author))
                book.author = tree.find(".//main-author").text
                book.title = tree.find('.//title').text
                book.frabl = tree.find('.//frabl').text
                book.vlacc = tree.find('.//id').get('nativeid')
                book.isbn = tree.find('.//normalized-isbn-id').text
                book.pages = tree.find('.//physical-description').text
                book.detail_page = tree.find('.//detail-page').text
                return book

    async def search_books(self, books: list):
        Cache().load_catalogue()
        async with aiohttp.ClientSession() as session:
            tasks = [self.search_book(book, session) for book in books]
            return await asyncio.gather(*tasks)

    async def get_availibities_of_books(self, books: list):
        async with aiohttp.ClientSession() as session:
            tasks = [self.get_book_availabilities(book, session) for book in books]
            return await asyncio.gather(*tasks)

    async def get_book_availabilities(self, book: Book, session):
        if book.frabl is None:
            return book

        for branch_config in self.branches:
            url = '{0}/{1}/availability/?frabl={2}&authorization={3}'.format(self.base_url, branch_config["name"], book.frabl, Configuration().cultuurconnect['auth_key'])
            async with session.get(url) as response:
                tree = et.fromstring(await response.text())

                if tree.find('.//error'):
                    continue

                for branch in tree.findall('.//locations/location'):
                    for library in branch.findall('.//location'):

                        if "libraries" in branch_config and library.get('name') not in branch_config["libraries"]:
                            continue

                        for item in library.findall('.//item'):
                            avail = Availability(
                                item.get('available') == 'true',
                                branch.get('name'),
                                library.get('name'),
                                item.find('status').text,
                                item.find('subloc').text,
                                item.find('shelfmark').text,
                                item.find('publication').text
                            )

                            avail.link = tree.find('.//detail-page').text + item.get('extid')

                            if item.find('zizo') is not None:
                                avail.zizo_image_url = item.find('zizo').get('image')

                            if item.find('returndate') is not None:
                                returndate = item.find('returndate').text
                                returndate = datetime.date(int(returndate[6:11]), int(returndate[3:5]), int(returndate[0:2]))
                                avail.return_date = returndate

                            book.add_availablity(avail)          

        if len(book.availabilities) > 0 :
            print("{} availabilities found for {} by {}".format(len(book.availabilities), book.title, book.author))
        else:
            print("\033[91m No availabilities found for {} by {}\033[00m".format(book.title, book.author))

        return book

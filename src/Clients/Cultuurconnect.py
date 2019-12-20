import aiohttp
import asyncio
import xml.etree.ElementTree as et
import datetime
import re

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

        url = '{0}/oostvlaanderen/search/?q=title:{1} AND author:{2}&authorization={3}'.format(
            self.base_url, book.title, book.author, Configuration().cultuurconnect['auth_key'])
        async with session.get(url) as response:
            tree = et.fromstring(await response.text())

            if not tree.find('.//results'):
                return book
            else:
                book.status = 'NO_AVAILABILITIES'

                book.author = tree.find(".//main-author").text
                book.title = tree.find('.//title').text
                book.frabl = tree.find('.//frabl').text
                book.isbn = tree.find('.//normalized-isbn-id').text
                book.pages = tree.find('.//physical-description').text
                book.library_page = tree.find('.//detail-page').text

                vlacc = tree.find('.//id').get('nativeid')
                book.cover_url = 'https://webservices.bibliotheek.be/index.php?func=cover&ISBN={0}&VLACCnr={1}&CDR=&EAN=&ISMN=&coversize=medium'.format(book.isbn, vlacc)
                return book

    async def search_books(self, books: list):
        Cache().load_catalogue()
        async with aiohttp.ClientSession() as session:
            tasks = [self.search_book(book, session) for book in books]
            return await asyncio.gather(*tasks)

    async def get_availibities_of_books(self, books: list):
        async with aiohttp.ClientSession() as session:
            tasks = [self.get_book_availabilities(
                book, session) for book in books]
            return await asyncio.gather(*tasks)

    async def get_book_availabilities(self, book: Book, session):

        def create_availability(item, branch_name, library_name):
            avail = Availability(
                item.get('available') == 'true',
                branch_name,
                library_name,
                item.find('status').text,
                item.find('subloc').text,
                item.find('publication').text
            )

            if item.find('shelfmark') is not None:
                avail.shelfmark = item.find('shelfmark').text

            avail.link = tree.find(
                './/detail-page').text + item.get('extid')
            
            zizo = item.find('zizo')
            if zizo is not None and zizo.get('code') is not '':
                avail.zizo_image_url = item.find(
                    'zizo').get('image')

            if item.find('returndate') is not None:
                returndate = item.find('returndate').text
                returndate = datetime.date(int(returndate[6:11]), int(
                    returndate[3:5]), int(returndate[0:2]))
                avail.return_date = returndate
            
            return avail

        if book.frabl is None:
            return book

        for branch_config in self.branches:
            branch_name = re.sub('[^a-zA-Z ]', '', branch_config["name"])
            url = '{0}/{1}/availability/?frabl={2}&authorization={3}'.format(
                self.base_url, branch_name, book.frabl, Configuration().cultuurconnect['auth_key'])
            async with session.get(url) as response:
                tree = et.fromstring(await response.text())

                if tree.find('.//error'):
                    continue

                book.status = 'UNAVAILABLE'
                
                branch = tree.find('.//locations/location')
                libraries = branch.findall('location')

                if len(libraries) == 0:
                    for item in branch.findall('.//item'):
                        book.add_availablity(create_availability(item, branch_config["name"], branch_config["name"]))
                else:
                    for library in libraries:
                        if "libraries" in branch_config and library.get('name') not in branch_config["libraries"]:
                            continue

                        for item in library.findall('.//item'):
                            book.add_availablity(create_availability(item, branch.get('name'), library.get('name')))

        return book

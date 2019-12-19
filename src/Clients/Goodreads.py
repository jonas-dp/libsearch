import webbrowser
import xml.etree.ElementTree as et
import re

from src.utils.Singleton import Singleton
from rauth import OAuth1Session, OAuth1Service
from src.Book import Book
from src.Cache import Cache
from src.Configuration import Configuration


class Goodreads(Singleton, object):

    def __init__(self):
        self.tokens = Cache().load_tokens()

    def get_auth_session(self):
        if self.tokens is not None:
            return OAuth1Session(
                consumer_key=Configuration().goodreads['dev_key'],
                consumer_secret=Configuration().goodreads['dev_secret'],
                access_token=self.tokens['token'],
                access_token_secret=self.tokens['secret']
            )
        else:
            service = OAuth1Service(
                consumer_key=Configuration().goodreads['dev_key'],
                consumer_secret=Configuration().goodreads['dev_secret'],
                name='goodreads',
                request_token_url='https://www.goodreads.com/oauth/request_token',
                authorize_url='https://www.goodreads.com/oauth/authorize',
                access_token_url='https://www.goodreads.com/oauth/access_token',
                base_url='https://www.goodreads.com/'
            )

            request_token, request_token_secret = service.get_request_token(
                header_auth=True)
            auth_url = service.get_authorize_url(request_token)

            webbrowser.open_new_tab(auth_url)

            authorized = 'n'
            while authorized.lower() != 'y':
                authorized = input(
                    'Have you authorized the application? (y/n) ')

            return service.get_auth_session(request_token, request_token_secret)

    def get_user_id(self, oauth_session):
        response = oauth_session.get('https://www.goodreads.com/api/auth_user')
        return et.fromstring(response.content).find('.//user').get('id')

    def get_books(self):
        session = self.get_auth_session()

        if self.tokens is None:
            Cache().save_access_tokens(session.access_token, session.access_token_secret)

        user_id = self.get_user_id(session)

        response = session.get('https://www.goodreads.com/review/list/{}.xml'.format(user_id),
                               params={"v": "2", "shelf": "to-read", "per_page": 200})
        response_books = et.fromstring(response.content).findall('.//book')
        books = []
        for response_book in response_books:
            title = response_book.find('.//title_without_series').text
            title = re.sub('[^0-9a-zA-Z ]', ' ', title)
            book = Book(response_book.find('.//author/name').text,
                        title, response_book.find('.//id').text)
            book.goodreads_page = response_book.find('.//link').text
            book.cover_url = response_book.find('.//image_url').text
            books.append(book)

        return books

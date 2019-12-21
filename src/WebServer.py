import os

from http.server import HTTPServer, SimpleHTTPRequestHandler
from src.utils.Singleton import Singleton

class WebServer(Singleton, object):

    def run(self):
        web_dir = os.path.join(os.path.dirname(__file__), '..\\www')
        os.chdir(web_dir)

        server = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
        server.serve_forever()
        print("tetteeeen")

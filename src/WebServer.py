import os
from pathlib import Path

from http.server import HTTPServer, SimpleHTTPRequestHandler
from src.utils.Singleton import Singleton

class WebServer(Singleton, object):

    def run(self):
        web_dir = os.path.join(Path(os.path.dirname(__file__)).parent, 'www')
        os.chdir(web_dir)

        req_handler = SimpleHTTPRequestHandler
        req_handler.extensions_map['.js'] = 'application/x-javascript'

        server = HTTPServer(('localhost', 8080), req_handler)
        server.serve_forever()
        print("tetteeeen")

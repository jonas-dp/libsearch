import os
import jsonpickle

from src.utils.Singleton import Singleton
from src.Catalogue import Catalogue


class JSONOutput(Singleton, object):

    dump_file_path = os.path.join(os.path.dirname(__file__), '..\\libsearch.json')

    def dump_catalogue(self, catalogue: Catalogue):
        with open(self.dump_file_path, 'w') as catalogue_cache:
            catalogue_cache.write(jsonpickle.encode(catalogue, unpicklable=False, make_refs=False))
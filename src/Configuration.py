import json
from os import path
from src.utils.Singleton import Singleton


class Configuration(Singleton, object):

    cultuurconnect = {
        'auth_key': None,
        'branches': []
    }

    goodreads = {
        'dev_key': None,
        'dev_secret': None
    }

    def load(self):
        config_path = path.join(path.dirname(__file__), '..\\config.json')

        with open(config_path) as config_file:
            config_json = json.load(config_file)

        cc = config_json['Cultuurconnect']
        self.cultuurconnect['auth_key'] = cc['authKey']
        self.cultuurconnect['branches'] = cc['branches']

        gr = config_json['Goodreads']
        self.goodreads['dev_key'] = gr['devKey']
        self.goodreads['dev_secret'] = gr['devSecret']

        return self

    def branches_to_string(self):
        branch_strings = []

        for branch in self.cultuurconnect['branches']:
            branch_string = branch['name']
            if 'libraries' in branch:
                branch_string += ' ('
                branch_string += ', '.join(branch['libraries'])
                branch_string += ')'
            branch_strings.append(branch_string)

        return ', '.join(branch_strings)

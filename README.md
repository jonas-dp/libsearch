# ![alt text](https://github.com/depken/libsearch/raw/development/img/large.png "LibSeach")

LibSearch = Goodreads + bibliotheek.be. Get availabilities of your Goodreads to-read list from Flanders' public libraries.

## Getting Started

Download the repo and add your configuration in config.json. As an example is given in config.json.

* Branch name is the municipality you want to search (enter 'Wetteren' for 'wetteren.bibliotheek.be')
* libraries are the name of the individual libraries in the municipality (this can be empty to search all the libraries in the municipality)

### Prerequisites

Add API keys to config.json:

* [Goodreads developer key & secret](https://www.goodreads.com/api/keys)
* [CultuurConnect API key](https://www.cultuurconnect.be/api) or use test key (b8157a8a17c57162b1c9d8096c5f3620)

You'll need Python (3.6.5 minimum) and some libraries:

```
pip install rauth
pip install aiohttp
```

## Running

Run libsearch.py.
If it's the first time the program is running, it will open the authorisation page for Goodreads.
When you've accepted the authorisation, enter 'y' in the console.

Your webbrowser will open, displaying the results.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* CultuurConnect

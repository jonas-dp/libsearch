class Availability(object):

    is_available = None
    branch = None
    library = None
    status = None
    subloc = None
    zizo_image_url = None
    shelfmark = None
    publication = None
    return_date = None

    def __init__(self, is_available: bool, branch: str, library: str, status: str, subloc: str, shelfmark: str, publication: str):
        self.is_available = is_available
        self.branch = branch
        self.library = library
        self.status = status
        self.subloc = subloc
        self.shelfmark = shelfmark
        self.publication = publication
    
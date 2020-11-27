from datetime import date


class Book(object):

    frabl = None
    isbn = None
    cloudlibrary_id = None
    pages = None
    availabilities = None
    library_page = None
    goodreads_page = None
    cover_url = None
    status = None
    formats = []

    def __init__(self, author: str, title: str, goodreads_id: str):
        self.author = author
        self.author_last_name = author.split(' ')[-1]
        self.title = title
        self.goodreads_id = goodreads_id
        self.status = 'NOT_FOUND'
        self.availabilities = []

    def add_availablity(self, availability):
        self.availabilities.append(availability)

        if availability.is_available:
            self.status = 'AVAILABLE'

    def to_html(self):
        content = """<div class="card">
                <div class="row no-gutters">
                    <div class="col-md-1">"""
        content += '<img class="card-img" src="{}">'.format(
            self.cover_url)

        content += """</div>
            <div class="col-md-11">
                <div class="card-body">"""

        content += '<h5 class="card-title">{}</h5>'.format(self.title)
        content += '<h6 class="card-subtitle mb-2 text-muted">{}</h6>'.format(
            self.author)

        if self.is_available and len(self.availabilities) > 0:

            content += """<p class="card-text">
                     <table class="table">
                         <thead>
                             <tr>
                                <th scope="col">Branch</th>
                                 <th scope="col">Library</th>
                                <th scope="col">Sublocation</th>
                                 <th scope="col">Shelfmark</th>
                                 <th scope="col">Publication</th>
                             </tr>
                         </thead>
                         <tbody>"""

            availables = [
                avail for avail in self.availabilities if avail.is_available]
            for avail in availables:
                content += "<tr>"
                content += "<td><a href='{}' target='_blank'>{}</a></td>".format(
                    avail.link, avail.branch)
                content += "<td>{}</td>".format(avail.library)
                content += "<td>"
                if avail.zizo_image_url is not None:
                    content += "<img src='{}' style='width: 30px; margin-right: 5px;'/>".format(
                        avail.zizo_image_url)
                content += "{}</td>".format(avail.subloc)
                content += "<td>{}</td>".format(avail.shelfmark)
                content += "<td>{}</td>".format(avail.publication)
                content += "<tr>"

            content += """</tbody></table></p>"""

            content += '<p class="card-text"><small class="text-muted">{} - {}</small></p>'.format(
                self.isbn, self.pages)
            content += '<a href="{}" class="card-link" target="_blank">Catalogus</a>'.format(
                self.library_page)
            content += '<a href="{}" class="card-link" target="_blank">Goodreads</a>'.format(
                self.goodreads_page)

            content += """</div>
                    </div>
                </div>
            </div>"""

        elif not self.is_available and len(self.availabilities) > 0:

            content += """<p class="card-text">
                     <table class="table">
                         <thead>
                             <tr>
                                <th scope="col">Branch</th>
                                <th scope="col">Library</th>
                                <th scope="col">Status</th>
                                <th scope="col">Return Date</th>
                                <th scope="col">Days until available</th>
                             </tr>
                         </thead>
                         <tbody>"""

            unavailables = [
                avail for avail in self.availabilities if avail.is_available == False]
            for unavail in unavailables:
                content += "<tr>"
                content += "<td><a href='{}' target='_blank'>{}</a></td>".format(
                    unavail.link, unavail.branch)
                content += "<td>{}</td>".format(unavail.library)
                content += "<td>{}</td>".format(unavail.status)
                content += "<td>{}</td>".format(unavail.return_date)
                if unavail.return_date is not None:
                    content += "<td>{}</td>".format(
                        (unavail.return_date - date.today()).days)
                content += "<tr>"

            content += """</tbody></table></p>"""

            content += '<p class="card-text"><small class="text-muted">{} - {}</small></p>'.format(
                self.isbn, self.pages)
            content += '<a href="{}" class="card-link" target="_blank">Catalogus</a>'.format(
                self.library_page)
            content += '<a href="{}" class="card-link" target="_blank">Goodreads</a>'.format(
                self.goodreads_page)

            content += """</div>
                    </div>
                </div>
            </div>"""

        elif self.frabl is not None:
            content += "<p class='card-text'>No availabilities found.</p>"

            content += '<p class="card-text"><small class="text-muted">{} - {}</small></p>'.format(
                self.isbn, self.pages)
            content += '<a href="{}" class="card-link" target="_blank">Catalogus</a>'.format(
                self.library_page)
            content += '<a href="{}" class="card-link" target="_blank">Goodreads</a>'.format(
                self.goodreads_page)

            content += """</div>
                    </div>
                </div>
            </div>"""
        else:
            content += "<p class='card-text'>Not found in library catalogue.</p>"
            content += '<a href="{}" class="card-link" target="_blank">Goodreads</a>'.format(
                self.goodreads_page)

            content += """</div>
                    </div>
                </div>
            </div>"""

        return content

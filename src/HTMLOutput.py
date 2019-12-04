import webbrowser
import os

from src.utils.Singleton import Singleton
from src.Configuration import Configuration
from src.Catalogue import Catalogue
class HTMLOutput(Singleton, object):

    file_path = os.path.join(os.path.dirname(__file__), 'libsearch.html')

    def createHTML(self, catalogue: Catalogue):
        print("creating HTML output...")

        available_books = catalogue.get_available_books()
        unavailable_books = catalogue.get_unavailable_books()
        books_without_availables = catalogue.get_books_with_no_availables()
        not_found_books = catalogue.get_not_found_books()

        len_avail = len(available_books)
        len_unavail = len(unavailable_books)
        len_no_availables = len(books_without_availables)
        len_not_found = len(not_found_books)

        avail_status = 'active' if len_avail > 0 else 'disabled'
        unavail_status = '' if len_unavail > 0 else 'disabled'
        no_availables_status = '' if len_no_availables > 0 else 'disabled'
        not_found_status = '' if len_not_found > 0 else 'disabled'

        content = """<!doctype html>
            <html lang="en">

            <head>
                <!-- Required meta tags -->
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

                <!-- Bootstrap CSS -->
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
                    integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">

                <link rel="icon" href="../img/icon.ico" type="image/x-icon"/>

                <title>LibSearch</title>
            </head>

            <body>
                <nav class="navbar navbar-light bg-light sticky-top">
                    <span class="navbar-brand mb-0 h1">LibSearch</span>"""
        content += '<span class="navbar-text">{}</span>'.format(Configuration().branches_to_string())
        content += """<div class="col-12">
                        <ul class="nav nav-pills nav-fill mb-3" id="pills-tab" role="tablist">
                            <li class="nav-item">"""
        content += '<a class="nav-link {}" data-toggle="pill" href="#available">Available ({})</a>'.format(avail_status, len_avail)
        content += """
                            </li>
                            <li class="nav-item">"""
        content += '<a class="nav-link {}" data-toggle="pill" href="#unavailable">Unavailable ({})</a>'.format(unavail_status, len_unavail)
        content += """</li>
                            <li class="nav-item">"""
        content += '<a class="nav-link {}" data-toggle="pill" href="#noavailables">No Availables ({})</a>'.format(no_availables_status, len_no_availables)
        content += """</li>
                            <li class="nav-item">"""
        content += '<a class="nav-link {}" data-toggle="pill" href="#notfound">Not Found ({})</a>'.format(not_found_status, len_not_found)
        content += """</li>
                        </ul>
                    </div>
                </nav>
                <div class="container-fluid tab-content">
        <div class="tab-pane fade show active" id="available" role="tabpanel" aria-labelledby="available"> """
        for available_book in available_books:
            content += available_book.to_html()

        content += """</div>
            <div class="tab-pane fade" id="unavailable" role="tabpanel" aria-labelledby="unavailable">"""

        for unavailable_book in unavailable_books:
            content += unavailable_book.to_html()
        
        content += """</div>
            <div class="tab-pane fade" id="noavailables" role="tabpanel" aria-labelledby="noavailables">"""

        for book_without_availables in books_without_availables:
            content += book_without_availables.to_html()
            
        content += """</div>
            <div class="tab-pane fade" id="notfound" role="tabpanel" aria-labelledby="notfound">"""

        for not_found_book in not_found_books:
            content += not_found_book.to_html()

        content += "</div>"
        content += """
                </div>
                </div>
                <!-- Optional JavaScript -->
                <!-- jQuery first, then Popper.js, then Bootstrap JS -->
                <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
                <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
                <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
            </body>
            </html>"""

        with open(self.file_path, "w") as f:
            f.write(content)
            f.close()

    def openHTML(self):
        webbrowser.open(self.file_path)

    def branches_to_string(self, branches: dict):
        branch_strings = []

        for branch in branches:
            branch_string = branch["name"]
            if "libraries" in branch:
                branch_string += " ("
                branch_string += ", ".join(branch["libraries"])
                branch_string += ")"
            branch_strings.append(branch_string)

        return ", ".join(branch_strings)
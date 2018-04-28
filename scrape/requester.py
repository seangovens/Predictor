import requests


class Requester:
    def __init__(self, url):
        self.url = url

    def get_page_content(self):
        page = requests.get(self.url)
        return page.content if page.status_code == 200 else None

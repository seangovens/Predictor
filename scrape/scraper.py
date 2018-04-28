from bs4 import BeautifulSoup
from scrape.requester import Requester


class Scraper:
    def __init__(self, base_url):
        self.base_url = base_url
        return

    def get_contents(self, sub_url):
        r = Requester(self.base_url + sub_url)
        contents = r.get_page_content()
        if contents is not None:
            soup = BeautifulSoup(r.get_page_content(), "html.parser")
        else:
            soup = None
        return soup

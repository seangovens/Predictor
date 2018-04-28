from scrape.scraper import Scraper
from scrape.entities.movie import Movie
from scrape.entities.person import Person


class RTScraper(Scraper):
    def __init__(self):
        super().__init__("https://www.rottentomatoes.com/")

    def get_movie(self, movie):
        title = movie.lower().replace(" ", "_")
        page = self.get_contents("m/" + title)
        return Movie(page) if page is not None else None

    def get_person(self, person, job):
        title = person.lower().replace(" ", "_")
        page = self.get_contents("celebrity/" + title)
        return Person(person, page, job) if page is not None else None

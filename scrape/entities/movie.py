from enum import Enum
from scrape.entities.person import Person
from scrape.entities.person import People
import re


class Genre(Enum):
    ACTION_ADVENTURE = 0        # Action & Adventure
    DRAMA = 1                   # Drama
    SCIFI_FANTASY = 2           # Science Fiction & Fantasy
    ANIMATION = 3               # Animation
    COMEDY = 4                  # Comedy
    KIDS_FAMILY = 5             # Kids & Family
    ART_INTERNATIONAL = 6       # Art House & International
    MYSTERY_SUSPENSE = 7        # Mystery & Suspense
    ROMANCE = 8                 # Romance
    DOCUMENTARY = 9             # Documentary
    HORROR = 10                 # Horror


class Rating(Enum):
    G = 0
    PG = 1
    PG13 = 2
    R = 3
    NC17 = 4
    NR = 5


class Movie:
    GENRE_TITLES = ["Action & Adventure", "Drama", "Science Fiction & Fantasy",
                    "Animation", "Comedy", "Kids & Family",
                    "Art House & International", "Mystery & Suspense",
                    "Romance", "Documentary", "Horror"]
    RATING_PATTERNS = [re.compile("^G.*"), re.compile("^PG(?!.?13).*"),
                       re.compile("^PG-?13.*"), re.compile("^R.*"),
                       re.compile("^NC17.*"), re.compile("^NR.*")]

    def __init__(self, page):
        self.page = page

    def extract_meta_people_links(self, heading):
        ret = []
        for sib in heading.next_siblings:
            if sib.name == "div":
                for child in sib.children:
                    if child.name == "a":
                        ret.append(child["href"].split("/")[-1])
        return ret

    def get_meta_people(self, key):
        names = []
        headings = self.page.find_all("div", class_="meta-label subtle")
        for h in headings:
            if key in h.get_text():
                names.extend(self.extract_meta_people_links(h))
        return names

    def get_directors(self):
        return self.get_meta_people("Directed By:")

    def get_writers(self):
        return self.get_meta_people("Written By:")

    def get_actors(self):
        cast_section = self.page.find("div", class_="castSection")
        ret = []
        if cast_section is not None:
            act_text = cast_section.find_all("div", class_="media-body")
            for t in act_text:
                a = t.find("a", href=re.compile("/celebrity/.*"))
                ret.append(a["href"].split("/")[-1])
        return ret

    def get_genres(self):
        genres = self.page.find_all("a", href=re.compile("/browse/opening/\?genres.*"))
        ret = []
        for g in genres:
            text = g.get_text().strip()
            if text in Movie.GENRE_TITLES:
                ret.append(Genre(Movie.GENRE_TITLES.index(text)))
        return ret

    def genre_vector(self):
        g = self.get_genres()
        g_int = [x.value for x in g]
        res = [0]*len(Genre)
        for i in range(0, len(res)):
            res[i] = 1 if i in g_int else 0
        return res

    def match_rating(self, text):
        for i in range(len(Movie.RATING_PATTERNS)):
            if Movie.RATING_PATTERNS[i].match(text) is not None:
                return Rating(i)
        return None

    def get_rating(self):
        rate_head = self.page.find_all("div", class_="meta-label subtle")
        for rate in rate_head:
            if "Rating:" in rate.get_text():
                for sib in rate.next_siblings:
                    if sib.name == "div":
                        return self.match_rating(sib.get_text())
        return None

    def get_score(self):
        score_box = self.page.find("span", class_="meter-value superPageFontColor")
        try:
            score = int(score_box.get_text().replace("%", ""))
            return score
        except ValueError:
            return -1

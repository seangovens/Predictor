from enum import Enum
import re


class People(Enum):
    DIRECTOR = 0
    WRITER = 1
    ACTOR = 2
    PRODUCER = 3


class Person:
    JOB_TITLES = ["Director", "Screenwriter", "Actor", "Producer"]

    def __init__(self, name: str, page, job: People):
        self.name = name
        self.page = page
        self.job = job

    def has_job(self, film_entry):
        creds = film_entry.find_all("em", class_="subtle")
        if creds is not None:
            for c in creds:
                if Person.JOB_TITLES[self.job.value] in c.get_text():
                    return True
        return False

    @staticmethod
    def score_exists(score):
        return score.find("span", class_="tMeterIcon small noRating") is None

    def get_scores(self, job_specific=False):
        scores = []
        try:
            filmography = self.page.find("table", id="filmographyTbl")
            all_scores = filmography.find_all("td", attrs={"data-rating":
                                                    re.compile(r"\d+")})
            for s in all_scores:
                if job_specific:
                    if (self.job == People.ACTOR or self.has_job(s.parent)) \
                            and Person.score_exists(s):
                        scores.append(int(s["data-rating"]))
                elif Person.score_exists(s):
                    scores.append(int(s["data-rating"]))
        except TypeError:
            print("Failed to get scores")
            pass
        return scores

    # DEPRECATED
    #def get_average_score(self):
    #    try:
    #        filmography = self.page.find("table", id="filmographyTbl")
    #        all_scores = filmography.find_all("span", class_="tMeterScore")
    #        total = 0.0
    #        count = 0
    #        for s in all_scores:
    #            text = s.get_text().replace("%", "")
    #            if text.isdigit():
    #                total += int(text)
    #                count += 1
    #        score = total / count if count > 0 else 0
    #    except TypeError:
    #        score = -1
    #    return score

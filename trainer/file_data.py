from trainer.datapoint import DataPoint
from scrape.entities.person import People
import math
import pickle


class FileData:
    @staticmethod
    def weight_quad(items, exp):
        if len(items) < 1:
            return 0
        res = 0.0
        t_w = 0.0
        for i in range(len(items)):
            w = -(i / len(items)) ** exp + 1
            res += w * items[i]
            t_w += w
        return res / t_w

    @staticmethod
    def weight_linear(items):
        if len(items) < 1:
            return 0
        res = 0.0
        for i in range(len(items)):
            res += (len(items) - i) * items[i]
        return res / (len(items) * (len(items) + 1) / 2)

    @staticmethod
    def weight_mean(items):
        if len(items) < 1:
            return 0
        return sum(items) / len(items)

    @staticmethod
    def get_cached(name, job):
        f_name = "directors" if job == People.DIRECTOR else\
            "writers" if job == People.WRITER else "actors"
        with open(f_name, "rb") as in_file:
            dic = pickle.load(in_file)
            if name in dic:
                return dic[name]
        return None

    @staticmethod
    def set_cached(name, job, scores):
        f_name = "directors" if job == People.DIRECTOR else \
            "writers" if job == People.WRITER else "actors"
        dic = {}
        with open(f_name, "rb") as in_file:
            dic = pickle.load(in_file)
        dic[name] = scores
        with open(f_name, "wb") as out_file:
            pickle.dump(dic, out_file)

    @staticmethod
    def lookup(s, names, job):
        people_scores = []
        for name in names:
            try:
                scores = FileData.get_cached(name, job)
                if scores is None:
                    p = s.get_person(name, job)
                    scores = p.get_scores(job_specific=True)
                    FileData.set_cached(name, job, scores)

                if len(scores) > 0:
                    people_scores.append(FileData.weight_linear(scores))
            except AttributeError:
                pass
        return [FileData.weight_mean(people_scores),
                FileData.weight_linear(people_scores),
                FileData.weight_quad(people_scores, 2)]

    @staticmethod
    def mov_to_data(s, title, m):
        ent = [title.strip("\n")] \
              + [FileData.lookup(s, m.get_directors(), People.DIRECTOR)[2]] \
              + [FileData.lookup(s, m.get_writers(), People.WRITER)[2]] \
              + [FileData.lookup(s, m.get_actors(), People.ACTOR)[2]] \
              + [m.get_rating().value] \
              + m.genre_vector() + [0]
        return DataPoint(*ent)

    @staticmethod
    def file_to_data(f_name, max_lines=math.inf):
        data = []
        with open(f_name, "r") as file:
            file.readline()
            num = 0
            for line in file.readlines():
                fields = line.split(",")
                fields = [fields[0], fields[3], fields[6]]+fields[9:]
                for i in range(1, 4):
                    fields[i] = float(fields[i])
                fields[4] = float(fields[4])
                for i in range(5, 16):
                    fields[i] = float(fields[i])
                fields[16] = float(fields[16])
                dp = DataPoint(*fields)
                data.append(dp)
                num += 1
                if num >= max_lines:
                    break
        return data

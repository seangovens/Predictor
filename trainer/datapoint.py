class DataPoint(object):
    def __init__(self, _title, _director_score, _writer_score, _actor_score,
                 _rating, _act_adv, _drama, _sci_fant, _anim, _comedy, _kids,
                 _artsy, _mystery, _romance, _doc, _horror, _score):
        self.title = _title
        self.director_score = _director_score / 100.0
        self.writer_score = _writer_score / 100.0
        self.actor_score = _actor_score / 100.0
        self.rating = _rating / 5.0
        self.act_adv = _act_adv
        self.drama = _drama
        self.sci_fant = _sci_fant
        self.anim = _anim
        self.comedy = _comedy
        self.kids = _kids
        self.artsy = _artsy
        self.mystery = _mystery
        self.romance = _romance
        self.doc = _doc
        self.horror = _horror
        self.score = _score

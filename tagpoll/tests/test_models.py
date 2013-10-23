# -*- coding: utf-8 -*-
from .. import models
from . import BaseTest
import transaction


class TestModels(BaseTest):
    def test_add_question(self):
        assert models.Question.query.count() == 0
        tags = set(["ponies", "thunderstorms", "giant robots", "archeological digs", "trombones"])
        q = models.Question(text="Which are cool?", min=3, max=3, active=True, tags=tags)
        models.DBSession.add(q)
        transaction.commit()
        assert models.Question.query.filter_by(active=True).count() == 1
        q = models.Question.query.filter_by(active=True).one()
        assert tags == q.tags

    def test_add_vote(self):
        self.test_add_question()
        assert models.Vote.query.count() == 0
        q = models.Question.query.filter_by(active=True).one()
        vote_tags = set(["thunderstorms", "archeological digs", "trombones"])
        q.add_vote(vote_tags)
        transaction.commit()
        vote = models.Vote.query.one()
        assert vote.uuid is not None
        assert vote.tags == vote_tags

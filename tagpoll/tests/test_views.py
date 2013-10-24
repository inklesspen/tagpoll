# -*- coding: utf-8 -*-
from pyramid import testing
from pyramid.httpexceptions import HTTPSeeOther, HTTPBadRequest

from .. import models, views
from . import BaseTest
import transaction
from webob.multidict import MultiDict
from ..util import make_uuid


class TestViews(BaseTest):
    def test_show_poll(self):
        tags = set(["ponies", "thunderstorms", "giant robots", "archeological digs", "trombones"])
        q = models.Question(text="Which are cool?", min=3, max=3, active=True, tags=tags)
        models.DBSession.add(q)
        transaction.commit()
        request = testing.DummyRequest(method='GET')
        response = views.show_poll(request)
        q = models.Question.query.one()
        expected = {}
        for f in ['text', 'tags', 'max', 'min']:
            expected[f] = getattr(q, f)
        assert response == expected

    def test_vote(self):
        views.includeme(self.config)
        tags = set(["ponies", "thunderstorms", "giant robots", "archeological digs", "trombones"])
        q = models.Question(text="Which are cool?", min=3, max=3, active=True, tags=tags)
        models.DBSession.add(q)
        transaction.commit()

        q = models.Question.query.one()
        assert models.Vote.query.filter(models.Vote.question == q).count() == 0

        data = MultiDict()
        data.add('tag', 'thunderstorms')
        data.add('tag', 'giant robots')
        data.add('tag', 'trombones')

        request = testing.DummyRequest(post=data)
        response = views.record_vote(request)

        assert isinstance(response, HTTPSeeOther)
        v = models.Vote.query.filter(models.Vote.question == q).one()
        assert v.tags == set(data.getall('tag'))

        assert v.uuid == request.session['uuid']

    def test_vote_skip(self):
        views.includeme(self.config)
        tags = set(["ponies", "thunderstorms", "giant robots", "archeological digs", "trombones"])
        q = models.Question(text="Which are cool?", min=3, max=3, active=True, tags=tags)
        models.DBSession.add(q)
        transaction.commit()

        request = testing.DummyRequest(post=MultiDict(skipped='skipped'))
        response = views.record_vote(request)

        assert isinstance(response, HTTPSeeOther)
        assert request.session['skipped']

    def test_vote_skipped(self):
        data = MultiDict()
        data.add('tag', 'thunderstorms')
        data.add('tag', 'giant robots')
        data.add('tag', 'trombones')

        request = testing.DummyRequest(post=data)
        request.session['skipped'] = True
        response = views.record_vote(request)

        assert isinstance(response, HTTPBadRequest)

    def test_vote_already_voted(self):
        data = MultiDict()
        data.add('tag', 'thunderstorms')
        data.add('tag', 'giant robots')
        data.add('tag', 'trombones')

        request = testing.DummyRequest(post=data)
        request.session['uuid'] = make_uuid()
        response = views.record_vote(request)

        assert isinstance(response, HTTPBadRequest)

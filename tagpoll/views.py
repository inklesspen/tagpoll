from pyramid.httpexceptions import HTTPSeeOther, HTTPBadRequest

from .models import (
    DBSession,
    Question,
)


def show_poll(request):
    q = Question.query.filter_by(active=True).one()
    return {
        'text': q.text,
        'tags': q.tags,
        'max': q.max,
        'min': q.min
    }


def already_voted(request):
    return request.session.get('uuid') is not None or request.session.get('skipped') is True


def record_vote(request):
    if already_voted(request):
        return HTTPBadRequest()
    if 'skipped' in request.POST:
        request.session['skipped'] = True
    else:
        q = Question.query.filter_by(active=True).one()
        vote = q.add_vote(request.POST.getall('tag'))
        DBSession.flush()
        request.session['uuid'] = vote.uuid
    return HTTPSeeOther(request.route_path('main'))


def show_results(request):
    q = Question.query.filter_by(active=True).one()
    data = q.calculate_results()
    data['question'] = q
    return data


class VotedPredicate(object):
    def __init__(self, val, config):
        self.val = val

    def text(self):
        return 'voted = {}'.format(self.val)

    phash = text

    def __call__(self, context, request):
        return already_voted(request) == self.val


def includeme(config):
    config.add_view_predicate('voted', VotedPredicate)
    config.add_route('main', '/')
    config.add_view(show_poll, route_name='main', renderer='tagpoll:templates/show_poll.mako', voted=False)
    config.add_view(show_results, route_name='main', renderer='tagpoll:templates/show_results.mako', voted=True)
    config.add_route('vote', '/vote')
    config.add_view(record_vote, route_name='vote')

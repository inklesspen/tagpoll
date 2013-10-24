from sqlalchemy import (
    Column,
    ForeignKey,
    UniqueConstraint,
    Integer,
    Unicode,
    Boolean,
    PickleType,
)

from sqlalchemy.inspection import inspect
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base, declared_attr

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship
)

from zope.sqlalchemy import ZopeTransactionExtension
from .util import convert_camel_case, GUID, make_uuid

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))


class Base(object):
    id = Column(Integer, primary_key=True)
    query = DBSession.query_property()

    @declared_attr
    def __tablename__(cls):
        return convert_camel_case("{}s".format(cls.__name__))

    def __json__(self, request=None):
        # The built-in json renderer passes in the request in case the __json__ needs it.
        # We don't. So we'll just optionally take it, and ignore it.
        mapper = inspect(type(self))
        d = {}
        for attrname in mapper.column_attrs.keys():
            d[attrname] = getattr(self, attrname)
            # TODO: other proeprty types (foreign keys, relationships, etc.)
            # just proving the functionality on simple fields first
        return d

    def __repr__(self):
        cls = type(self)
        mapper = inspect(cls)
        fills = []
        formats = []
        formats.append("<{}")
        for attrname in mapper.column_attrs.keys():
            formats.append(' {}={!r}')
            fills.append(attrname)
            fills.append(getattr(self, attrname))
        formats.append(">")
        return "".join(formats).format(cls.__name__, *fills)

Base = declarative_base(cls=Base)


class Question(Base):
    text = Column(Unicode(length=300), nullable=False)
    active = Column(Boolean, nullable=False, default=False)
    min = Column(Integer, nullable=False)
    max = Column(Integer, nullable=False)
    tags = Column(PickleType, nullable=False)
    votes = relationship('Vote', backref='question')

    def add_vote(self, vote_tags):
        vote_tags = set(vote_tags)
        if len(vote_tags) < self.min:
            raise ValueError("Needed at least {} tags, got {}".format(self.min, len(vote_tags)))
        if len(vote_tags) > self.max:
            raise ValueError("Needed at most {} tags, got {}".format(self.max, len(vote_tags)))
        for tag in vote_tags:
            if tag not in self.tags:
                raise ValueError("'{}' not in my tags.".format(tag))
        return Vote(question=self, tags=vote_tags)


class Vote(Base):
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    uuid = Column(GUID, nullable=False, unique=True, default=make_uuid)
    tags = Column(PickleType, nullable=False)

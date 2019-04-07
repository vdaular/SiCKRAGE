from sqlalchemy import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    tv_shows = Table('tv_shows', meta, autoload=True)
    last_backlog_search = Column('last_backlog_search', Integer, default=0)
    last_backlog_search.create(tv_shows)


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    tv_shows = Table('tv_shows', meta, autoload=True)
    tv_shows.c.last_backlog_search.drop()

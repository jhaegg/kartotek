import sqlite3
from yoyo import read_migrations, get_backend

from mtgapi.config import config

def _load_database():
    backend = get_backend("sqlite:///%s" % config['db_file'])
    migrations = read_migrations("migrations/")
    backend.apply_migrations(backend.to_apply(migrations))

    con = sqlite3.connect(config['db_file'])
    con.row_factory = sqlite3.Row
    return con


class Database:
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state
        if not hasattr(self, '_db'):
            self._db = _load_database()

    def set_have_cards(self, cards):
        with self._db as cursor:
            cursor.executemany(
                """INSERT OR REPLACE INTO have
                   ('gatherer_id', 'num_regular', 'num_foil')
                   VALUES (:gatherer_id, :num_regular, :num_foil);""", cards)

    def get_have_cards(self):
        cursor = self._db.cursor()
        cursor.execute("SELECT * FROM have WHERE 1;")
        yield from cursor

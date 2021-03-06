import sqlite3
from yoyo import read_migrations, get_backend

from kartotek.config import config

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

    def set_have_cards(self, user_id, cards):
        with self._db as cursor:
            # Note that user_id is not escaped, safe since integer only
            cursor.executemany(
                """INSERT OR REPLACE INTO have
                   ('user_id', 'mvid', 'num_regular', 'num_foil')
                   VALUES (%d, :mvid, :num_regular, :num_foil);""" % user_id, cards)

    def get_have_cards(self, user_id):
        cursor = self._db.cursor()
        cursor.execute("""
            SELECT card.mvid        AS mvid,
                   card.name        AS name,
                   card.rarity      AS ratity,
                   have.num_regular AS num_regular,
                   have.num_foil    AS num_foil
            FROM have
            INNER JOIN cards AS card
                ON have.mvid = card.mvid
            WHERE have.user_id = ?;""", user_id)

        yield from cursor

    def set_set(self, set):
        cursor = self._db.cursor()
        cursor.execute(
            """INSERT OR REPLACE INTO sets
               ('code', 'name')
               VALUES (:code, :name);""", set)
        self._db.commit()
        return cursor.lastrowid

    def set_cards(self, cards):
        with self._db as cursor:
            cursor.executemany(
                """INSERT OR REPLACE INTO cards
                   ('mvid', 'set_id', 'name', 'printed', 'oracle', 'cost', 'cmc', 'rarity')
                   VALUES (:mvid, :set_id, :name, :printed, :oracle, :cost, :cmc, :rarity);""", cards)

    def add_user(self, username, salt, password):
        cursor = self._db.cursor()
        cursor.execute(
            """INSERT INTO users ('username', 'password_salt', 'password_hash')
               VALUES (?, ?, ?);""", (username, salt, password))
        self._db.commit()
        return cursor.lastrowid

    def get_credentials(self, username):
        cursor = self._db.execute(
            "SELECT user_id, password_salt, password_hash FROM users WHERE username = ?;", (username, ))
        return cursor.fetchone()

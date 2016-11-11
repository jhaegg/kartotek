import json
from falcon import API

from mtgapi.db import Database


_db = Database()


class HaveResource:
    def on_get(self, req, resp):
        resp.body = json.dumps(list(map(dict, _db.get_have_cards())))


app = API()
app.add_route('/have', HaveResource())

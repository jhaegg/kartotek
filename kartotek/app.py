import json
from csv import DictReader
from io import TextIOWrapper

import falcon

from kartotek.db import Database
from kartotek.auth import new_password, auth, AuthMiddleware
from kartotek.util import Translator

_db = Database()


class HaveResource:
    def on_get(self, req, resp, user_id):
        resp.body = json.dumps(list(map(dict, _db.get_have_cards(user_id))))

    @auth
    def on_post(self, req, resp, user_id):
        if req.user_id != int(user_id):
            raise falcon.HTTPForbidden()

        if req.content_type != "text/csv":
            raise falcon.HTTPBadRequest("Expected Content-Type 'text/csv', not '%s'" % req.content_type)

        translator = Translator({k: req.get_param(k, default=k)
                                 for k in ['mvid', 'num_regular', 'num_foil']})

        wrapped = translator(DictReader(TextIOWrapper(req.bounded_stream, encoding="utf-8")))
        _db.set_have_cards(req.user_id, wrapped)


class UsersResource:
    def on_post(self, req, resp):
        user_id = _db.add_user(req.params['username'], *new_password(req.params['password']))
        resp.body = json.dumps({'user_id': user_id})


app = falcon.API(middleware=[AuthMiddleware()])
app.add_route('/have/{user_id}', HaveResource())
app.req_options.auto_parse_form_urlencoded = True
app.add_route('/user', UsersResource())

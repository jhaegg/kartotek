import json
from falcon import API

from kartotek.db import Database
from kartotek.auth import new_password, auth, AuthMiddleware

_db = Database()


class HaveResource:
    def on_get(self, req, resp, user_id):
        resp.body = json.dumps(list(map(dict, _db.get_have_cards(user_id))))

class UsersResource:
    def on_post(self, req, resp):
        user_id = _db.add_user(req.params['username'], *new_password(req.params['password']))
        resp.body = json.dumps({'user_id': user_id})


app = API(middleware=[AuthMiddleware()])
app.add_route('/have/{user_id}', HaveResource())
app.add_route('/user', UsersResource())

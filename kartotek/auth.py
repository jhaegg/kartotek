import falcon
import scrypt

from base64 import b64decode
from os import urandom

from kartotek.config import config
from kartotek.db import Database


_db = Database()


def new_password(password):
    salt = urandom(256)
    full_salt = salt + config['password_secret'].encode('utf-8')
    return (salt, scrypt.hash(password, full_salt))


def verify_password(password, salt, password_hash):
    return password_hash == scrypt.hash(password, salt + config['password_secret'].encode('utf-8'))


def auth(fn):
    setattr(fn, '__auth', True)
    return fn


class AuthMiddleware:
    def process_resource(self, req, resp, resource, params):
        if hasattr(getattr(resource, "on_%s" % req.method.lower()), '__auth') == False:
            return

        if req.auth is None:
            raise falcon.HTTPUnauthorized()

        auth_type, user_password = req.auth.split(" ")
        if auth_type.lower() != "basic":
            raise falcon.HTTPBadRequest()

        username, password = b64decode(user_password).decode('utf-8').split(":")
        credentials = _db.get_credentials(username)
        if credentials is None:
            raise falcon.HTTPUnauthorized()

        if not verify_password(password, credentials['password_salt'], credentials['password_hash']):
            raise falcon.HTTPUnauthorized()

        req.user_id = credentials['user_id']

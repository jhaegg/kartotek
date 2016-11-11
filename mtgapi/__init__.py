from mtgapi.app import app
from wsgiref.simple_server import make_server
from logging import getLogger
from argparse import ArgumentParser
from csv import DictReader

from mtgapi.util import Translator
from mtgapi.db import Database
from mtgapi.config import config

def api():
    logger = getLogger('api')
    try:
        make_server(config['api_bind'], config['api_port'], app).serve_forever()
    except KeyboardInterrupt:
        return 0
    except Exception:
        logger.exception("Uncaught Exception")
        return 1

def csv():
    logger = getLogger('csv')
    parser = ArgumentParser(description="Load CSV into DB")
    parser.add_argument('--translation',
                        dest='translation',
                        type=str,
                        help="Field mapping",
                        required=True)
    parser.add_argument('file',
                        type=str,
                        nargs=1,
                        help="CSV to load")

    args = parser.parse_args()

    translator = Translator(args.translation)

    with open(args.file[0], 'r') as csv_file:
        Database().set_have_cards(translator(DictReader(csv_file)))

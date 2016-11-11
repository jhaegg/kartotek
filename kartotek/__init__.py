
from wsgiref.simple_server import make_server
from logging import getLogger
from argparse import ArgumentParser
from csv import DictReader

from kartotek.app import app
from kartotek.util import Translator
from kartotek.util import MTGJSONReader
from kartotek.db import Database
from kartotek.config import config

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

def cards():
    logger = getLogger('cards')
    parser = ArgumentParser(description="Load card definition JSON into DB")
    parser.add_argument('file',
                        type=str,
                        nargs=1,
                        help="JSON to load")
    args = parser.parse_args()
    reader = MTGJSONReader(args.file[0])
    set_id = Database().set_set(reader.set())
    Database().set_cards(reader.cards(set_id))

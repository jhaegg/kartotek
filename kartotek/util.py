from json import load


class Translator:
    def __init__(self, translation):
        with open(translation, 'r') as json_file:
            self._translation = load(json_file)

    def __call__(self, source):
        for item in source:
            yield {
                field: item[self._translation[field]]
                for field in ['mvid', 'num_regular', 'num_foil']
            }


class MTGJSONReader:
    def __init__(self, set_file):
        with open(set_file, 'r') as json_file:
            self._set = load(json_file)

    def set(self):
        return {
            'name': self._set['name'],
            'code': self._set['code']
        }

    def cards(self, set_id):
        for card in self._set['cards']:
            yield {
                'mvid': card['multiverseid'],
                'set_id': set_id,
                'name': card['name'],
                'printed': card.get('originalText', ""),
                'oracle': card.get('text', ""),
                'cost': card.get('manaCost', ""),
                'cmc': card.get('cmc', 0),
                'rarity': card['rarity']
            }

from json import load

class Translator:
    def __init__(self, translation):
        with open(translation, 'r') as json_file:
            self._translation = load(json_file)

    def __call__(self, source):
        for item in source:
            yield {
                field: item[self._translation[field]]
                for field in ['gatherer_id', 'num_regular', 'num_foil']
            }

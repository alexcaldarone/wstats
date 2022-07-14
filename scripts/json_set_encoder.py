import json

class SetEncoder(json.JSONEncoder):
    '''
    Class used to encode sets for the creation of the json file
    '''
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)
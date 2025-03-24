from django.test import TestCase

# Create your tests here.
import json
import os
from django.conf import settings


def jsonToDict(json_str=None, file_path=None):
    if json_str:
        dict1 = json.loads(json_str)
        return dict1
    if file_path:
        with open(file_path, 'r') as f:
            dict1 = json.load(f)
        return dict1




jsonFile = '{"id": 1, "name": "Gbenga", "email": "opesam42@gmail.com"}'
# conver to python dict

file_path = os.path.join(settings.BASE_DIR, 'listing', 'data', 'states_and_lgas.json')

# print(data)

STATES_AND_LGAS = jsonToDict(file_path=file_path)

STATE_CHOICES = tuple( (slugify(state), state) for state in STATES_AND_LGAS.keys())
print(STATE_CHOICES)
print(type(STATE_CHOICES))
# print( tuple(dict1.keys()) )
# print(dict1["Lagos"])


 
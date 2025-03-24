import json
import os
from django.conf import settings


jsonFile = '{"id": 1, "name": "Gbenga", "email": "opesam42@gmail.com"}'
# conver to python dict

file_path = os.path.join(settings.BASE_DIR, 'listing', 'data', 'states_and_lgas.json')
with open(file_path, 'r') as f:
    data =json.load(f)

def jsonToDict(json_str):
    dict1 = json.loads(json_str)
    
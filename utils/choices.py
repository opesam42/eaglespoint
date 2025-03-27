from django.conf import settings
import os
from .helper_functions import *

file_path = os.path.join(settings.BASE_DIR, 'data', 'states_and_lgas.json')

STATES_AND_LGAS = json_to_dict(file_path=file_path)

LISTING_TYPE = (
    ('buy', 'Buy'),
    ('rent', 'Rent'),
    ('land', 'Land'),
)
STATE_CHOICES = tuple( (state, state) for state in STATES_AND_LGAS.keys())
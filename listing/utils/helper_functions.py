import json
import re

def slugify(text):
    return re.sub(r'\s+', '-', text.strip().lower())

def json_to_dict(json_str=None, file_path=None):
    """ to convert json file to python dictionary """
    if json_str:
        return json.loads(json_str)
    
    if file_path:
        try:
            with open(file_path, 'r', encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{file_path}' not found.")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in file.")
    
    raise ValueError("Either 'json_str' or 'file_path' must be provided.")

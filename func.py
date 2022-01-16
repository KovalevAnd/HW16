import json


def read_json(file):
    with open(file, encoding='utf-8') as f:
        return json.load(f)

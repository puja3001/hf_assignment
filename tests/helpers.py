import json
import os


def get_fixture_filepath(filename):
    base_dir = os.path.dirname(__file__)
    return os.path.join(base_dir, 'fixtures', filename)


def load_fixtures(filename):
    filepath = get_fixture_filepath(filename)
    file = open(filepath)
    data = json.load(file)
    return data
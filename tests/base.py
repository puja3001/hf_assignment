from dal.models import insert_values, create_tables, drop_tables
from tests import helpers


def setup_db():
    create_tables()
    filepath = helpers.get_fixture_filepath('data.json')
    insert_values(filepath)


def clean_db():
    drop_tables()
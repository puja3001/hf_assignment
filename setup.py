import os

from dal.models import insert_values, create_tables, drop_tables

base_dir = os.path.dirname(__file__)
filepath = os.path.join(base_dir, 'fixtures', 'data.json')

if __name__ == '__main__':
    drop_tables()
    create_tables()
    insert_values(filepath)

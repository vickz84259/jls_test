import csv
import sqlite3
from typing import cast, Union, MutableMapping

from flask import current_app, g

Row = MutableMapping[str, Union[str, int, None]]


def get_db() -> sqlite3.Connection:
    if 'db' not in g:
        g.db = sqlite3.connect(
            'jls.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row

    return cast(sqlite3.Connection, g.db)


def close_db() -> None:
    db = g.pop('db', None)

    if db is not None:
        db.close()


def convert_boolean(key: str, row: Row) -> None:
    value = row[key]
    if value == 'Yes':
        row[key] = int(True)
    elif value == 'No':
        row[key] = int(False)
    else:
        row[key] = None


def prepare_products_data(products_data: csv.DictReader) -> list[Row]:  # fix
    results: list[Row] = []  # fix

    for row in products_data:
        for key in ['Restockable', 'Hazmat', 'Active']:
            convert_boolean(key, row)

        results.append(tuple(row.values()))
    return results


def init_db() -> None:
    db = get_db()
    cursor = db.cursor()

    with current_app.open_resource('schema.sql') as schema_file:
        cursor.executescript(schema_file.read().decode('utf8'))
        db.commit()

    with open('core_products.csv', newline='\r\n') as products_file:
        products_data = csv.DictReader(products_file)
        cursor.executemany(
            f'INSERT INTO products VALUES ({"?," * 26} ?)',
            prepare_products_data(products_data))
        db.commit()

    assert(cursor.rowcount == 2724)

    with open('locations.csv') as locations_file:
        locations_data = csv.DictReader(locations_file)
        cursor.executemany(
            'INSERT INTO locations VALUES(?, ?, ?, ?)',
            (tuple(row.values()) for row in locations_data))
        db.commit()

    assert(cursor.rowcount == 1201)

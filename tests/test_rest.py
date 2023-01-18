import psycopg2
import pytest

from fastapi.testclient import TestClient
from utils.db import db_pool
from main import app


def setup():
    print('SETUP!')
    from os import environ
    print('!!!', environ.get('POSTGRES_USER'), environ.get('POSTGRES_PASSWORD'), environ.get('DB_SERVICE_NAME'), environ.get('DB_PORT'), environ.get('POSTGRES_DATABASE'), '!!!')
    connection = None
    try:
        with db_pool.getconn() as connection:
            connection: psycopg2.connection
            with connection.cursor() as cursor:
                cursor: psycopg2.cursor
                cursor.execute(
                    """CREATE TABLE ciplay_stats (
                        stat_id SERIAL PRIMARY KEY,
                        date DATE NOT NULL UNIQUE ,
                        views BIGINT,
                        clicks BIGINT,
                        cost DECIMAL(12,2)
                    );""")
    finally:
        if connection:
            connection.close()
            db_pool.putconn(connection)


def teardown():
    print('TEARDOWN!')
    connection = None
    try:
        with db_pool.getconn() as connection:
            connection: psycopg2.connection
            with connection.cursor() as cursor:
                cursor: psycopg2.cursor
                cursor.execute(
                    """DROP TABLE ciplay_stats""")
    finally:
        if connection:
            connection.close()
            db_pool.putconn(connection)
    if db_pool:
        db_pool.closeall()


@pytest.fixture(scope="module")
def test_app():
    yield TestClient(app)


def test_one_entry(test_app):
    response = test_app.get('/stats?from=2022-01-17&to=2023-01-17')
    assert response.json() == []
    response = test_app.post('/stats', json={
        "date": "2022-05-23",
        "views": 10,
        "clicks": 5,
        "cost": 1.0
    })
    assert response.json().get('message') == "Stats saved"
    response = test_app.get('/stats?from=2022-01-17&to=2023-01-17')
    response.json() == [{
        "date": "2022-05-23",
        "views": 10,
        "clicks": 5,
        "cost": 1.0
    }]

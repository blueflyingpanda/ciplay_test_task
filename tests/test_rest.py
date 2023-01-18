import psycopg2
import pytest

from fastapi.testclient import TestClient
from utils.db import db_pool
from main import app


def setup():
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


@pytest.fixture()
def test_app():
    client = TestClient(app)
    yield client
    client.delete('/stats')


def test_one_entry(test_app):
    response = test_app.get('/stats?from=2022-01-17&to=2023-01-17')
    assert response.json() == []
    response = test_app.post('/stats', json={
        "date": "2022-05-23",
        "views": 10,
        "clicks": 5,
        "cost": 10.0
    })
    assert response.json().get('message') == "Stats saved"
    response = test_app.get('/stats?from=2022-01-17&to=2023-01-17')
    assert response.json() == [{
        "date": "2022-05-23",
        "views": 10,
        "clicks": 5,
        "cost": 10.0,
        "cpc": 2.0,
        "cpm": 1000.0
    }]


def test_one_entry_duplication(test_app):
    response = test_app.post('/stats', json={
        "date": "2022-05-23",
        "views": 10,
        "clicks": 5,
        "cost": 10.0
    })
    assert response.json().get('message') == "Stats saved"
    response = test_app.post('/stats', json={
        "date": "2022-05-23",
        "views": 20,
        "clicks": 10,
        "cost": 20.0
    })
    assert response.json().get('message') == "Stats saved"
    response = test_app.get('/stats?from=2022-01-17&to=2023-01-17')
    assert response.json() == [{
        "date": "2022-05-23",
        "views": 30,
        "clicks": 15,
        "cost": 30.0,
        "cpc": 2.0,
        "cpm": 1000.0
    }]


def test_more_than_one_entry(test_app):
    response = test_app.post('/stats', json={
        "date": "2022-05-23",
        "views": 10,
        "clicks": 5,
        "cost": 10.0
    })
    assert response.json().get('message') == "Stats saved"
    response = test_app.post('/stats', json={
        "date": "2022-08-05",
        "views": 20,
        "clicks": 10,
        "cost": 20.0
    })
    assert response.json().get('message') == "Stats saved"
    response = test_app.get('/stats?from=2022-01-17&to=2023-01-17')
    assert response.json() == [{
        "date": "2022-05-23",
        "views": 10,
        "clicks": 5,
        "cost": 10.0,
        "cpc": 2.0,
        "cpm": 1000.0
    }, {
        "date": "2022-08-05",
        "views": 20,
        "clicks": 10,
        "cost": 20.0,
        "cpc": 2.0,
        "cpm": 1000.0
    }]
    response = test_app.get('/stats?from=2022-01-17&to=2022-06-17')
    assert response.json() == [{
        "date": "2022-05-23",
        "views": 10,
        "clicks": 5,
        "cost": 10.0,
        "cpc": 2.0,
        "cpm": 1000.0
    }]
    response = test_app.get('/stats?from=2022-06-17&to=2022-09-17')
    assert response.json() == [{
        "date": "2022-08-05",
        "views": 20,
        "clicks": 10,
        "cost": 20.0,
        "cpc": 2.0,
        "cpm": 1000.0
    }]
    response = test_app.get('/stats?from=2022-01-17&to=2023-01-17&direction=DESC')
    assert response.json() == [{
        "date": "2022-08-05",
        "views": 20,
        "clicks": 10,
        "cost": 20.0,
        "cpc": 2.0,
        "cpm": 1000.0
    }, {
        "date": "2022-05-23",
        "views": 10,
        "clicks": 5,
        "cost": 10.0,
        "cpc": 2.0,
        "cpm": 1000.0
    }]
    response = test_app.post('/stats', json={
        "date": "2022-05-23",
        "views": 20,
        "clicks": 10,
        "cost": 20.0
    })
    assert response.json().get('message') == "Stats saved"
    response = test_app.get('/stats?from=2022-01-17&to=2023-01-17&direction=DESC')
    assert response.json() == [{
        "date": "2022-08-05",
        "views": 20,
        "clicks": 10,
        "cost": 20.0,
        "cpc": 2.0,
        "cpm": 1000.0
    }, {
        "date": "2022-05-23",
        "views": 30,
        "clicks": 15,
        "cost": 30.0,
        "cpc": 2.0,
        "cpm": 1000.0
    }]
    response = test_app.get('/stats?from=2022-01-17&to=2023-01-17&direction=DESC&order=views')
    assert response.json() == [{
        "date": "2022-05-23",
        "views": 30,
        "clicks": 15,
        "cost": 30.0,
        "cpc": 2.0,
        "cpm": 1000.0
    }, {
        "date": "2022-08-05",
        "views": 20,
        "clicks": 10,
        "cost": 20.0,
        "cpc": 2.0,
        "cpm": 1000.0
    }]

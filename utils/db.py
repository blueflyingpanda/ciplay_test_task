import sys
from os import environ
from psycopg2.pool import ThreadedConnectionPool
from utils.config import conf


db_pool = None

try:
    db_conf = conf['database']
    db_pool = ThreadedConnectionPool(user=environ.get('POSTGRES_USER'),
                                     password=environ.get('POSTGRES_PASSWORD'),
                                     host=environ.get('DB_SERVICE_NAME'),
                                     port=environ.get('DB_PORT'),
                                     database=environ.get('POSTGRES_DATABASE'),
                                     minconn=db_conf['min_connections'],
                                     maxconn=db_conf['max_connections'])
except KeyError as e:
    print(f"Configuration file is invalid: {e}", file=sys.stderr)
    raise e
except Exception as e:
    print(f"Error while connecting to database: {e}", file=sys.stderr)
    raise e

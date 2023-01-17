import sys

from psycopg2.pool import ThreadedConnectionPool
from utils.config import conf


db_pool = None

try:
    db_conf = conf['database']
    db_pool = ThreadedConnectionPool(user=db_conf['user'],
                                     password=db_conf['password'],
                                     host=db_conf['host'],
                                     port=db_conf['port'],
                                     database=db_conf['database'],
                                     minconn=db_conf['min_connections'],
                                     maxconn=db_conf['max_connections'])
except KeyError as e:
    print(f"Configuration file is invalid: {e}", file=sys.stderr)
    raise e
except Exception as e:
    print(f"Error while connecting to database: {e}", file=sys.stderr)
    raise e

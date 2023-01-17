import sys
import uvicorn

from utils.config import conf
from utils.db import db_pool
from utils.rest import app


def main():
    try:
        rest_conf = conf['restful_api']
        uvicorn.run(app, host=rest_conf['host'], port=int(rest_conf['port']))
    except Exception as e:
        print(f"Configuration file is invalid: {e}", file=sys.stderr)


if __name__ == '__main__':
    main()
    if db_pool:
        db_pool.closeall()

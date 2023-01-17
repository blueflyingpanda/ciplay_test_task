import logging
import os
import sys

from pathlib import Path
from utils.config import conf


LEVELS = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG
}


try:
    log_conf = conf['logging']

    if not os.path.exists(log_conf['logs_file']):
        os.makedirs(Path(log_conf['logs_file']).parent)

    logging.basicConfig(
        filename=log_conf['logs_file'],
        filemode='a',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=LEVELS[log_conf['level']]
    )
except KeyError as e:
    print(f"Configuration file is invalid: {e}", file=sys.stderr)
    raise e


logger = logging.getLogger('rest_logger')

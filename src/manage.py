import logging
import logging.config

from config.log_config import LOG_CONFIG
logging.config.dictConfig(LOG_CONFIG)

import argparse
import sys
from trades.parse_wisdom_contract_files import main as parse_wisdom_contract_files
LOGGER = logging.getLogger(__name__)


def main():
    arguments = sys.argv
    if not arguments or len(arguments) < 2:
        raise argparse.ArgumentTypeError("No arguments passed")
    # The first argument will be equal to manage.py
    # The second arg identifies the file and the rest of the arguments are the function arguments
    cmd = arguments[1]
    arguments = arguments[2:]
    if cmd == "parse_wisdom_contract_files":
        parse_wisdom_contract_files(*arguments)
    if cmd == "historical_data_nse":
        pass


if __name__ == '__main__':
    main()

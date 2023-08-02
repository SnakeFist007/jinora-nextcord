import logging
from logging.handlers import SysLogHandler
from main import PAPERTRAIL_URL, PAPERTRAIL_PORT


# * Logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        SysLogHandler(address=(PAPERTRAIL_URL, PAPERTRAIL_PORT)),
        logging.StreamHandler()
    ]
)
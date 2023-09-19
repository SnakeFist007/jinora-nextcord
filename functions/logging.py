import os
import logging
from dotenv import load_dotenv
from logging.handlers import SysLogHandler

load_dotenv()
PAPERTRAIL_URL = os.getenv("PAPERTRAIL_URL")
PAPERTRAIL_PORT = int(os.getenv("PAPERTRAIL_PORT"))


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
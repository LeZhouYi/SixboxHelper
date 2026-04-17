import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

logger_save_path = "data/log"
os.makedirs(logger_save_path, exist_ok=True)

logging.basicConfig(
    level="DEBUG",
    format="%(asctime)s-%(name)s-%(levelname)s-%(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        TimedRotatingFileHandler(
            filename=f"{logger_save_path}/log.log",
            when="midnight",
            interval=1,
            backupCount=7,
            encoding="utf-8"
        )
    ]
)
logger = logging.getLogger()

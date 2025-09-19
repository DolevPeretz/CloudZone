import logging
import json
import sys
from app import config

def setup_logger(name: str = "app") -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)

        class JsonFormatter(logging.Formatter):
            def format(self, record):
                return json.dumps({
                    "level": record.levelname,
                    "message": record.getMessage(),
                    "logger": record.name,
                }, ensure_ascii=False)

        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        logger.setLevel(config.LOG_LEVEL)

    return logger

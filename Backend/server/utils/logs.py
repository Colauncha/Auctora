# logging_config.py
import logging
from pythonjsonlogger import jsonlogger
from concurrent_log_handler import ConcurrentRotatingFileHandler

from server.config.app_configs import app_configs

env = app_configs.ENV

FILE_PATH = 'biddius.log' if env == 'development' else '/var/log/biddius-logs/biddius.log'

def setup_logging():
    handler = ConcurrentRotatingFileHandler(
        "biddius.log", maxBytes=10*1024*1024, backupCount=5
    )
    handler.setFormatter(jsonlogger.JsonFormatter(
        "%(asctime)s %(process)d %(levelname)s %(name)s: %(message)s"
    ))

    # Root logger (for your own app.logger.info(...) calls)
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(handler)

    # Uvicorn's loggers — attach explicitly since they don't propagate by default
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        uv_logger = logging.getLogger(name)
        # uv_logger.handlers = []          # remove Uvicorn's default stdout handler if you don't want duplicate output
        uv_logger.addHandler(handler)
        uv_logger.propagate = False
    
    request_logger = logging.getLogger('biddius.request')
    request_logger.setLevel(logging.INFO)
    request_logger.addHandler(handler)
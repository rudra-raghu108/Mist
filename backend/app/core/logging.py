# app/core/logging.py
import logging
import coloredlogs

def setup_logging():
    fmt = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    coloredlogs.install(level="INFO", fmt=fmt)
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)

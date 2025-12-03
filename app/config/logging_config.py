import logging
import sys
from pythonjsonlogger import jsonlogger
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True,exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

def get_logger(name: str = "app", level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = True

    fmt = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s %(value)s %(type_value)s"
    )

    fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
    fh.setLevel(level)
    fh.setFormatter(fmt)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    ch.setFormatter(fmt)

    if not logger.handlers:
        logger.addHandler(fh)
        # logger.addHandler(ch)

    return logger
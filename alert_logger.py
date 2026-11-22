
import logging
from pathlib import Path


def log_event(event_type, file_path):

    log_directory = Path("logs")
    log_directory.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("FIM_Logger")
    logger.setLevel(logging.INFO)

    if not logger.handlers:

        handler = logging.FileHandler(
            log_directory / "fim_alerts.log",
            encoding="utf-8"
        )

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.warning(
        "%s | File: %s",
        event_type,
        file_path
    )

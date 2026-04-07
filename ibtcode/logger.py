"""Logging setup using loguru."""

import sys
from loguru import logger
from ibtcode.config import cfg


def setup_logging(level: str | None = None) -> None:
    logger.remove()
    logger.add(
        sys.stderr,
        level=level or cfg.log_level,
        format=(
            "<green>{time:HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{line}</cyan> — {message}"
        ),
        colorize=True,
    )
    logger.add(
        "logs/ibtcode.log",
        level="DEBUG",
        rotation="1 MB",
        retention="7 days",
        compression="zip",
    )

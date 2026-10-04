"""统一日志配置：模块化、可配置级别。"""
import logging
import sys

from config.settings import settings


def setup_logging(level: str | None = None) -> None:
    level = (level or settings.log_level).upper()
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

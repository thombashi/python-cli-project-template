import sys

from ._const import MODULE_NAME


class LogLevel:
    DEBUG = "DEBUG"
    INFO = "INFO"
    QUIET = "QUIET"


class NullLogger:
    level_name = None

    def remove(self, handler_id=None):  # pragma: no cover
        pass

    def add(self, sink, **kwargs):  # pragma: no cover
        pass

    def disable(self, name):  # pragma: no cover
        pass

    def enable(self, name):  # pragma: no cover
        pass

    def critical(self, __message, *args, **kwargs):  # pragma: no cover
        pass

    def debug(self, __message, *args, **kwargs):  # pragma: no cover
        pass

    def error(self, __message, *args, **kwargs):  # pragma: no cover
        pass

    def exception(self, __message, *args, **kwargs):  # pragma: no cover
        pass

    def info(self, __message, *args, **kwargs):  # pragma: no cover
        pass

    def log(self, __level, __message, *args, **kwargs):  # pragma: no cover
        pass

    def success(self, __message, *args, **kwargs):  # pragma: no cover
        pass

    def trace(self, __message, *args, **kwargs):  # pragma: no cover
        pass

    def warning(self, __message, *args, **kwargs):  # pragma: no cover
        pass


try:
    from loguru import logger

    logger.disable(MODULE_NAME)
except ImportError:
    logger = NullLogger()  # type: ignore


def set_logger(is_enable: bool, propagation_depth: int = 1):
    if is_enable:
        logger.enable(MODULE_NAME)
    else:
        logger.disable(MODULE_NAME)


def initialize_logger(name: str, log_level: str) -> None:
    logger.remove()

    if log_level == LogLevel.QUIET:
        logger.disable(name)
        return

    if log_level == "DEBUG":
        log_format = (
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:"
            "<cyan>{function}</cyan>:"
            "<cyan>{line}</cyan> - <level>{message}</level>"
        )
    else:
        log_format = "<level>[{level}]</level> {message}"

    logger.add(sys.stderr, colorize=True, format=log_format, level=log_level)
    logger.enable(name)

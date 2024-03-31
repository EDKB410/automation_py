import logging
import logging.config
import sys
from logging import FileHandler

APP_NAME = "opencart"

def _init_logger(name='', level=None, logfile=None):
    if name:
        name = f'{APP_NAME}.{name}'
    else:
        name = APP_NAME

    logger = logging.getLogger(name)

    if logger.parent is not logging.root:
        return logger

    # if len(logger.handlers):
    #     return logger

    formatter = logging.Formatter(
        '{asctime} [{levelname}] [{name}] [{funcName}] > {message}', style='{')
    
    if level:
        logger.setLevel(level)
    
    stream_handler = logging.StreamHandler(sys.stderr)
    if level:
        stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if logfile:
        file_handler = FileHandler(filename=logfile, mode='a')
        if level:
            file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

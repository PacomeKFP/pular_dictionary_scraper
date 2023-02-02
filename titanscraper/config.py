import logging
import os


LOGGING_FILENAME = "scraperLog.log"
LOGGING_DIR = ""

LOGGING_FILEPATH = os.path.join(LOGGING_DIR, LOGGING_FILENAME)
LOGGING_FORMAT = "%(levelname)s %(asctime)s  %(name)s - %(message)s"
LOGGING_STREAM_FORMAT = "[%(levelname)s] - %(message)s"
LOGGING_LEVEL = logging.DEBUG

# define the formatter of the log
LOGGING_FORMATTER = logging.Formatter(LOGGING_FORMAT)
LOGGING_STREAM_FORMATTER = logging.Formatter(LOGGING_STREAM_FORMAT)

# define the file handler of the log file
LOGGING_FILE_HANDLER = logging.FileHandler(LOGGING_FILEPATH)
LOGGING_FILE_HANDLER.setFormatter(LOGGING_FORMATTER)
LOGGING_STREAM_HANDLER = logging.StreamHandler()
LOGGING_STREAM_HANDLER.setFormatter(LOGGING_STREAM_FORMATTER)
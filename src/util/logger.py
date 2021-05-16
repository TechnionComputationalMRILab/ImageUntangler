from io import StringIO
import sys
import logging


logger = logging.getLogger(__name__)
formatter = \
    logging.Formatter('%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s')
string_stream = StringIO()

logging.basicConfig(stream=string_stream, level=logging.DEBUG)


def logger_setup():
    file_handler = logging.FileHandler('../log.txt')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # logging.basicConfig(stream=string_stream, level=logging.DEBUG)


def get_logger():
    return logger


def get_log_stream():
    # string_stream = StringIO()
    # logging.basicConfig(stream=string_stream, level=logging.DEBUG)

    return string_stream.getvalue()

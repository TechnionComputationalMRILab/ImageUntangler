import nrrd

import logging
logging.getLogger(__name__)


def save_as_nrrd(array, filename, header=None):
    if not header:
        header = dict()

    logging.info(f"Creating a NRRD file with size {array.shape}")

    try:
        nrrd.write(filename, array, index_order='F', header=header)
    except Exception as err:
        logging.info(f"NRRD file error: {err}")
    else:
        logging.info(f"NRRD file created")

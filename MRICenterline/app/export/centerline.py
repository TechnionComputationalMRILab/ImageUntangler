import logging
logging.getLogger(__name__)


def export(cl_model, destination, options):
    logging.info(f"Exporting CL to {destination} as {options}")

    print(cl_model.nparray.shape)

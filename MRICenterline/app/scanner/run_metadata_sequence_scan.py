from pathlib import Path
from MRICenterline.app.file_reader.imager import Imager

import logging
logging.getLogger(__name__)


def run_metadata_sequence_scan(folders, parent_widget=None, running_for_v3_scanner=False):
    if running_for_v3_scanner:
        root_folder = folders.pop(0)
        logging.info(f"Using {root_folder} as folder root")
    else:
        root_folder = None

    num_folders = len(folders)
    for index, folder in enumerate(folders):
        get_metadata(folder, index, num_folders, root_folder, parent_widget, running_for_v3_scanner)

    logging.info("Metadata sequence scan complete!")

    if parent_widget:
        done_message = f"Done! You may close."
        parent_widget.add_to_textbox(done_message)


def get_metadata(folder, index, num_folders, root_folder, parent_widget=None, running_for_v3_scanner=False):
    if running_for_v3_scanner and Path(folder).parts[-1] == 'data':
        logging.info(f"Skipping {folder}")
        return f"Skipping {folder}"

    reading_info = f"[{1 + index} / {num_folders}] Reading {folder}"
    logging.info(reading_info)
    if parent_widget:
        parent_widget.add_to_textbox(reading_info)

    try:
        imager = Imager(folder, root_folder=root_folder)
    except NotImplementedError:
        error_info = f"{folder} is either not supported or has no MRI images."
        logging.warning(error_info)
        if parent_widget:
            parent_widget.add_to_textbox(error_info, color='red')
        return error_info
    else:
        reading_done_info = f"Folder is {imager.file_type} | {len(imager)} sequences found"
        logging.info(reading_done_info)
        if parent_widget:
            parent_widget.add_to_textbox(reading_done_info)
        return reading_done_info

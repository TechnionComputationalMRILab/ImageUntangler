import os
from pathlib import Path
import sqlite3
import shutil
from MRICenterline import CFG
from MRICenterline.app.database.name_id import get_case_name

import logging

logging.getLogger(__name__)


def export_as_dicom(case_id: int, seq_id: int, destination):
    con = sqlite3.connect(CFG.get_db())
    filenames = [i[0] for i in con.cursor().execute(
        f"select filename from 'sequence_files' where case_id={case_id} and seq_id={seq_id + 1}").fetchall()]
    con.close()

    source_folder = CFG.get_folder("raw_data")
    case_name = get_case_name(case_id)
    Path(destination).mkdir(parents=True, exist_ok=True)

    logging.info(f"Copying {len(filenames)} files to {destination}")

    for idx, file in enumerate(filenames):
        logging.info(f"Copying file {idx} / {len(filenames)} | {file}")
        shutil.copy(os.path.join(source_folder, case_name, file), destination)

    logging.info("Copy complete")

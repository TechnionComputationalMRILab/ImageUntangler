from glob import glob
from typing import List
from pathlib import Path

from MRICenterline.app.points.import_from_v3 import Ver3AnnotationImport

import logging
logging.getLogger(__name__)


def load_v3_points(folders: List[str] or List[Path]):
    logging.info("Starting v3 point loader")
    num_folders = len(folders)

    for index, folder in enumerate(folders):
        logging.info(f"[{1 + index} / {num_folders}] Reading {folder}")
        root_folder = folder.parents[1]

        if Path(folder).parts[-1] == 'data':
            for annotation_file in [Path(i) for i in glob(f"{folder}/*.annotation.json")]:
                if Path(annotation_file).name.split(".")[-3] == "centerline":
                    pass
                    # centerline_files.add(annotation_file)
                else:
                    try:
                        importer = Ver3AnnotationImport(annotation_file, root_folder)
                    # TODO: should not be needed when using the Rambam PC
                    except KeyError:
                        pass
                    else:
                        print(importer)
                        importer.commit()

        else:
            pass


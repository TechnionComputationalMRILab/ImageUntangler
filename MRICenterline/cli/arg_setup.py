import argparse
from glob import glob
from pathlib import Path

from MRICenterline.app import scanner
from MRICenterline import CONST

import logging
logging.getLogger(__name__)

'''
Generate sequence/metadata report:
    creates a CSV listing the cases, a list of the sequences available for each case, and the metadata
    in the heading file for each case
    
Organize folder data:
    NOT IMPLEMENTED

Generate timing report:
    creates a CSV listing the cases, the time it took the radiologist to do the "normal" measurement, 
    and the measurement with the centerlines
    
Load points from v3:
    IU v3 used separate JSON files to store the points for each session in a sub-folder inside the case folders
    called 'data'. This takes those files and merges them into the SQLite database used by v4
'''


def arg_setup():
    parser = argparse.ArgumentParser(description='ImageUntangler Commandline')

    parser.add_argument('-f', '--folder', action='store', type=str,
                        help="Folder to scan", required=True)

    arguments = [
        ("-s", "--scan", "Generate sequence/metadata report"),
        ("-o", "--org", "Organize folder data"),
        ("-t", "--time", "Generate timing report"),
        ("-v3", "--ver3", "Load points from v3")
    ]

    for sh, lo, he in arguments:
        parser.add_argument(sh, lo, action='store_true', help=he)

    args = parser.parse_args()
    directories = [Path(i) for i in glob(f"{args.folder}/**/", recursive=True)]

    logging.info(f"Starting scan: {args.folder}, found {len(directories)} folders.")

    if args.scan:
        logging.info("Generate sequence/metadata report")
    if args.org:
        logging.warning("Organize folder data")
        print(f"This functionality is not implemented in {CONST.VER_NUMBER}")
    if args.time:
        logging.info("Generate timing report")
    if args.ver3:
        logging.info("Load points from v3")
        scanner.run_metadata_sequence_scan(directories, running_for_v3_scanner=True)
        scanner.load_v3_points(directories)

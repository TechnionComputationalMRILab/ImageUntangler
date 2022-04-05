import argparse

from MRICenterline.app import scanner

import logging
logging.getLogger(__name__)


def arg_setup():
    parser = argparse.ArgumentParser(description='ImageUntangler CLI version')

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

    logging.info(f"Starting scan: {args.folder}")

    # TODO: create a temporary CFG file for the scanner to use

    if args.scan:
        logging.info("Generate sequence/metadata report")
    if args.org:
        logging.info("Organize folder data")
    if args.time:
        logging.info("Generate timing report")
    if args.ver3:
        logging.info("Load points from v3")
        scanner.run_metadata_sequence_scan(args.folder)
        scanner.load_v3_points(args.folder)

import os
from glob import glob
from pathlib import Path
import csv
from tqdm import tqdm

from MRICenterline.BulkFolderScanner import Scanner


def run_folder_scan(folder):
    folder = (folder[0])
    directories = [Path(file) for file in glob(f"{folder}/**/", recursive=True)]

    try:
        os.remove(os.path.join(folder, 'report.csv'))
    except Exception:
        pass

    if len(directories) > 0:
        print(f"Starting scan of {len(directories)} directories!")

        _to_csv = []
        for i, val in enumerate(directories):
            _dict = Scanner.generate_report(val)
            if _dict:
                _dict['Path'] = val
                _to_csv.append(_dict)
            else:
                pass

            print(f"Processing folder {i + 1}/{len(directories)} : {val}")

        with open(os.path.join(folder, 'report.csv'), 'w', encoding='utf8', newline='') as output_file:
            fc = csv.DictWriter(output_file, fieldnames=_to_csv[0].keys())
            fc.writeheader()
            fc.writerows(_to_csv)

        print("Cleaning up...")

        json_files = [Path(file) for file in glob(f"{folder}/**/seqdict.json", recursive=True)]
        if json_files:
            [os.remove(file) for file in json_files]

        data_dirs = [Path(file) for file in glob(f"{folder}/**/data/", recursive=True)]
        if data_dirs:
            [os.rmdir(file) for file in data_dirs]

        print(f"Done! Report is saved to {os.path.join(folder, 'report.csv')}.")
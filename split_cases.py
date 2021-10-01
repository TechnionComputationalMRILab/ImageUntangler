import csv
import ast
import os
import shutil
from pathlib import Path

MOVE_TO = Path(r"C:\Users\rambam-user\Desktop\processed")

with open('report.csv', 'r') as f:
    di = list(csv.DictReader(f))

    for key, val in enumerate(di):
        val['key'] = key + 1 # assign simple keys

        seq_list = ast.literal_eval(val['Sequences'])
        for j in seq_list:
            try:
                int(j)
            except ValueError: # then the sequence is ok
                val['is_ok'] = True
            else: # then the sequence is not ok
                val['is_ok'] = False

        if val['is_ok']:
            destination = os.path.join(MOVE_TO, "ok", str(val['key']))
        else:
            destination = os.path.join(MOVE_TO, "not_ok", str(val['key']))
        print(destination)

        print(f"Moving {Path(val['Path'])} to {destination}")
        shutil.copy(Path(val['Path']), destination)

        val["Path"] = destination

with open("new_report.csv", 'w', newline='') as f:
    wr = csv.DictWriter(f, fieldnames=list(di[0].keys()))
    wr.writeheader()

    for i in di:
        wr.writerow(i)

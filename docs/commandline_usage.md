# Commandline Interface

WARNING: The program defaults to the GUI if no arguments are given.

## Help text

```
ImageUntangler Commandline

optional arguments:
  -h, --help            show this help message and exit
  -f FOLDER, --folder FOLDER
                        Folder to scan
  -s, --scan            Generate sequence/metadata report
  -o, --org             Organize folder data
  -t, --time            Generate timing report
  -v3, --ver3           Load points from v3
```

## Functions


### Generate sequence/metadata report
Creates a CSV listing the cases, a list of the sequences available for each case, and the metadata  in the heading file for each case
    
### Organize folder data
**Not implemented as of v-4.0**

Re-organizes and anonymizes cases in nested folders into a flat folder sturcture where each case is named 1, 2, 3...

### Generate timing report:
Creates a CSV listing the cases, the time it took the radiologist to do the "normal" measurement, and the measurement with the centerlines
    
### Load points from v3:
Used to migrate from the v3 structure to v4.

IU v3 used separate JSON files to store the points for each session in a sub-folder inside the case folders called 'data'. This takes those files and merges them into the SQLite database used by v4

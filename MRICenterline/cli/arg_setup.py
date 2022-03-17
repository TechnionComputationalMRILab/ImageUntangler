from MRICenterline.CommandLineInterface import run_folder_scan
import sys

opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

if "-f" in opts:
    run_folder_scan(args)
else:
    raise SystemError("Please see usage instructions.")

__author__ = "Yael Zaffrani and Avraham Kahan and Angeleene Ang"

import os
import sys
from vtkmodules.all import vtkOutputWindow

# move VTK warnings/errors to terminal
vtk_out = vtkOutputWindow()
vtk_out.SetInstance(vtk_out)

args = sys.argv

if "--clean" in args:
    try:
        os.remove("config.ini")
    except OSError:
        pass

    try:
        os.remove("metadata.db")
    except OSError:
        pass

    args.remove("--clean")


if len(args) == 1:
    # run as GUI application
    from MRICenterline.gui import start
    start()
else:
    # run as CLI application
    from MRICenterline.cli import arg_setup
    arg_setup()


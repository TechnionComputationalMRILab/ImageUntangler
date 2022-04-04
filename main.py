__author__ = "Yael Zaffrani and Avraham Kahan and Angeleene Ang"

import sys

from icecream import ic, install
install()
ic.configureOutput(includeContext=True)

from vtkmodules.all import vtkOutputWindow

# move VTK warnings/errors to terminal
vtk_out = vtkOutputWindow()
vtk_out.SetInstance(vtk_out)


if len(sys.argv) == 1:
    # run as GUI application
    from MRICenterline.gui import start
    start()
else:
    # run as CLI application
    pass

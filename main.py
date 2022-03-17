__author__ = "Yael Zaffrani and Avraham Kahan and Angeleene Ang"

import sys

from icecream import ic, install
install()
ic.configureOutput(includeContext=True)

if len(sys.argv) == 1:
    # run as GUI application
    from MRICenterline.gui import start
    start()
else:
    # run as CLI application
    pass

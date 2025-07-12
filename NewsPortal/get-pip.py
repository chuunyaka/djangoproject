#!/usr/bin/env python
"""Install pip as a standalone zipapp.

This bootstrapping script is a reduced version of the one in the
official repository: https://github.com/pypa/get-pip

It installs pip from the PyPI wheel, bypassing the need for pre-existing pip.
"""

import runpy
import tempfile
import os
import shutil
import urllib.request

URL = "https://bootstrap.pypa.io/pip/pip.pyz"

def main():
    print("Downloading pip...")
    with urllib.request.urlopen(URL) as resp:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pyz") as tmp_file:
            shutil.copyfileobj(resp, tmp_file)
            tmp_path = tmp_file.name

    print(f"Running pip bootstrap from {tmp_path}...")
    runpy.run_path(tmp_path, run_name="__main__")

    print("Cleaning up...")
    os.remove(tmp_path)
    print("pip installed successfully.")

if __name__ == "__main__":
    main()

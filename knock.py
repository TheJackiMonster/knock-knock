#!/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Tobias Frisch"
__copyright__ = "Copyright 2025, Tobias Frisch"
__credits__ = "Tobias Frisch"

__license__ = "GPL"
__license_version__ = "3.0.0"

__maintainer__ = "Tobias Frisch"
__email__ = "jacki@thejackimonster.de"
__status__ = "Production"
__version__ = "1.0.0"

import sys

try:
    from icmplib import ping, SocketPermissionError

    def knock(address):
        try:
            host = ping(address, count=1, privileged=False)
            return host.is_alive
        except SocketPermissionError:
            return False

except ModuleNotFoundError:
    import subprocess

    def knock(address):
        process = subprocess.run(["ping", "-c", "1", address], capture_output=True)
        return process.returncode == 0

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if knock(sys.argv[1]):
            exit(0)
        else:
            exit(1)
    else:
        exit(2)


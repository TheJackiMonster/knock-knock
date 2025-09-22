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

import socket
import sys

def knock_stream(address: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((address, port))
            data = s.recv(1024)
            return len(data) > 0
        except (OSError, TimeoutError, InterruptedError):
            return False

try:
    from icmplib import ping, SocketPermissionError

    def knock(address: str, port: int | None = None):
        try:
            host = ping(address, count=1, privileged=False)
            return host.is_alive
        except SocketPermissionError:
            return knock_stream(address, port) if port else False

except ModuleNotFoundError:
    import subprocess

    def knock(address: str, port: int | None = None):
        try:
            process = subprocess.run(["ping", "-c", "1", address], capture_output=True)
            return process.returncode == 0
        except PermissionError:
            return knock_stream(address, port) if port else False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if knock(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else None):
            exit(0)
        else:
            exit(1)
    else:
        exit(2)


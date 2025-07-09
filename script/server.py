#!/usr/bin/env python3

import os
import subprocess

class Server:

    def __init__(self):
        self.is_credentials = False
        self.credentials = None

    def start_server(self):
        if os.path.exists("../web/"):
            os.chdir("../web/")

            subprocess.run(['python3', '-m', 'http.server', '80'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
 
    def request_status(self):
        pass

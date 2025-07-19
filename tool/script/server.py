#!/usr/bin/env python3

import os
import subprocess

class Server:

    def start_server(self, ip):
        path = os.getcwd() + "/web_server/"
        if os.path.exists(path):
            os.chdir(path)

            subprocess.run(['node', 'server.js'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

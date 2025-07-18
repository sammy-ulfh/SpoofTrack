#!/usr/bin/env python3

import os
import subprocess

class Server:

    def start_server(self, ip):
        if os.path.exists("../script/web_server/"):
            os.chdir("../script/web_server/")

            subprocess.run(['node', 'server.js'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

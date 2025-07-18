#!/usr/bin/env python3

import os
import subprocess

class Server:

    def __init__(self):
        self.is_credentials = False
        self.credentials = None

    def replace(self, ip):
        route = f'{os.getcwd()}/js/script.js'
        if os.path.exists(route):
            with open(route, 'r') as f:
                content = f.read()

                with open(route, 'w') as f:
                    content = content.replace('URL_DEL_ENDPOINT', f'http://{ip}:80/api/datos')
                    f.write(content)

    def start_server(self, ip):
        if os.path.exists("../web/"):
            os.chdir('../web/')
            self.replace(ip)

            os.chdir("../script/web_server/")

            subprocess.run(['node', 'server.js'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

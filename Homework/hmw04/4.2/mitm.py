from netfilterqueue import NetfilterQueue
from scapy.layers.inet import IP
from scapy.layers import http

def packetReceived(pkt):
    # convert the packet to scapy form
    ip = IP(pkt.get_payload())

    # look at the raw layer
    if ip.haslayer("Raw"):
        tcpPayload = ip["Raw"].load

        # filter out the TLS handshake
        if tcpPayload[0] == 0x16 and tcpPayload[1] == 0x03:
            # filter out TCP handshake with cypher TLS_RSA_WITH_AES_256_CBC_SHA
            if (tcpPayload[46] == 0x00 and tcpPayload[47] == 0x35):
                msgBytes = pkt.get_payload()  # msgBytes is read-only, copy it

                # copy msgBytes since it is read-only.
                msgBytes2 = [b for b in msgBytes]
                msgBytes2[112] = 0x00
                msgBytes2[113] = 0x2F
                pkt.set_payload(bytes(msgBytes2))

    pkt.accept()
    return


nfqueue = NetfilterQueue()
nfqueue.bind(1, packetReceived)

try:
    nfqueue.run()

except KeyboardInterrupt:
    print('')

nfqueue.unbind()
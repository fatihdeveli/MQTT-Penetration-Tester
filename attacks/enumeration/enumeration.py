import copy
import time

import paho.mqtt.client as mqtt

topic_set = dict()


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    url = input("Enter broker URL: ")
    try:
        client.connect(url, 1883, 60)
    except Exception as e:
        raise e

    client.loop_start()

    tmp = copy.deepcopy(topic_set)

    try:
        while True:
            time.sleep(1)
            if not (tmp == topic_set):
                tmp = copy.deepcopy(topic_set)
    except KeyboardInterrupt:
        client.loop_stop()
        write_results()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe("#")
        print("Successfully connected. Hit Ctrl-C to stop.")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global topic_set
    if msg.topic in topic_set:
        topic_set[msg.topic].append(msg.payload)
    else:
        topic_set[msg.topic] = [msg.payload]


def write_results():
    f = open('results.txt', 'w')
    for k in topic_set:
        f.write("Topic: " + k + '\n')
        for m in topic_set[k]:
            if len(m) > 1000:  # Prevent flooding the file with large data
                continue
            f.write(str(m) + '\n')
    print('All messages are written to results.txt')
    f.close()


if __name__ == '__main__':
    main()

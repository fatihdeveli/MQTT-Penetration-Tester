## Sniffer

Run with
```shell script
sudo python3 sniffer.py 
```

The script will print captured MQTT messages and credentials while it is running.

To simulate MQTT messages, Mosquitto clients can be used. Install it with:

```shell script
sudo apt install mosquitto-clients
```

To send a message to topic `test` of the public MQTT broker `mqtt.eclipse.org`:

```shell script
mosquitto_pub -h mqtt.eclipse.org -t test -m "hello world"
```

Use `-u` and `-P` flags to include username and password if the broker is password protected.
## Dictionary Attack

By default the script is configured to attack on a broker running on `localhost`. To run an mqtt broker locally,
Mosquitto can be used.

Install mosquitto with
```shell script
sudo apt install mosquitto
```
After installing, broker service will start automatically in the background, however this service do not implement
password authentication. To stop the service, use:
```shell script
sudo service mosquitto stop
```

Now create the configuration file `password.conf` and password file `passwords.txt`. In `password.conf`, paste this,
replacing the path with the correct path to the file.

```
allow_anonymous false
password_file /path/to/passwords.txt
```

Now, create a user with a username, enter a password when prompted:
```shell script
mosquitto_passwd -c passwords.txt <username>
```

Now the broker can be started with this password configuration:
```shell script
mosquitto -c password.conf
```

Now the broker is running with authentication on localhost, and the script can be run.

```shell script
python3 dictionary_attack.py
```
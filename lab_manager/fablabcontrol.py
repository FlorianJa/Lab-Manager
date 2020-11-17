import paho.mqtt.subscribe as subscribe
import json
from datetime import datetime
import paho.mqtt.client as mqttclient
import time

def on_mqtt_connect(client, userdata, flags, rc):
        if int(rc) != 0:
            if int(rc) == -4:
                print("MQTT_CONNECTION_TIMEOUT")
            elif int(rc) == -3:
                print("MQTT_CONNECTION_LOST")
            elif int(rc) == -2:
                print("MQTT_CONNECT_FAILED")
            elif int(rc) == 1:
                print("MQTT_CONNECT_BAD_PROTOCOL")
            elif int(rc) == 2:
                print("MQTT_CONNECT_BAD_CLIENT_ID")
            elif int(rc) == 3:
                print("MQTT_CONNECT_UNAVAILABLE")
            elif int(rc) == 4:
                print("MQTT_CONNECT_BAD_CREDENTIALS")
            elif int(rc) == 5:
                print("MQTT_CONNECT_UNAUTHORIZED")
        else:
            print("Mit MQTT Server verbunden...")
            global connected
            connected=True
def on_mqtt_message(client, userdata, msg):
    import json
    import datetime
    print("MQTT Nachricht empfangen" + msg.topic +
              " " + msg.payload.decode('UTF-8'))
    
connected=False
messageReceived=False

broker_address=""
port=
user=""
password=""

client= mqttclient.Client("MQTT")
client.on_message=on_mqtt_message
client.username_pw_set(user,password=password)
client.on_connect=on_mqtt_connect
client.connect(broker_address,port=port)
client.loop_start()
client.subscribe("fablab/printers/eos/#")

while connected!=True:
    time.sleep(0.2)
while messageReceived!=True:
    time.sleep(0.2)
client.loop_stop()

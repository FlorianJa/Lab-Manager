# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import paho.mqtt.client as mqtt
import threading
import datetime
import time


MQTT_HOST = '127.0.0.1'
MQTT_PORT = 1884
# WARNING add credentials
MQTT_USER = 'fablabcontrol'
MQTT_PASS = 'fablabcontrol'

# Topics
# FabLab WebIf
# FabLab/{esp_mac}/cmd/ {uuid} no-retain subscribe
# FabLab/{esp_mac}/status/ {uuid} retain publish

# FabLab ESP
# FabLab/{esp_mac}/cmd/ {uuid} no-retain publish
# FabLab/{esp_mac}/status/ {uuid} retain subscribe

# json message
# {'cmd':'command','data':'information'}


class fablabcontrolThread(threading.Thread):
    def __init__(self, event):
        threading.Thread.__init__(self)
        self.stop_event = event
        self.mqttc = None

    def run(self):
        print("Start FabLabControl Thread, wait for Django ....")
        time.sleep(5.0)

        # mqtt client starten
        self.mqttc = mqtt.Client()
        self.mqttc.on_message = self.on_mqtt_message
        self.mqttc.username_pw_set(MQTT_USER, password=MQTT_PASS)
        self.mqttc.on_connect = self.on_mqtt_connect
        self.mqttc.connect(MQTT_HOST, MQTT_PORT)
        self.mqttc.on_disconnect = self.on_mqtt_disconnect

        try:
            while not self.stop_event.wait(0.2):
                self.mqttc.loop_start()
        finally:
            self.mqttc.disconnect()

    def on_mqtt_connect(self, client, userdata, flags, rc):
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
            print("Connected to MQTT server ...")
            client.subscribe("#")
            # django.setup()

    def on_mqtt_disconnect(self, client, userdata, rc):
        self.mqttc.reconnect()
        if rc != 0:
            print("MQTT connection lost ...")

    def on_mqtt_message(self, client, userdata, msg):
        import json
        from channels import Group
        import datetime

        print("MQTT message received" + msg.topic +
              " " + msg.payload.decode('UTF-8'))
        print(msg)
        try:
            topic = msg.topic.split('/')
            data = json.loads(msg.payload.decode('UTF-8'))
            print(topic)
            print(data)
            if str(topic[0]) == "FabLabevent" and str(topic[1]) == "PrintDone":
                self.add_usage(data)

        except Exception as e:
            print(e)

    def login(self, esp_mac):
        from .models import FabLabUser
        from lab_manager.serializers import FabLabUserSerializer
        import json
        import datetime
        try:
            user = FabLabUser.objects.get(rfid_uuid=esp_mac)
            user.is_login = True
            fablabuser_serializer = FabLabUserSerializer(user, data=user_data)
            if fablabuser_serializer.is_valid():
                fablabuser_serializer.save()
                print(+ esp_mac + ": login status as Active updated")
        except FabLabUser.DoesNotExist:
            return JsonResponse({'message': 'The User does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def add_usage(self, data):
        from lab_manager.serializers import UsageSerializer, MaterialSerializer, PrinterSerializer, PrinterSerializer
        from .models import UsageData, Material, Printer, Operating
        import json
        import datetime
        material = Material.objects.get(pk=1)
        operating = Operating.objects.get(pk=1)
        printer = Printer.objects.get(pk=1)
        usage_data = {
            "user": data["owner"],
            "file_name": data["name"],
            "print_time": data["time"],
            "time_stamp": data["_timestamp"],
            "state": data["_event"],
            "printer_name": 'EOS',
            "filament_price": material.filament_price,
            "filament_weight": material.filament_weight,
            "model_weight": material.model_weight,
            "price_printer": printer.price_printer,
            "lifespan": printer.lifespan,
            "maintainence_cost": printer.maintainence_cost,
            "electricity_cost": operating.electricity_cost,
            "power_consumption": operating.power_consumption
        }
        #usage_data = JSONParser().parse(request)
        usage_serializer = UsageSerializer(data=usage_data)
        if usage_serializer.is_valid():
            usage_serializer.save()

    def logout(self, esp_mac, data):
        from .models import FabLabUser
        from lab_manager.serializers import FabLabUserSerializer
        import json
        import datetime
        try:
            user = FabLabUser.objects.get(rfid_uuid=esp_mac)
            if(data["owner"] == user.username and data["_event"] == "PrintDone"):
                user.is_login = False
            fablabuser_serializer = FabLabUserSerializer(user, data=user_data)
            if fablabuser_serializer.is_valid():
                fablabuser_serializer.save()
                print(+ esp_mac + ": login status as Inactive updated")
        except FabLabUser.DoesNotExist:
            return JsonResponse({'message': 'The User does not exist'}, status=status.HTTP_404_NOT_FOUND)

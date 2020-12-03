# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import paho.mqtt.client as mqtt
import threading
import time
from rest_framework.parsers import JSONParser 
import simplejson



MQTT_HOST = '18.198.3.0'
MQTT_PORT = 1883
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
            self.mqttc.subscribe([("FabLabevent/PrintDone", 2),("FabLab/+/cmd", 2)])
            # django.setup()

    def on_mqtt_disconnect(self, client, userdata, rc):
        self.mqttc.reconnect()
        if rc != 0:
            print("MQTT connection lost ...")
    def on_mqtt_message(self, client, userdata, msg):
        import json
        import datetime
        print("MQTT Nachricht empfangen" + msg.topic +
              " " + msg.payload.decode('UTF-8'))
        try:
            topic = msg.topic.split('/')
            data = json.loads(msg.payload.decode('UTF-8'))
            print(topic)
            print(data)
            if(data["_event"]=="PrintDone"):
                print("print done event received")
                self.add_usage(data)
        except Exception as e:
            print(e)
    
           
    def add_usage(self,data):
        from .models import UsageData,PrinterUsage,OperatingUsage,FilamentUsage
        import json
        import time
        from datetime import datetime
        from decimal import Decimal
        import requests
        
        operating = OperatingUsage.objects.get(pk=1)
        printer = PrinterUsage.objects.get(pk=1)
        filament = FilamentUsage.objects.get(filament_name='Other')        
        print_time = time.strftime("%H:%M:%S", time.gmtime(data["time"]))
        print_time_hrs = data["time"]/3600
        print("variables initialised")
        
        AdditionCost = 0
        if(printer.lifespan > 0):
            depreciation_per_hour= printer.price_printer / printer.lifespan
        else:
            depreciation_per_hour=0
            
        print("variables initialised2")
        FilamentCost= round((filament.filament_price/filament.filament_weight)* Decimal(0),2)
        print("variables initialised3")
        OperatingCost= round((operating.power_consumption*operating.electricity_cost)*Decimal(print_time_hrs),2)
        print("variables initialised4")
        PrinterCost= round((depreciation_per_hour+printer.maintainence_cost)* Decimal(print_time_hrs),2)
        print("variables initialised5")
        TotalCost= round(FilamentCost+OperatingCost+PrinterCost+ Decimal(AdditionCost),2)
        print("variables initialised6")
        print("calculation done")
        
        self.request=simplejson.dumps({
             "owner": data["owner"],
             "file_name": data["name"],
             "print_time": print_time,
             "time_stamp": str(datetime.fromtimestamp(data["_timestamp"])),
             "print_status": data["_event"],
             "printer_name":"EOS",
             "filament_price":filament.filament_price,
             "filament_name":filament.filament_name,
             "filament_weight":filament.filament_weight,
             "filament_used":"0.0",
             "filament_cost":FilamentCost,
             "operating_cost":OperatingCost,
             "printer_cost":PrinterCost,
             "additional_cost":AdditionCost,
             "total_cost":TotalCost
             })
        print(self.request)
        try:
            r = requests.post('http://localhost:8080/api/usage', self.request)
            print(r)
        except Exception as e:
            print(e)
            
        
        
        # usage_data = JSONParser().parse(request)
        # usage_serializer = UsageSerializer(data=usage_data)
        # if usage_serializer.is_valid():
        #     usage_serializer.save()
        #     print("print done event saved to db")
        # else:
        #     print("print done event not saved to db")

        # if str(topic[0]) == "FabLab" and str(topic[2]) == "cmd":
        #         if data["cmd"] == "1":
        #             print("ESP " +
        #                   str(topic[1]) +
        #                   " will anmelden..." +
        #                   msg.payload.decode('UTF-8'))
        #             self.login(str(topic[1]), data)
        #         elif data["cmd"] == "3":
        #             print("ESP " +
        #                   str(topic[1]) +
        #                   " will abmelden..." + 
        #                   msg.payload.decode('UTF-8'))
        #             self.logout(str(topic[1]), data)
        # if str(topic[0]) == "FabLab" and str(topic[2]) == "cmd":
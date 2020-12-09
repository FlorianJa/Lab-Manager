# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import paho.mqtt.client as mqtt
import threading
import time
from rest_framework.parsers import JSONParser
import simplejson


MQTT_HOST = '54.93.38.253'
MQTT_PORT = 1883
# WARNING add credentials
MQTT_USER = 'fablabdev'
MQTT_PASS = 'fablabdev'

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
            self.mqttc.subscribe(
                [("FabLabevent/PrintDone", 2), ("FabLabevent/PrintStarted", 2), ("FabLabevent/PrintCancelled", 2), ("FabLab/UserStatus", 2)])  # change it for testing in real time
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
            if(data["_event"] == "Login"):
                print("Login event received")
                self.login(data)
            if(data["_event"] == "Logout"):
                print("Logout event received")
                self.logout(data)

            if(data["_event"] == "PrintCancelled"):
                print("Logout event received")
                self.logout(data)

            if(data["_event"] == "PrintDone"):
                self.add_usage(data)
                self.add_print_hours_maintenance(data)
                self.logout(data)

            if(data["_event"] == "PrintStarted"):
                print("print start event received")
                self.login(data)

        except Exception as e:
            print(e)

    def login(self, data):
        from .models import FabLabUser
        import requests
        import datetime

        print('login start')

        today = datetime.datetime.now()
        date_time = today.strftime("%m-%d-%Y, %H:%M:%S")

        try:
            if(data["_event"] == "PrintStarted"):
                user = FabLabUser.objects.get(username=data["owner"])
            else:
                user = FabLabUser.objects.get(
                    rfid_uuid=data["rfid_number"])
        except Exception as e:
            print(e)

        try:
            if(data["_event"] == "PrintStarted") and not user:
                username = data["owner"]
                name = data["owner"]
                assigned_by = data["owner"]
            else:
                username = user.username
                name = user.name
                assigned_by = user.assigned_by

        except Exception as e:
            print(e)

        self.set_active = simplejson.dumps({
            "id": user.id,
            "rfid_uuid": user.rfid_uuid,
            "printer_name": user.printer_name,
            "username": username,
            "name": name,
            "last_access_date": str(date_time),
            "status": "Active",
            "assigned_by": assigned_by
        })
        print(self.set_active)
        try:
            self.login_request = requests.put(
                'http://localhost:8080/api/printers/'+str(user.id), self.set_active)
            print(self.login_request)
        except Exception as e:
            print(e)

    def logout(self, data):
        from .models import FabLabUser
        import requests
        import datetime

        today = datetime.datetime.now()
        date_time = today.strftime("%m-%d-%Y, %H:%M:%S")

        print('logout request start')

        try:
            if(data["_event"] == "PrintDone" or data["_event"] == "PrintCancelled"):
                logoutuser = FabLabUser.objects.get(username=data["owner"])
            else:
                logoutuser = FabLabUser.objects.get(
                    rfid_uuid=data["rfid_number"])
        except Exception as e:
            print(e)

        self.set_inactive = simplejson.dumps({
            "id": logoutuser.id,
            "rfid_uuid": logoutuser.rfid_uuid,
            "printer_name": logoutuser.printer_name,
            "username": logoutuser.username,
            "name": logoutuser.name,
            "last_access_date": str(date_time),
            "status": "Inactive",
            "assigned_by": logoutuser.assigned_by
        })
        print(self.set_inactive)

        try:
            self.logout_request = requests.put(
                'http://localhost:8080/api/printers/'+str(logoutuser.id), self.set_inactive)
            print(self.logout_request)
        except Exception as e:
            print(e)
        print('logout request end')

    def add_print_hours_maintenance(self, data):
        from .models import Maintenance, FabLabUser
        import requests

        print('maintenance request start')

        try:
            printer = FabLabUser.objects.get(
                username=data["owner"])
        except Exception as e:
            print(e)

        maintenance = Maintenance.objects.get(
            printer_name=printer.printer_name)

        print_time_hrs = data["time"]/3600

        self.add_print_hours = simplejson.dumps({
            "printer_name": maintenance.printer_name,
            "service_interval": maintenance.service_interval,
            "print_hours": maintenance.print_hours + int(print_time_hrs)
        })

        print(self.add_print_hours)
        try:
            self.maintenance_request = requests.put(
                'http://localhost:8080/api/maintenance', self.add_print_hours)
            print(self.maintenance_request)

        except Exception as e:
            print(e)

        print('maintenance request end')

    def add_usage(self, data):
        from .models import UsageData, PrinterUsage, OperatingUsage, FilamentUsage, FabLabUser
        import json
        import time
        import datetime
        from decimal import Decimal
        import requests

        try:
            printer_detail = FabLabUser.objects.get(username=data["owner"])
            if(printer_detail):
                printer_name = printer_detail.printer_name
            else:
                printer_name = "Other"
        except Exception as e:
            print(e)

        operating = OperatingUsage.objects.get(pk=1)
        printer = PrinterUsage.objects.get(pk=1)
        filament = FilamentUsage.objects.get(filament_name='Other')
        print_time = time.strftime("%H:%M:%S", time.gmtime(data["time"]))
        today = datetime.datetime.now()
        date_time = today.strftime("%m-%d-%Y, %H:%M:%S")
        print_time_hrs = data["time"]/3600
        print("variables initialised")

        AdditionCost = 0
        if(printer.lifespan > 0):
            depreciation_per_hour = printer.price_printer / printer.lifespan
        else:
            depreciation_per_hour = 0

        print("variables initialised2")
        FilamentCost = round(
            (filament.filament_price/filament.filament_weight) * Decimal(0), 2)
        print("variables initialised3")
        OperatingCost = round(
            (operating.power_consumption*operating.electricity_cost)*Decimal(print_time_hrs), 2)
        print("variables initialised4")
        PrinterCost = round(
            (depreciation_per_hour+printer.maintainence_cost) * Decimal(print_time_hrs), 2)
        print("variables initialised5")
        TotalCost = round(FilamentCost+OperatingCost +
                          PrinterCost + Decimal(AdditionCost), 2)
        print("variables initialised6")
        print("calculation done")

        self.add_usage_detail = simplejson.dumps({
            "owner": data["owner"],
            "file_name": data["name"],
            "print_time": print_time,
            "time_stamp": date_time,
            "print_status": data["_event"],
            "printer_name": printer_name,
            "filament_price": filament.filament_price,
            "filament_name": filament.filament_name,
            "filament_weight": filament.filament_weight,
            "filament_used": "0.0",
            "filament_cost": FilamentCost,
            "operating_cost": OperatingCost,
            "printer_cost": PrinterCost,
            "additional_cost": AdditionCost,
            "total_cost": TotalCost
        })

        try:
            self.usage_request = requests.post(
                'http://localhost:8080/api/usage', self.add_usage_detail)
            print(self.usage_request)
        except Exception as e:
            print(e)

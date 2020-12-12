# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import paho.mqtt.client as mqtt
import threading
from rest_framework.parsers import JSONParser
import simplejson
import time


MQTT_HOST = '52.57.250.120'
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
                [("OctPrintEvent/PrintDone", 2), ("OctPrintEvent/PrintStarted", 2), ("OctPrintEvent/PrintCancelled", 2)])  # change it for testing in real time

    def on_mqtt_disconnect(self, client, userdata, rc):
        self.mqttc.reconnect()
        if rc != 0:
            print("MQTT connection lost ...")

    def on_mqtt_message(self, client, userdata, msg):
        import json
        print("MQTT Nachricht empfangen" + msg.topic +
              " " + msg.payload.decode('UTF-8'))
        try:
            topic = msg.topic.split('/')
            data = json.loads(msg.payload.decode('UTF-8'))
            print(topic)
            print(data)

            if(data["_event"] == "PrintCancelled"):
                print("Logout event received")
                self.logout(data)
            elif(data["_event"] == "PrintDone"):
                self.add_usage(data)
                self.add_print_hours_maintenance(data)
                self.logout(data)
            elif(data["_event"] == "PrintStarted"):
                print("print start event received")
                self.login(data)

        except Exception as e:
            print(e)

    # Make the printer status active
    def login(self, data):
        from .models import FabLabUser
        from datetime import datetime as dt
        import time

        print('login start')

        # changing status of printer to Active
        # change names
        try:
            # If user starts a print from OctPrintEvent change status to Active
            if(data["_event"] == "PrintStarted"):
                login_user = FabLabUser.objects.get(username=data["owner"])
                if login_user:
                    login_user.username = data["owner"]
                    login_user.name = data["owner"]
                    login_user.assigned_by = data["owner"]
                    login_time = dt.fromtimestamp(data["_timestamp"])
                    login_user.last_access_date = login_time.strftime(
                        '%d-%m-%Y %H:%M:%S')
                    login_user.status = "Active"
                    print(login_user)
                    login_user.save()
                    print("login end")
                else:
                    login_user.status = "Active"
                    login_time = dt.fromtimestamp(data["_timestamp"])
                    login_user.last_access_date = login_time.strftime(
                        '%d-%m-%Y %H:%M:%S')
                    print(login_user)
                    login_user.save()
                    print("login end")

        except Exception as e:
            print(e)

    # Make the printer status inactive
    # change names
    def logout(self, data):
        from .models import FabLabUser
        from datetime import datetime as ldt
        import time

        print('logout request start')

        # changing status of printer to Inactive
        try:
            # If user ends a print from OctPrintEvent status change to Inactive
            if(data["_event"] == "PrintDone" or data["_event"] == "PrintCancelled"):
                logout_user = FabLabUser.objects.get(username=data["owner"])
                logout_user.status = "Inactive"
                logout_time = ldt.fromtimestamp(data["_timestamp"])
                logout_user.last_access_date: logout_time.strftime(
                    '%d-%m-%Y %H:%M:%S')
                print(logout_user)
                logout_user.save()
                print('logout request end')

        except Exception as e:
            print(e)

    # Add maintenance details by summing the print hours

    def add_print_hours_maintenance(self, data):
        from .models import Maintenance, FabLabUser
        from decimal import Decimal

        print('maintenance request start')

        # get the printer name which is assigned to the user
        try:
            printer = FabLabUser.objects.get(
                username=data["owner"])
        except Exception as e:
            print(e)

        maintenance = Maintenance.objects.get(
            printer_name=printer.printer_name)
        print_time_hrs = data["time"]/3600
        # Add the print time to the total print hours of the printer
        maintenance.print_hours = maintenance.print_hours + \
            Decimal(print_time_hrs)

        try:
            print(maintenance)
            maintenance.save()
            print('maintenance request end')
        except Exception as e:
            print(e)

    # Add usage details of the print once it is Done.
    def add_usage(self, data):
        from .models import UsageData, Printer, Operating, Filament, FabLabUser
        import json
        from datetime import datetime
        from decimal import Decimal
        import time

        try:
            printer_detail = FabLabUser.objects.get(username=data["owner"])
            if(printer_detail):
                printer_name = printer_detail.printer_name
            else:
                printer_name = "Other"
        except Exception as e:
            print(e)

        operating = Operating.objects.get(printer_name=printer_name)
        printer = Printer.objects.get(printer_name=printer_name)
        filament = Filament.objects.get(filament_name='Other')
        print_time = time.strftime("%H:%M:%S", time.gmtime(data["time"]))
        done_time = datetime.fromtimestamp(data["_timestamp"])
        timestamp = done_time.strftime('%d-%m-%Y %H:%M:%S')
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

        add_usage_detail = UsageData(
            owner=data["owner"],
            file_name=data["name"],
            print_time=print_time,
            time_stamp=timestamp,
            print_status=data["_event"],
            printer_name=printer_name,
            filament_price=filament.filament_price,
            filament_name=filament.filament_name,
            filament_weight=filament.filament_weight,
            filament_used=Decimal('0.00'),
            filament_cost=FilamentCost,
            operating_cost=OperatingCost,
            printer_cost=PrinterCost,
            additional_cost=AdditionCost,
            total_cost=TotalCost
        )

        try:
            print(add_usage_detail)
            add_usage_detail.save()
            print("usage added")

        except Exception as e:
            print(e)

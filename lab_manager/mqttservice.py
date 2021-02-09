# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import paho.mqtt.client as mqtt
import threading
from rest_framework.parsers import JSONParser
import simplejson
import time


# WARNING add credentials
# WARNING add MQTT Host
MQTT_HOST = ''
MQTT_PORT = 1883
# WARNING add credentials
MQTT_USER = ''
MQTT_PASS = ''

# Topics
# OctoPrintEvent/PrintDone no-retain subscribe
# OctoPrintEvent/PrintStarted no-retain subscribe
# OctoPrintEvent/PrintCancelled no-retain subscribe

# json message
# {'cmd':'command','data':'information'}


class mqttserviceThread(threading.Thread):

    def __init__(self, event):
        threading.Thread.__init__(self)
        self.stop_event = event
        self.mqttc = None

    def run(self):
        print("Start mqttservice Thread, wait for Django ....")
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
                [("OctoPrintEvent/PrintDone", 2), ("OctoPrintEvent/PrintStarted", 2), ("OctoPrintEvent/PrintCancelled", 2)])

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

            # When print is cancelled event received from octoprint then logout the user
            if(data["_event"] == "PrintCancelled"):
                print("Logout event received")
                self.logout(data)
            # When print is done event received from octoprint then add the usage, login the user, update the maintenance details
            elif(data["_event"] == "PrintDone"):
                self.add_usage(data)
                self.add_print_hours_maintenance(data)
                self.logout(data)
            # When print is started event received from octoprint then login the user
            elif(data["_event"] == "PrintStarted"):
                print("print start event received")
                self.login(data)

        except Exception as e:
            print(e)

    # Makes the printer status active
    def login(self, data):
        from .models import FabLabPrinter
        from datetime import datetime as dt
        import time

        print('login start')

        # changing status of printer to Active
        # change names
        try:
            # If user starts a print from OctoPrintEvent change status in app to Active
            if(data["_event"] == "PrintStarted"):
                try:
                    login_user = FabLabPrinter.objects.get(
                        username=data["owner"])
                    login_user.status = "Active"
                    login_time = dt.fromtimestamp(data["_timestamp"])
                    login_user.last_access_date = login_time.strftime(
                        '%d-%m-%Y %H:%M:%S')
                    print(login_user)
                    login_user.save()
                    print("login end")
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

    # Make the printer status inactive
    # change names
    def logout(self, data):
        from .models import FabLabPrinter
        from datetime import datetime as ldt
        import time

        print('logout request start')

        # changing status of printer to Inactive
        try:
            # If user ends a print from OctoPrintEvent status change in app to Inactive
            if(data["_event"] == "PrintDone" or data["_event"] == "PrintCancelled"):
                logout_user = FabLabPrinter.objects.get(username=data["owner"])
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
        from .models import Maintenance, FabLabPrinter
        from decimal import Decimal

        print('maintenance request start')

        # get the printer name which is assigned to the user
        try:
            printer = FabLabPrinter.objects.get(
                username=data["owner"])
        except Exception as e:
            print(e)

        maintenance = Maintenance.objects.get(
            printer_name=printer.printer_name)

        print_time_hrs = int(Decimal(data["time"]/3600))
        print(print_time_hrs)
        # Add the print time to the total print hours of the printer
        maintenance.print_hours = maintenance.print_hours + print_time_hrs

        try:
            print(maintenance)
            maintenance.save()
            print('maintenance request end')
        except Exception as e:
            print(e)

    # Add usage details of the print once it is Done.
    def add_usage(self, data):
        from .models import UsageData, Printer, Operating, Filament, FabLabPrinter, User
        import json
        from datetime import datetime
        from decimal import Decimal
        import time

        # get the printer details which is assigned to the user
        try:
            printer_detail = FabLabPrinter.objects.get(username=data["owner"])
            if(printer_detail):
                printer_name = printer_detail.printer_name
            else:
                printer_name = "Other"
        except Exception as e:
            print(e)

        operating = Operating.objects.get(printer_name=printer_name)
        printer = Printer.objects.get(printer_name=printer_name)
        filament = Filament.objects.get(filament_name='Other')
        # change format of timestamp to HH:MM:SS
        print_time = time.strftime("%H:%M:%S", time.gmtime(data["time"]))
        done_time = datetime.fromtimestamp(data["_timestamp"])
        timestamp = done_time.strftime('%d-%m-%Y %H:%M:%S')
        # Calculate print time to print hours
        print_time_hrs = data["time"]/3600

        if(printer.lifespan > 0):
            depreciation_per_hour = printer.price_printer / printer.lifespan
        else:
            depreciation_per_hour = 0

        # Calculating costs involved in each aspect
        # Filament Cost is set to 0 initially, this will be updated by operator in UI
        FilamentCost = round(
            (filament.filament_price/filament.filament_weight) * Decimal(0), 2)
        # Operating Cost is calculated based on power comsumption of printer, local electricity cost and print time
        OperatingCost = round(
            (operating.power_consumption*operating.electricity_cost)*Decimal(print_time_hrs), 2)
        # Printer Cost is based on depreciation_per_hour, maintenance cost of the printer and print time
        PrinterCost = round(
            (depreciation_per_hour+printer.maintainence_cost) * Decimal(print_time_hrs), 2)
        # Additional cost is Zero when usage detail is received, can be added from UI
        AdditionCost = 0
        TotalCost = round(FilamentCost+OperatingCost +
                          PrinterCost + Decimal(AdditionCost), 2)

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

        except Exception as e:
            print(e)

        # Storing usage details for each user
        try:
            # Find existing user
            user = User.objects.get(user=data["owner"])
            if(user):
                # If user found, add new cost details to user account usage
                user.last_access_date = timestamp
                user.operating_cost += OperatingCost
                user.printer_cost += PrinterCost
                user.print_hours += Decimal(print_time_hrs)
                user.filament_cost += FilamentCost
                user.total_cost += TotalCost
                try:
                    user.save()
                except Exception as e:
                    print(e)

        except Exception as e:
            print(e)
            # If user does't exist which means user is printing for the first time
            # Then, add details of the user and usage detail to user account
            add_usage_user = User(
                user=data["owner"],
                last_access_date=timestamp,
                print_hours=Decimal(print_time_hrs),
                filament_cost=FilamentCost,
                operating_cost=OperatingCost,
                printer_cost=PrinterCost,
                additional_cost=AdditionCost,
                total_cost=TotalCost)
            try:
                add_usage_user.save()
            except Exception as e:
                print(e)

from rest_framework import serializers
from lab_manager.models import FabLabUser, Printer, Filament, Operating, Maintenance, UsageData


class FabLabUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = FabLabUser
        fields = ('id',
                  'rfid_uuid',
                  'printer_name',
                  'username',
                  'name',
                  'last_access_date',
                  'status',
                  'assigned_by')


class MaintenanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Maintenance
        fields = ('id',
                  'printer_name',
                  'service_interval',
                  'print_hours')


class OperatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Operating
        fields = ('power_consumption',
                  'electricity_cost')


class FilamentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Filament
        fields = ('filament_name',
                  'filament_price',
                  'filament_weight')


class PrinterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Printer
        fields = ('price_printer',
                  'lifespan',
                  'maintainence_cost')


class UsageSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsageData
        fields = ('id',
                  'owner',
                  'file_name',
                  'print_time',
                  'time_stamp',
                  'print_status',
                  'printer_name',
                  'filament_name',
                  'filament_price',
                  'filament_weight',
                  'filament_used',
                  'filament_cost',
                  'operating_cost',
                  'printer_cost',
                  'additional_cost',
                  'total_cost')

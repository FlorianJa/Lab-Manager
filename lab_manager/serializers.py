from rest_framework import serializers
from lab_manager.models import FabLabUser, PrinterUsage, FilamentUsage, OperatingUsage, UsageData, Maintenance


class FabLabUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = FabLabUser
        fields = ('id',
                  'rfid_uuid',
                  'username',
                  'name',
                  'date_joined',
                  'is_login')


class MaintenanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Maintenance
        fields = ('printer_name',
                  'service_interval',
                  'total_hours',
                  'remaining_hours')


class OperatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = OperatingUsage
        fields = ('power_consumption',
                  'electricity_cost')


class FilamentSerializer(serializers.ModelSerializer):

    class Meta:
        model = FilamentUsage
        fields = ('filament_name',
                  'filament_price',
                  'filament_weight')


class PrinterSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrinterUsage
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

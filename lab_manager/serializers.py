from rest_framework import serializers
from lab_manager.models import FabLabPrinter, Printer, Filament, Operating, Maintenance, User, UsageData


# Django's serialization framework provides a mechanism for “translating” Django models into other formats.
# Serializer for FabLabPrinter model
class FabLabPrinterSerializer(serializers.ModelSerializer):

    class Meta:
        model = FabLabPrinter
        fields = ('id',
                  'rfid_uuid',
                  'printer_name',
                  'username',
                  'name',
                  'last_access_date',
                  'status',
                  'assigned_by')


# Serializer for User model
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('user',
                  'last_access_date',
                  'print_hours',
                  'filament_cost',
                  'operating_cost',
                  'printer_cost',
                  'additional_cost',
                  'total_cost')

# Serializer for Maintenance model


class MaintenanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Maintenance
        fields = ('id',
                  'printer_name',
                  'service_interval',
                  'print_hours')

# Serializer for Operating model


class OperatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Operating
        fields = ('id',
                  'printer_name',
                  'power_consumption',
                  'electricity_cost')

# Serializer for Filament model


class FilamentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Filament
        fields = ('filament_name',
                  'filament_price',
                  'filament_weight')

# Serializer for Printer model


class PrinterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Printer
        fields = ('id',
                  'printer_name',
                  'price_printer',
                  'lifespan',
                  'maintainence_cost')

# Serializer for UsageData model


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

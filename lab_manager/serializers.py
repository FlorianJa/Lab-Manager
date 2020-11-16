from rest_framework import serializers 
from lab_manager.models import FabLabUser, Material,Printer,Operating,UsageData
 
 
class FabLabUserSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = FabLabUser
        fields = ('id',
                  'rfid_uuid',
                  'username',
                  'name',
                  'date_joined',
                  'is_login')

class MaterialSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Material
        fields = ('filament_price',
                  'filament_weight',
                  'model_weight')

class OperatingSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Operating
        fields = ('power_consumption',
                  'electricity_cost')

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
                  'filament_price',
                  'filament_weight',
                  'model_weight',
                  'power_consumption',
                  'electricity_cost',
                  'price_printer',
                  'lifespan',
                  'maintainence_cost')
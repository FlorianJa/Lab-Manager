from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from lab_manager.models import FabLabUser, Printer, Operating, UsageData, Filament, Maintenance
from lab_manager.serializers import FabLabUserSerializer, FilamentSerializer, OperatingSerializer, PrinterSerializer, UsageSerializer, MaintenanceSerializer
from rest_framework.decorators import api_view

# Create your views here.

# To retreive user status with respect to RFID,Printer


@api_view(['GET', 'POST'])
def fablab_printers(request):
    if request.method == 'GET':
        users = FabLabUser.objects.all()
        user_serializer = FabLabUserSerializer(users, many=True)
        usage_serializer = UsageSerializer(usage)
        return JsonResponse(user_serializer.data, safe=False)
    elif request.method == 'POST':
        user_data = JSONParser().parse(request)
        fablabuser_serializer = FabLabUserSerializer(data=user_data)
        if fablabuser_serializer.is_valid():
            fablabuser_serializer.save()
            return JsonResponse(fablabuser_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(fablabuser_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# To change user,status with respect to RFID,Printer
@api_view(['PUT', 'GET'])
def fablab_printers_detail(request, pk):
    try:
        users = FabLabUser.objects.get(pk=pk)
    except FabLabUser.DoesNotExist:
        return JsonResponse({'message': 'The printer does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        fablabuser_serializer = FabLabUserSerializer(users)
        return JsonResponse(fablabuser_serializer.data, safe=False)
    if request.method == 'PUT':
        user_data = JSONParser().parse(request)
        fablabuser_serializer = FabLabUserSerializer(users, data=user_data)
        if fablabuser_serializer.is_valid():
            fablabuser_serializer.save()
            return JsonResponse(fablabuser_serializer.data)
        return JsonResponse(fablabuser_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# To manage default material usage details


@api_view(['GET', 'PUT'])
def filament_usage_default(request):
    if request.method == 'GET':
        filament = Filament.objects.all()
        filament_serializer = FilamentSerializer(filament, many=True)
        return JsonResponse(filament_serializer.data, safe=False)
    elif request.method == 'PUT':
        filament_data = JSONParser().parse(request)
        filament_serializer = FilamentSerializer(filament, data=filament_data)
        if filament_serializer.is_valid():
            filament_serializer.save()
            return JsonResponse(filament_serializer.data)
        return JsonResponse(filament_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# To manage default operating usage details


@api_view(['GET', 'PUT'])
def operating_usage_default(request):
    try:
        operating = Operating.objects.get(pk=1)
    except Operating.DoesNotExist:
        return JsonResponse({'message': 'The Operating usage default does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        operating = Operating.objects.all()
        operating_serializer = OperatingSerializer(operating, many=True)
        return JsonResponse(operating_serializer.data, safe=False)
    elif request.method == 'PUT':
        operating_data = JSONParser().parse(request)
        print(operating_data)
        operating_serializer = OperatingSerializer(
            operating, data=operating_data)
        if operating_serializer.is_valid():
            operating_serializer.save()
            return JsonResponse(operating_serializer.data)
        return JsonResponse(operating_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# To manage default printer usage details


@api_view(['GET', 'PUT'])
def printer_usage_default(request):
    try:
        printer = Printer.objects.get(pk=1)
    except Printer.DoesNotExist:
        return JsonResponse({'message': 'The Pinter usage default does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        printer = Printer.objects.all()
        printer_serializer = PrinterSerializer(printer, many=True)
        return JsonResponse(printer_serializer.data, safe=False)
    elif request.method == 'PUT':
        printer_data = JSONParser().parse(request)
        printer_serializer = PrinterSerializer(printer, data=printer_data)
        if printer_serializer.is_valid():
            printer_serializer.save()
            return JsonResponse(printer_serializer.data)
        return JsonResponse(printer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# To manage total usage details


@api_view(['GET', 'DELETE', 'POST'])
def usage(request):
    if request.method == 'GET':
        usage = UsageData.objects.all()
        usage_serializer = UsageSerializer(usage, many=True)
        return JsonResponse(usage_serializer.data, safe=False)
    elif request.method == 'DELETE':
        count = UsageData.objects.all().delete()
        return JsonResponse({'message': '{} Usage details were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'POST':
        usage_data = JSONParser().parse(request)
        usage_serializer = UsageSerializer(data=usage_data)
        if usage_serializer.is_valid():
            usage_serializer.save()
            return JsonResponse(usage_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(usage_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 # To manage each individual usage detail


# To manage default material usage details
@api_view(['GET', 'PUT'])
def maintenance(request):
    try:
        maintenance = Maintenance.objects.get(pk=1)
    except Maintenance.DoesNotExist:
        return JsonResponse({'message': 'The maintenance usage default does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        maintenance = Maintenance.objects.all()
        maintenance_serializer = MaintenanceSerializer(maintenance, many=True)
        return JsonResponse(maintenance_serializer.data, safe=False)
    elif request.method == 'PUT':
        maintenance_data = JSONParser().parse(request)
        maintenance_serializer = MaintenanceSerializer(
            maintenance, data=maintenance_data)
        if maintenance_serializer.is_valid():
            maintenance_serializer.save()
            return JsonResponse(maintenance_serializer.data)
        return JsonResponse(maintenance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def usage_detail(request, pk):
    try:
        usage = UsageData.objects.get(pk=pk)
    except UsageData.DoesNotExist:
        return JsonResponse({'message': 'UsageDetail does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        usage_serializer = UsageSerializer(usage)
        return JsonResponse(usage_serializer.data)
    elif request.method == 'PUT':
        usage_data = JSONParser().parse(request)
        usage_serializer = UsageSerializer(usage, data=usage_data)
        if usage_serializer.is_valid():
            usage_serializer.save()
            return JsonResponse(usage_serializer.data)
        return JsonResponse(usage_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        usage.delete()
        return JsonResponse({'message': 'usage detail was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

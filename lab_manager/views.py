from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from lab_manager.models import FabLabPrinter, Printer, Operating, UsageData, Filament, Maintenance, User
# Django's serialization framework provides a mechanism for “translating” Django models into other formats.
from lab_manager.serializers import FabLabPrinterSerializer, FilamentSerializer, OperatingSerializer, PrinterSerializer, UsageSerializer, MaintenanceSerializer, UserSerializer


# To retreive/add Printers details available in Lab
@api_view(['GET', 'POST'])
def fablab_printers(request):
    if request.method == 'GET':
        fablabprinter = FabLabPrinter.objects.all()
        fablabprinter_serializer = FabLabPrinterSerializer(
            fablabprinter, many=True)
        return JsonResponse(fablabprinter_serializer.data, safe=False)
    elif request.method == 'POST':
        fablabprinter_data = JSONParser().parse(request)
        fablabprinter_serializer = FabLabPrinterSerializer(
            data=fablabprinter_data)
        if fablabprinter_serializer.is_valid():
            fablabprinter_serializer.save()
            return JsonResponse(fablabprinter_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(fablabprinter_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# To assign a Printer to user
@api_view(['PUT', 'GET'])
def fablab_printers_detail(request, pk):
    try:
        fablabprinter = FabLabPrinter.objects.get(pk=pk)
    except users.DoesNotExist:
        return JsonResponse({'message': 'The printer does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        fablabprinter_serializer = FabLabPrinterSerializer(fablabprinter)
        return JsonResponse(fablabprinter_serializer.data, safe=False)
    if request.method == 'PUT':
        fablabprinter_data = JSONParser().parse(request)
        fablabprinter_serializer = FabLabPrinterSerializer(
            fablabprinter, data=fablabprinter_data)
        if fablabprinter_serializer.is_valid():
            fablabprinter_serializer.save()
            return JsonResponse(fablabprinter_serializer.data)
        return JsonResponse(fablabprinter_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# To get overall usage details by all users


@api_view(['GET'])
def user(request):
    if request.method == 'GET':
        user = User.objects.all()
        user_serializer = UserSerializer(user, many=True)
        return JsonResponse(user_serializer.data, safe=False)


# To manage usage details of each individual user
@api_view(['PUT', 'GET'])
def user_detail(request, slug):
    try:
        user = User.objects.get(user=slug)
    except user.DoesNotExist:
        return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        user_serializer = UserSerializer(user)
        return JsonResponse(user_serializer.data, safe=False)
    if request.method == 'PUT':
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data)
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# To manage total usage details for printers
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


# To manage usage detail based on each usage item
@api_view(['GET', 'PUT', 'DELETE'])
def usage_detail(request, pk):
    try:
        usage = UsageData.objects.get(pk=pk)
    except UsageData.DoesNotExist:
        return JsonResponse({'message': 'Usage detail does not exist'}, status=status.HTTP_404_NOT_FOUND)
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


# To get available filaments details
@api_view(['GET'])
def filament_usage(request):
    if request.method == 'GET':
        filament = Filament.objects.all()
        filament_serializer = FilamentSerializer(filament, many=True)
        return JsonResponse(filament_serializer.data, safe=False)


# To manage default filament usage details
@api_view(['GET', 'PUT'])
def filament_usage_default(request, slug):
    try:
        filament_detail = Filament.objects.get(filament_name=slug)
    except filament.DoesNotExist:
        return JsonResponse({'message': 'The default filament detail does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        filament_serializer = FilamentSerializer(filament_detail)
        return JsonResponse(filament_serializer.data, safe=False)
    elif request.method == 'PUT':
        filament_data = JSONParser().parse(request)
        filament_serializer = FilamentSerializer(
            filament_detail, data=filament_data)
        if filament_serializer.is_valid():
            filament_serializer.save()
            return JsonResponse(filament_serializer.data)
        return JsonResponse(filament_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# To manage default operating usage details
@api_view(['GET', 'PUT'])
def operating_usage_default(request, pk):
    try:
        operating = Operating.objects.get(pk=pk)
    except Operating.DoesNotExist:
        return JsonResponse({'message': 'Default Operating usage detail does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        operating_serializer = OperatingSerializer(operating)
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
def printer_usage_default(request, pk):
    try:
        printer = Printer.objects.get(pk=pk)
    except Printer.DoesNotExist:
        return JsonResponse({'message': 'The default Pinter usage detail does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        printer_serializer = PrinterSerializer(printer)
        return JsonResponse(printer_serializer.data, safe=False)
    elif request.method == 'PUT':
        printer_data = JSONParser().parse(request)
        printer_serializer = PrinterSerializer(printer, data=printer_data)
        if printer_serializer.is_valid():
            printer_serializer.save()
            return JsonResponse(printer_serializer.data)
        return JsonResponse(printer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# To manage default material usage details
@api_view(['GET', 'PUT'])
def maintenance(request, pk):
    try:
        maintenance = Maintenance.objects.get(pk=pk)
    except Maintenance.DoesNotExist:
        return JsonResponse({'message': 'The default maintenance usage detail does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        maintenance_serializer = MaintenanceSerializer(maintenance)
        return JsonResponse(maintenance_serializer.data, safe=False)
    elif request.method == 'PUT':
        maintenance_data = JSONParser().parse(request)
        maintenance_serializer = MaintenanceSerializer(
            maintenance, data=maintenance_data)
        if maintenance_serializer.is_valid():
            maintenance_serializer.save()
            return JsonResponse(maintenance_serializer.data)
        return JsonResponse(maintenance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

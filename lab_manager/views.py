from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from lab_manager.models import FabLabUser,Material,Printer,Operating,UsageData
from lab_manager.serializers import FabLabUserSerializer,MaterialSerializer,OperatingSerializer,PrinterSerializer,UsageSerializer
from rest_framework.decorators import api_view

# Create your views here.

#To manage users with respect to RFID
@api_view(['GET', 'POST', 'DELETE'])
def user_list(request):
    if request.method == 'GET':
        users = FabLabUser.objects.all()
        username = request.GET.get('username', None)
        if username is not None:
            users = users.filter(username__icontains=username)
        fablabuser_serializer = FabLabUserSerializer(users, many=True)
        return JsonResponse(fablabuser_serializer.data, safe=False)
    elif request.method == 'POST':
        user_data = JSONParser().parse(request)
        fablabuser_serializer = FabLabUserSerializer(data=user_data)
        if fablabuser_serializer.is_valid():
            fablabuser_serializer.save()
            return JsonResponse(fablabuser_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(fablabuser_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = FabLabUser.objects.all().delete()
        return JsonResponse({'message': '{} Users were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


#To change login status
@api_view(['PUT'])
def user_list_detail(request,pk):
    try: 
        user = FabLabUser.objects.get(rfid_uuid=pk)
    except FabLabUser.DoesNotExist: 
        return JsonResponse({'message': 'The User does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'PUT': 
        user_data = JSONParser().parse(request) 
        fablabuser_serializer = FabLabUserSerializer(user, data=user_data) 
        if fablabuser_serializer.is_valid(): 
            fablabuser_serializer.save() 
            return JsonResponse(fablabuser_serializer.data) 
        return JsonResponse(fablabuser_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#To manage default material usage details
@api_view(['GET', 'PUT'])
def material_usage_default(request):
    try: 
        material = Material.objects.get(pk=1)
    except Material.DoesNotExist: 
        return JsonResponse({'message': 'The Material usage default does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET':
        material = Material.objects.all()
        material_serializer = MaterialSerializer(material, many=True)
        return JsonResponse(material_serializer.data, safe=False)
    elif request.method == 'PUT': 
        material_data = JSONParser().parse(request) 
        material_serializer = MaterialSerializer(material, data=material_data) 
        if material_serializer.is_valid(): 
            material_serializer.save() 
            return JsonResponse(material_serializer.data) 
        return JsonResponse(material_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#To manage default operating usage details
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
        operating_serializer = OperatingSerializer(operating, data=operating_data) 
        if operating_serializer.is_valid(): 
            operating_serializer.save() 
            return JsonResponse(operating_serializer.data) 
        return JsonResponse(operating_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

#To manage default printer usage details
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

#To manage total usage details
@api_view(['GET','DELETE','POST'])
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
    
 #To manage each individual usage detail
@api_view(['GET','PUT','DELETE'])
def usage_detail(request,pk):
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
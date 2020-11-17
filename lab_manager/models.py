from django.db import models

# Create your models here.

#Model for mapping user detail with RFID
class FabLabUser(models.Model):
    rfid_uuid = models.CharField(max_length=14, unique=True, verbose_name='RFID UUID')
    username = models.CharField(max_length=14, unique=True)
    name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_login = models.BooleanField(verbose_name='Active', default=False)
    
    def __str__(self):
        return "(%r, %r, %r)" % (self.username, self.rfid_uuid, self.is_login)

#Model for storing default material usage
class MaterialUsage(models.Model):
    class Meta:
        abstract = True
    filament_price = models.DecimalField(max_digits=10, decimal_places=2)
    filament_weight = models.DecimalField(max_digits=10, decimal_places=2)
    model_weight = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return "(%r, %r, %r, %r)" % (self.id, self.filament_price, self.filament_weight, self.model_weight)
    
#Model for storing default operating usage
class OperatingUsage(models.Model):
    class Meta:
        abstract = True
    power_consumption = models.DecimalField(max_digits=10, decimal_places=2)
    electricity_cost = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return "(%r, %r)" % (self.power_consumption, self.electricity_cost)

#Model for storing default printer usage    
class PrinterUsage(models.Model):
    class Meta:
        abstract = True
    price_printer = models.DecimalField(max_digits=10, decimal_places=2)
    lifespan = models.DecimalField(max_digits=10, decimal_places=2)
    maintainence_cost = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return "(%r, %r, %r)" % (self.price_printer, self.lifespan, self.maintainence_cost)


class Material(MaterialUsage):
    pass

class Operating(OperatingUsage):
    pass

class Printer(PrinterUsage):
    pass

#Model for storing usage details all together including Material,Operating,Printer usage details   
class UsageData(MaterialUsage,OperatingUsage,PrinterUsage):
    owner = models.CharField(max_length=14)
    file_name = models.CharField(max_length=50)
    print_time = models.DecimalField(max_digits=15, decimal_places=3)
    time_stamp = models.BigIntegerField()
    print_status=models.CharField(max_length=14)
    printer_name =models.CharField(max_length=14)
    
    def __str__(self):
        return "(%r, %r, %r, %r, %r, %r)" % (self.owner, self.print_status,self.file_name,self.print_time,self.time_stamp,self.printer_name)
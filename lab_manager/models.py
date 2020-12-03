from django.db import models
from decimal import Decimal
# Create your models here.

# Model for mapping user detail with RFID


class FabLabUser(models.Model):

    rfid_uuid = models.CharField(
        max_length=14, unique=True, verbose_name='RFID UUID')
    username = models.CharField(max_length=14, unique=True)
    name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    # naming
    is_login = models.BooleanField(verbose_name='Active', default=False)

    def __str__(self):
        return "(%r, %r, %r)" % (self.username, self.rfid_uuid, self.is_login)

# Model for storing default Maintenance details


class Maintenance(models.Model):

    printer_name = models.CharField(max_length=14, unique=True)
    service_interval = models.PositiveSmallIntegerField()
    total_hours = models.PositiveSmallIntegerField()
    remaining_hours = models.PositiveSmallIntegerField()

    def __str__(self):
        return "(%r, %r, %r, %r)" % (self.service_interval, self.total_hours, self.remaining_hours, self.printer_name)


# Model for storing default Materials usage
class FilamentUsage(models.Model):

    filament_name = models.CharField(max_length=14, unique=True)
    filament_price = models.DecimalField(max_digits=10, decimal_places=2)
    filament_weight = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return "(%r, %r, %r)" % (self.filament_name, self.filament_price, self.filament_weight)

# Model for storing default operating usage


class OperatingUsage(models.Model):

    power_consumption = models.DecimalField(max_digits=10, decimal_places=2)
    electricity_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return "(%r, %r)" % (self.power_consumption, self.electricity_cost)

# Model for storing default printer usage


class PrinterUsage(models.Model):

    price_printer = models.DecimalField(max_digits=10, decimal_places=2)
    lifespan = models.PositiveSmallIntegerField()
    maintainence_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return "(%r, %r, %r)" % (self.price_printer, self.lifespan, self.maintainence_cost)

# Model for storing usage details all together including Material,Operating,Printer usage details


class UsageData(models.Model):

    owner = models.CharField(max_length=14)
    file_name = models.CharField(max_length=100)
    print_time = models.CharField(max_length=10)
    time_stamp = models.CharField(max_length=20, unique=True)
    print_status = models.CharField(max_length=14)
    printer_name = models.CharField(max_length=14)
    filament_name = models.CharField(max_length=14)
    filament_price = models.DecimalField(max_digits=10, decimal_places=2)
    filament_weight = models.DecimalField(max_digits=10, decimal_places=2)
    filament_used = models.DecimalField(max_digits=10, decimal_places=2)
    filament_cost = models.DecimalField(max_digits=10, decimal_places=2)
    operating_cost = models.DecimalField(max_digits=10, decimal_places=2)
    printer_cost = models.DecimalField(max_digits=10, decimal_places=2)
    additional_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        filament_cost = round(
            (self.filament_price/self.filament_weight)*self.filament_used, 2)
        total_cost = round(self.filament_cost + self.operating_cost +
                           self.printer_cost + self.additional_cost, 2)
        super(UsageData, self).save(*args, **kwargs)

    def __str__(self):
        return "(%r, %r, %r, %r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r)" % (self.owner, self.print_status, self.file_name, self.time_stamp, self.print_status, self.printer_name, self.filament_price, self.filament_used, self.filament_weight, self.filament_cost, self.printer_cost, self.operating_cost, self.additional_cost, self.total_cost)

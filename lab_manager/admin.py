from django.contrib import admin

# Register your models here.
from .models import FabLabUser, OperatingUsage, PrinterUsage, UsageData, FilamentUsage, Maintenance

admin.site.site_header = "Lab-Manager Admin"
admin.site.site_title = "Lab-Manager Admin Area"
admin.site.index_title = "Welcome to the Lab-Manager Admin area"

admin.site.register(FabLabUser)
admin.site.register(FilamentUsage)
admin.site.register(OperatingUsage)
admin.site.register(PrinterUsage)
admin.site.register(UsageData)
admin.site.register(Maintenance)

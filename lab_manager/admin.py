from django.contrib import admin

# Register your models here.
from .models import FabLabPrinter, Operating, Printer, UsageData, Filament, Maintenance, User

admin.site.site_header = "Lab-Manager Admin"
admin.site.site_title = "Lab-Manager Admin Area"
admin.site.index_title = "Welcome to the Lab-Manager Admin area"

admin.site.register(FabLabPrinter)
admin.site.register(Filament)
admin.site.register(Operating)
admin.site.register(Printer)
admin.site.register(UsageData)
admin.site.register(Maintenance)
admin.site.register(User)

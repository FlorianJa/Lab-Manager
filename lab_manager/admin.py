from django.contrib import admin

# Register your models here.
from .models import FabLabUser,Material,Operating,Printer,UsageData

admin.site.site_header = "Lab-Manager Admin"
admin.site.site_title = "Lab-Manager Admin Area"
admin.site.index_title = "Welcome to the Lab-Manager Admin area"

admin.site.register(FabLabUser)
admin.site.register(Material)
admin.site.register(Operating)
admin.site.register(Printer)
admin.site.register(UsageData)

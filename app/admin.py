from django.contrib import admin

# Register your models here.
from app.models import Notice, Manufacture, Government, Repairshop, Insurance

admin.site.register(Manufacture)
admin.site.register(Government)
admin.site.register(Repairshop)
admin.site.register(Insurance)
admin.site.register(Notice)
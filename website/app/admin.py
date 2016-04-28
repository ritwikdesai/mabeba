from django.contrib import admin
from app.models import  Account,SessionData,RequestQR
# Register your models here.
admin.site.register(Account)
admin.site.register(SessionData)
admin.site.register(RequestQR)
from django.contrib.admin.models import LogEntry
LogEntry.objects.all().delete()
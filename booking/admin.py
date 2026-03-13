from django.contrib import admin

# Register your models here.
from .models import Booking, Ticket

admin.site.register(Booking)
admin.site.register(Ticket)
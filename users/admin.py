from django.contrib import admin
from .models import UserProfile

admin.site.register(UserProfile)

admin.site.site_header = "Railway/Bus Ticket Booking System Admin"
admin.site.site_title = "Admin Login"
admin.site.index_title = "Welcome to Admin Panel"
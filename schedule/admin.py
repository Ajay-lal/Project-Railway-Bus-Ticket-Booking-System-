from django.contrib import admin
from .models import Vehicle, Route, Schedule, Coach

admin.site.register(Vehicle)
admin.site.register(Route)
admin.site.register(Schedule)
admin.site.register(Coach)
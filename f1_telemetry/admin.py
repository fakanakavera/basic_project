from django.contrib import admin
from .models import Header, CarMotion  # Adjust the import path according to your project structure

class HeaderAdmin(admin.ModelAdmin):
    list_display = ('sessionUID', 'sessionTime')  # Fields to display in the model list page
    search_fields = ('sessionUID',)

class CarMotionAdmin(admin.ModelAdmin):
    list_display = ('header', 'gForceLateral', 'gForceLongitudinal', 'gForceVertical', 'yaw', 'pitch', 'roll')  # Fields to display in the model list page

# Correctly register your models here
admin.site.register(Header, HeaderAdmin)
admin.site.register(CarMotion, CarMotionAdmin)
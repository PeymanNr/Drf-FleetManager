from django.contrib import admin
from django.contrib.admin import register
from tracking.models import Location


@register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('car_id', 'latitude', 'longitude', 'created_at')


# @register(Report)
# class ReportAdmin(admin.ModelAdmin):
#     list_display = ('location', )


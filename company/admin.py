from django.contrib import admin
from django.contrib.admin import register
from company.models import Company, Car


@register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'car_count')


@register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'company')

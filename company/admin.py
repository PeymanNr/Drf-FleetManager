from django.contrib import admin
from django.contrib.admin import register
from company.models import Company, OTPCode, Car


@register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'car_count')


@register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'sent_at', 'last_sent_at', "is_expired", "is_used", "user")


@register(Car)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company',)

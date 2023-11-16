from django.contrib import admin
from django.contrib.admin import register
from accounts.models import User


@register(User)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'is_active')

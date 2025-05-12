from django.contrib import admin
from .models import *
# Register your models here.

from django.contrib import admin
from .models import Profile

from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'mobile')

    def get_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

    get_name.short_description = "User"




from django.contrib import admin
from .models import CanteenStatus

@admin.register(CanteenStatus)
class CanteenStatusAdmin(admin.ModelAdmin):
    list_display = ('is_open', 'opening_time', 'closing_time')

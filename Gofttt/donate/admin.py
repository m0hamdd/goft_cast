from django.contrib import admin
from .models import Donate



# Register your models here.
@admin.register(Donate)
class DonateAdmin(admin.ModelAdmin):
    list_display = ['user', 'currency', 'amount', 'status', 'date']
    search_fields = ['amount', 'currency']
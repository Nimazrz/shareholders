from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import ShareholdersHistory


@admin.register(ShareholdersHistory)
class ShareholdersHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'shareholder_id')
    search_fields = ('id', 'date', 'shareholder_id', 'shareholder_shares', 'shareholder_percentage',
                     'shareholder_instrument_id', 'shareholder_name', 'change', 'symbol')

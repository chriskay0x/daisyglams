from django.contrib import admin
from .models import NailDesign, BusinessAccount

@admin.register(NailDesign)
class NailDesignAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'uploaded_at')
    list_filter = ('category',)
    search_fields = ('title',)

@admin.register(BusinessAccount)
class BusinessAccountAdmin(admin.ModelAdmin):
    list_display = ('bank_name', 'account_name', 'account_number')
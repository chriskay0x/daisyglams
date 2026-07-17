from django.contrib import admin
from .models import Service, Appointment

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'emoji', 'is_active')
    list_editable = ('is_active',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'service', 'preferred_date', 'preferred_time', 'status', 'created_at')
    list_filter = ('status', 'service')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_editable = ('status',)
    readonly_fields = ('created_at',)
    

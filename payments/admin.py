from django.contrib import admin
from .models import PaymentProof

@admin.register(PaymentProof)
class PaymentProofAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'sender_name', 'is_verified', 'submitted_at')
    list_filter = ('is_verified',)
    list_editable = ('is_verified',)
    readonly_fields = ('submitted_at',)
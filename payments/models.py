from django.db import models

# Create your models here.
from django.db import models
from bookings.models import Appointment

class PaymentProof(models.Model):
    appointment = models.OneToOneField(
        Appointment, on_delete=models.CASCADE, related_name='payment'
    )
    sender_name = models.CharField(max_length=100)
    receipt = models.ImageField(upload_to='receipts/')
    note = models.CharField(max_length=255, blank=True)
    is_verified = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.appointment}"
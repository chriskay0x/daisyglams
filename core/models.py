from django.db import models

# Create your models here.
from django.db import models

class NailDesign(models.Model):
    CATEGORY_CHOICES = [
        ('nail-art', 'Nail Art'),
        ('extensions', 'Extensions'),
        ('manicure', 'Manicure'),
        ('pedicure', 'Pedicure'),
        ('gel', 'Gel Polish'),
    ]

    title = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='designs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-uploaded_at']


class BusinessAccount(models.Model):
    bank_name = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.bank_name} — {self.account_number}"

    class Meta:
        verbose_name = "Business Account"
from django import forms
from .models import Appointment, Service

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'service', 'first_name', 'last_name',
            'email', 'phone', 'preferred_date',
            'preferred_time', 'notes', 'inspiration_image'
        ]
        widgets = {
            'preferred_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
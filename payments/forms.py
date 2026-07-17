from django import forms
from .models import PaymentProof

class PaymentProofForm(forms.ModelForm):
    class Meta:
        model = PaymentProof
        fields = ['sender_name', 'receipt', 'note']
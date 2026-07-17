from bookings.models import Appointment
from payments.models import PaymentProof

def dashboard_counts(request):
    if request.user.is_authenticated and request.user.is_staff:
        return {
            'pending_bookings_count': Appointment.objects.filter(status='pending').count(),
            'pending_payments_count': PaymentProof.objects.filter(is_verified=False).count(),
        }
    return {}
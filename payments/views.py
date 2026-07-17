from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from bookings.models import Appointment
from core.models import BusinessAccount
from .models import PaymentProof
from .forms import PaymentProofForm

def payment(request):
    appointment_id = request.session.get('appointment_id')
    appointment = None
    if appointment_id:
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            pass

    if not appointment:
        return redirect('bookings:booking')

    account = BusinessAccount.objects.first()

    if request.method == 'POST':
        form = PaymentProofForm(request.POST, request.FILES)
        if form.is_valid():
            proof = form.save(commit=False)
            proof.appointment = appointment
            proof.save()

            # Send email notification to admin
            try:
                send_mail(
                    subject=f'💳 New Payment Proof — {appointment.first_name} {appointment.last_name}',
                    message=f'''
New payment proof received!

Customer: {appointment.first_name} {appointment.last_name}
Service: {appointment.service}
Date: {appointment.preferred_date}
Time: {appointment.preferred_time}
Email: {appointment.email}
Phone: {appointment.phone}
Sender Name: {proof.sender_name}

Please log into the dashboard to verify:
http://127.0.0.1:8000/dashboard/payments/
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass

            return redirect('bookings:confirmation')

    else:
        form = PaymentProofForm()

    return render(request, 'payments/payment.html', {
        'appointment': appointment,
        'account': account,
        'form': form,
    })
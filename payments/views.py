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
        existing_proof = PaymentProof.objects.filter(appointment=appointment).first()
        form = PaymentProofForm(request.POST, request.FILES, instance=existing_proof)  # ✅ Pass instance

        if form.is_valid():
            proof = form.save(commit=False)
            proof.appointment = appointment
            proof.save()  # ✅ Properly saves file to disk

            dashboard_url = request.build_absolute_uri('/dashboard/payments/')

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
{dashboard_url}
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
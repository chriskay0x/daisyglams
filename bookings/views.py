from django.shortcuts import render, redirect
from .models import Service, Appointment
from .forms import AppointmentForm

def booking(request):
    services = Service.objects.filter(is_active=True)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, request.FILES)
        if form.is_valid():
            appointment = form.save()
            request.session['appointment_id'] = appointment.id
            return redirect('payments:payment')
    else:
        form = AppointmentForm()
    return render(request, 'bookings/booking.html', {
        'form': form,
        'services': services,
    })

def confirmation(request):
    appointment_id = request.session.get('appointment_id')
    appointment = None
    if appointment_id:
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            pass
    progress_steps = ['Booked', 'Paid', 'Proof Sent', 'Confirming']
    return render(request, 'bookings/confirmation.html', {
        'appointment': appointment,
        'progress_steps': progress_steps,
    })
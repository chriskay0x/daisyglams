from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator

from bookings.models import Appointment, Service
from payments.models import PaymentProof
from core.models import NailDesign, BusinessAccount


def dashboard_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard:overview')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('dashboard:overview')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    return render(request, 'dashboard/login.html')


def dashboard_logout(request):
    logout(request)
    return redirect('dashboard:login')


@login_required(login_url='/dashboard/login/')
def overview(request):
    context = {
        'total_bookings': Appointment.objects.count(),
        'pending_bookings': Appointment.objects.filter(status='pending').count(),
        'confirmed_bookings': Appointment.objects.filter(status='confirmed').count(),
        'pending_payments': PaymentProof.objects.filter(is_verified=False).count(),
        'recent_bookings': Appointment.objects.all()[:5],
        'recent_payments': PaymentProof.objects.filter(is_verified=False)[:5],
    }
    return render(request, 'dashboard/overview.html', context)


@login_required(login_url='/dashboard/login/')
def bookings(request):
    status_filter = request.GET.get('status', 'all')
    all_bookings = Appointment.objects.all()
    if status_filter != 'all':
        all_bookings = all_bookings.filter(status=status_filter)

    statuses = [
        ('all', 'All'),
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    context = {
        'bookings': all_bookings,
        'active_filter': status_filter,
        'statuses': statuses,
    }
    
    return render(request, 'dashboard/bookings.html', context)


@login_required(login_url='/dashboard/login/')
def update_booking(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pending', 'confirmed', 'completed', 'cancelled']:
            appointment.status = new_status
            appointment.save()
            messages.success(request, f'Booking status updated to {new_status}.')
    return redirect('dashboard:bookings')


@login_required(login_url='/dashboard/login/')
def gallery(request):
    designs = NailDesign.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        if title and category and image:
            NailDesign.objects.create(title=title, category=category, image=image)
            messages.success(request, 'Design uploaded successfully!')
            return redirect('dashboard:gallery')
    return render(request, 'dashboard/gallery.html', {'designs': designs})


@login_required(login_url='/dashboard/login/')
def delete_design(request, pk):
    design = get_object_or_404(NailDesign, pk=pk)
    design.delete()
    messages.success(request, 'Design deleted.')
    return redirect('dashboard:gallery')


@login_required(login_url='/dashboard/login/')
def payments(request):
    all_payments = PaymentProof.objects.select_related('appointment').all()
    return render(request, 'dashboard/payments.html', {'payments': all_payments})


@login_required(login_url='/dashboard/login/')
def verify_payment(request, pk):
    proof = get_object_or_404(PaymentProof, pk=pk)
    proof.is_verified = True
    proof.appointment.status = 'confirmed'
    proof.appointment.save()
    proof.save()
    messages.success(request, 'Payment verified and booking confirmed!')
    return redirect('dashboard:payments')


@login_required(login_url='/dashboard/login/')
def services(request):
    all_services = Service.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        emoji = request.POST.get('emoji', '💅')
        if name and price:
            Service.objects.create(
                name=name, description=description,
                price=price, emoji=emoji
            )
            messages.success(request, f'Service "{name}" added!')
            return redirect('dashboard:services')
    return render(request, 'dashboard/services.html', {'services': all_services})


@login_required(login_url='/dashboard/login/')
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    service.delete()
    messages.success(request, 'Service deleted.')
    return redirect('dashboard:services')


@login_required(login_url='/dashboard/login/')
def site_settings(request):
    account = BusinessAccount.objects.first()
    if request.method == 'POST':
        bank_name = request.POST.get('bank_name')
        account_name = request.POST.get('account_name')
        account_number = request.POST.get('account_number')
        whatsapp = request.POST.get('whatsapp_number', '')
        if account:
            account.bank_name = bank_name
            account.account_name = account_name
            account.account_number = account_number
            account.whatsapp_number = whatsapp
            account.save()
        else:
            BusinessAccount.objects.create(
                bank_name=bank_name,
                account_name=account_name,
                account_number=account_number,
                whatsapp_number=whatsapp,
            )
        messages.success(request, 'Settings updated successfully!')
        return redirect('dashboard:settings')
    return render(request, 'dashboard/settings.html', {'account': account})
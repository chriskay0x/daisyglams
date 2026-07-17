from django.shortcuts import render
from .models import NailDesign, BusinessAccount
from bookings.models import Service

def home(request):
    designs = NailDesign.objects.all()[:4]
    services = Service.objects.filter(is_active=True)
    return render(request, 'core/home.html', {
        'designs': designs,
        'services': services,
    })

def gallery(request):
    category = request.GET.get('category', 'all')
    designs = NailDesign.objects.all()
    if category != 'all':
        designs = designs.filter(category=category)

    categories = [
        ('all', 'All Designs'),
        ('nail-art', 'Nail Art'),
        ('extensions', 'Extensions'),
        ('manicure', 'Manicure'),
        ('pedicure', 'Pedicure'),
        ('gel', 'Gel Polish'),
    ]

    return render(request, 'core/gallery.html', {
        'designs': designs,
        'active_category': category,
        'categories': categories,
    })
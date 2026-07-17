from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.overview, name='overview'),
    path('login/', views.dashboard_login, name='login'),
    path('logout/', views.dashboard_logout, name='logout'),
    path('bookings/', views.bookings, name='bookings'),
    path('bookings/<int:pk>/update/', views.update_booking, name='update_booking'),
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/delete/<int:pk>/', views.delete_design, name='delete_design'),
    path('payments/', views.payments, name='payments'),
    path('payments/<int:pk>/verify/', views.verify_payment, name='verify_payment'),
    path('services/', views.services, name='services'),
    path('services/delete/<int:pk>/', views.delete_service, name='delete_service'),
    path('settings/', views.site_settings, name='settings'),
]
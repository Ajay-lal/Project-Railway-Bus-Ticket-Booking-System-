"""
URL configuration for railway_bus_ticket_booking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
URL configuration for railway_bus_ticket_booking project.
"""

from django.contrib import admin
from django.urls import path

# Users views
from users.views import home, register, login_user, logout_user, reset_password, dashboard

# Booking views
from booking.views import book_ticket, booking_history, cancel_ticket

# Payment views
from payment.views import payment_page, payment_success


urlpatterns = [

    # Admin panel
    path('admin/', admin.site.urls),

    # Home page
    path('', home, name='home'),

    # Booking
    path('book/<int:schedule_id>/', book_ticket, name='book_ticket'),
    path('bookings/', booking_history, name='booking_history'),
    path('cancel/<int:booking_id>/', cancel_ticket, name='cancel_ticket'),

    # Payment
    path('payment/<int:booking_id>/', payment_page, name='payment_page'),
    path('payment-success/<int:booking_id>/', payment_success, name='payment_success'),

    # User authentication
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('reset-password/', reset_password, name='reset_password'),

    # User dashboard
    path('dashboard/', dashboard, name='dashboard'),
]
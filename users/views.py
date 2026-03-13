from django.shortcuts import render, redirect
from schedule.models import Schedule
from notification.models import Notification
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from booking.models import Booking
from .models import UserProfile
from django.contrib import messages



@login_required
def dashboard(request):

    user = request.user

    profile = UserProfile.objects.filter(user=user).first()

    bookings = Booking.objects.filter(user=user)

    total_bookings = bookings.count()
    confirmed = bookings.filter(status="Confirmed").count()
    cancelled = bookings.filter(status="Cancelled").count()

    recent_bookings = bookings.order_by('-booking_date')[:5]

    return render(request, "dashboard.html", {
        "profile": profile,
        "total_bookings": total_bookings,
        "confirmed": confirmed,
        "cancelled": cancelled,
        "recent_bookings": recent_bookings
    })

def home(request):

    source = request.GET.get('source')
    destination = request.GET.get('destination')

    schedules = None

    if source and destination:
        schedules = Schedule.objects.filter(
            route__source__icontains=source,
            route__destination__icontains=destination
        )

    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
    else:
        notifications = []

    return render(request, 'home.html', {
        'schedules': schedules ,
        'notificationS' : notifications                        
    })


def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        gender = request.POST.get("gender")
        dob = request.POST.get("dob")
        aadhaar = request.POST.get("aadhaar")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose another.")
            return redirect("register")

        # Aadhaar validation
        if len(aadhaar) != 12 or not aadhaar.isdigit():
            messages.error(request, "Aadhaar must be 12 digits")
            return redirect("register")

        # Create user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        # Create profile
        UserProfile.objects.create(
            user=user,
            phone=phone,
            gender=gender,
            email=email,
            date_of_birth=dob,
            aadhaar_number=aadhaar
        )

        messages.success(request, "Registration successful! Please login.")

        return redirect("login")

    return render(request, "register.html")




def login_user(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            next_url = request.GET.get('next')

            if next_url:
                return redirect(next_url)
            else:
                return redirect('dashboard')

    return render(request, "login.html")




def logout_user(request):

    logout(request)

    return redirect("login")



def reset_password(request):

    if request.method == "POST":

        username = request.POST.get("username")
        new_password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)

            user.password = make_password(new_password)

            user.save()

            return redirect("login")

        except User.DoesNotExist:

            return render(request, "reset_password.html", {
                "error": "User not found"
            })

    return render(request, "reset_password.html")
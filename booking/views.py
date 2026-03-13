

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from schedule.models import Schedule, Coach
from .models import Booking, Passenger
from notification.models import Notification
import random


# =====================================================
# BOOK TICKET VIEW
# =====================================================
@login_required
def book_ticket(request, schedule_id):

    # Get selected schedule
    schedule = Schedule.objects.get(id=schedule_id)

    # Get coach selected from URL
    coach_id = request.GET.get("coach")

    if not coach_id:
        return redirect("home")

    coach = Coach.objects.get(id=coach_id)

    vehicle_type = schedule.vehicle.vehicle_type

    seat_list = []

    # =====================================================
    # TRAIN SEAT GENERATION
    # =====================================================
    if vehicle_type == "Train":

        rows = ["A", "B", "C", "D", "E", "F"]

        seat_count = coach.total_seats

        row_index = 0
        number = 1

        while len(seat_list) < seat_count:

            row = rows[row_index]
            seat_list.append(f"{row}{number}")

            row_index += 1

            if row_index == len(rows):
                row_index = 0
                number += 1

    # =====================================================
    # BUS SEAT GENERATION
    # =====================================================
    elif vehicle_type == "Bus":

        seat_count = coach.total_seats

        for i in range(1, seat_count + 1):
            seat_list.append(f"B{i}")

    # =====================================================
    # GET BOOKED SEATS (ONLY CONFIRMED BOOKINGS)
    # =====================================================
    booked_seats = Passenger.objects.filter(
        booking__schedule=schedule,
        booking__coach=coach,
        booking__status="Confirmed"
    ).values_list("seat_number", flat=True)


    # =====================================================
    # HANDLE BOOKING FORM
    # =====================================================
    if request.method == "POST":

        seats = request.POST.get("seat_number")

        passenger_names = request.POST.getlist("passenger_name[]")
        phones = request.POST.getlist("phone[]")
        dobs = request.POST.getlist("dob[]")
        aadhaars = request.POST.getlist("aadhaar[]")

        if not seats:

            return render(request, "book_ticket.html", {
                "schedule": schedule,
                "coach": coach,
                "seat_list": seat_list,
                "booked_seats": booked_seats,
                "error": "Please select seats."
            })

        seat_list_selected = seats.split(",")

        # =====================================================
        # LIMIT SEATS (MAX 5)
        # =====================================================
        if len(seat_list_selected) > 5:

            return render(request, "book_ticket.html", {
                "schedule": schedule,
                "coach": coach,
                "seat_list": seat_list,
                "booked_seats": booked_seats,
                "error": "Maximum 5 seats allowed per booking."
            })

        # =====================================================
        # CHECK IF SEAT ALREADY BOOKED
        # =====================================================
        for seat in seat_list_selected:

            if seat in booked_seats:

                return render(request, "book_ticket.html", {
                    "schedule": schedule,
                    "coach": coach,
                    "seat_list": seat_list,
                    "booked_seats": booked_seats,
                    "error": f"Seat {seat} already booked."
                })

        # =====================================================
        # GENERATE PNR
        # =====================================================
        if vehicle_type == "Train":
            pnr = "TR" + str(random.randint(1000000000, 9999999999))
        else:
            pnr = "BS" + str(random.randint(10000000, 99999999))

        # =====================================================
        # CREATE BOOKING (PENDING UNTIL PAYMENT)
        # =====================================================
        booking = Booking.objects.create(
            user=request.user,
            schedule=schedule,
            coach=coach,
            pnr=pnr,
            status="Pending"
        )

        # =====================================================
        # CREATE PASSENGERS (SEATS TEMPORARY UNTIL PAYMENT)
        # =====================================================
        for i in range(len(seat_list_selected)):

            Passenger.objects.create(
                booking=booking,
                name=passenger_names[i],
                phone=phones[i],
                dob=dobs[i],
                aadhaar=aadhaars[i],
                seat_number=seat_list_selected[i]
            )

        # =====================================================
        # CREATE NOTIFICATION
        # =====================================================
        Notification.objects.create(
            user=request.user,
            message=f"Booking created. Complete payment to confirm ticket. PNR: {pnr}"
        )

        # Redirect to payment page
        return redirect("payment_page", booking_id=booking.id)


    # =====================================================
    # LOAD BOOKING PAGE
    # =====================================================
    return render(request, "book_ticket.html", {
        "schedule": schedule,
        "coach": coach,
        "seat_list": seat_list,
        "booked_seats": booked_seats
    })


# =====================================================
# BOOKING HISTORY
# =====================================================
@login_required
def booking_history(request):

    bookings = Booking.objects.filter(
        user=request.user
    ).order_by('-booking_date')

    return render(request, 'booking_history.html', {
        'bookings': bookings
    })


# =====================================================
# CANCEL TICKET
# =====================================================
@login_required
def cancel_ticket(request, booking_id):

    booking = Booking.objects.get(id=booking_id, user=request.user)

    booking.status = "Cancelled"
    booking.save()

    Notification.objects.create(
        user=request.user,
        message=f"Ticket for {booking.schedule.route} has been cancelled."
    )

    return redirect('booking_history')
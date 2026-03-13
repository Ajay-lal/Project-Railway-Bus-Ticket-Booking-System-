
from django.shortcuts import render, redirect
from .models import Payment
from booking.models import Booking, Passenger
from notification.models import Notification
from django.contrib.auth.decorators import login_required

import qrcode
from io import BytesIO
import base64
import random


# =====================================
# PAYMENT PAGE
# =====================================
@login_required
def payment_page(request, booking_id):

    booking = Booking.objects.get(id=booking_id)

    # Dummy ticket price
    amount = 500

    # Prevent duplicate payment
    existing_payment = Payment.objects.filter(
        booking=booking,
        payment_status="Completed"
    ).first()

    if existing_payment:
        return redirect("payment_success", booking_id=booking.id)

    if request.method == "POST":

        method = request.POST.get("method")

        payment = Payment.objects.create(
            booking=booking,
            amount=amount,
            payment_method=method,
            payment_status="Completed",
            payment_id="PAY" + str(random.randint(100000, 999999))
        )

        # ✅ Confirm booking only after payment
        booking.status = "Confirmed"
        booking.save()

        # Notification
        Notification.objects.create(
            user=request.user,
            message=f"Payment successful for {booking.schedule.route}"
        )

        return redirect("payment_success", booking_id=booking.id)

    return render(request, "payment.html", {
        "booking": booking,
        "amount": amount
    })


# =====================================
# PAYMENT SUCCESS → GENERATE TICKET
# =====================================
@login_required
def payment_success(request, booking_id):

    booking = Booking.objects.get(id=booking_id)

    # Only allow ticket if payment completed
    payment = Payment.objects.filter(
        booking=booking,
        payment_status="Completed"
    ).first()

    if not payment:
        return redirect("payment_page", booking_id=booking.id)

    # Get passengers
    passengers = Passenger.objects.filter(booking=booking)

    # Prepare seat list
    seat_list = ", ".join([p.seat_number for p in passengers])

    # QR DATA
    qr_data = f"""
    PNR: {booking.pnr}
    Vehicle: {booking.schedule.vehicle.vehicle_name}
    Route: {booking.schedule.route}
    Date: {booking.schedule.journey_date}
    Seats: {seat_list}
    """

    qr = qrcode.make(qr_data)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    qr_image = base64.b64encode(buffer.getvalue()).decode()

    return render(request, "ticket.html", {
        "booking": booking,
        "payment": payment,
        "passengers": passengers,
        "qr_image": qr_image
    })
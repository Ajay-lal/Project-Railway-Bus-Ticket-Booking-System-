from django.db import models
from django.contrib.auth.models import User
from schedule.models import Schedule, Coach


# -----------------------------------
# BOOKING MODEL (PNR LEVEL)
# -----------------------------------
class Booking(models.Model):

    STATUS_CHOICES = (
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled"),
        ("Pending", "Pending"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)

    # PNR NUMBER
    pnr = models.CharField(max_length=15, unique=True)

    booking_date = models.DateField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"PNR {self.pnr}"


# -----------------------------------
# PASSENGER MODEL (MULTIPLE PASSENGERS)
# -----------------------------------
class Passenger(models.Model):

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="passengers"
    )

    name = models.CharField(max_length=100)

    phone = models.CharField(max_length=10)

    aadhaar = models.CharField(max_length=12)

    dob = models.DateField()

    seat_number = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.name} - {self.seat_number}"


# -----------------------------------
# TICKET MODEL
# -----------------------------------
class Ticket(models.Model):

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)

    ticket_number = models.CharField(max_length=50, unique=True)

    issue_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket {self.ticket_number}"
from django.db import models
from booking.models import Booking


class Payment(models.Model):

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=8, decimal_places=2)

    payment_method = models.CharField(max_length=50)

    payment_status = models.CharField(max_length=20)

    payment_id = models.CharField(max_length=100)

    payment_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Payment {self.payment_id}"
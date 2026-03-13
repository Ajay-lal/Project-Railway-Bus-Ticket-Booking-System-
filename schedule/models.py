from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Vehicle(models.Model):

    VEHICLE_TYPE = (
        ("Train", "Train"),
        ("Bus", "Bus"),
    )

    vehicle_name = models.CharField(max_length=100)
    vehicle_number = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE)
    capacity = models.IntegerField()

    def __str__(self):
        return self.vehicle_name


class Route(models.Model):

    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source} → {self.destination}"


class Schedule(models.Model):

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    journey_date = models.DateField()
    running_days = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.vehicle} - {self.route}"


class Coach(models.Model):

    COACH_TYPE = (
        ("General", "General"),
        ("AC", "AC"),
        ("Non-AC", "Non-AC"),
        ("Sleeper", "Sleeper"),
        ("Sleeper 2 Tier", "Sleeper 2 Tier"),
        ("Sleeper 3 Tier", "Sleeper 3 Tier"),
    )

    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    coach_name = models.CharField(max_length=10)
    coach_type = models.CharField(max_length=20, choices=COACH_TYPE)

    total_seats = models.IntegerField()

    def __str__(self):
        return f"{self.schedule.vehicle.vehicle_name} - {self.coach_name} ({self.coach_type})"


# ---------- SIGNAL TO AUTO CREATE COACHES ----------

@receiver(post_save, sender=Schedule)
def create_coaches(sender, instance, created, **kwargs):

    if not created:
        return

    vehicle = instance.vehicle
    total_capacity = vehicle.capacity

    if vehicle.vehicle_type == "Train":

        ac_seats = int(total_capacity * 0.30)
        sleeper_seats = int(total_capacity * 0.50)
        general_seats = total_capacity - (ac_seats + sleeper_seats)

        Coach.objects.create(schedule=instance, coach_name="A1", coach_type="AC", total_seats=ac_seats)
        Coach.objects.create(schedule=instance, coach_name="S1", coach_type="Sleeper", total_seats=sleeper_seats)
        Coach.objects.create(schedule=instance, coach_name="GEN", coach_type="General", total_seats=general_seats)

    elif vehicle.vehicle_type == "Bus":

        ac_seats = int(total_capacity * 0.60)
        non_ac_seats = total_capacity - ac_seats

        Coach.objects.create(schedule=instance, coach_name="AC", coach_type="AC", total_seats=ac_seats)
        Coach.objects.create(schedule=instance, coach_name="NA", coach_type="Non-AC", total_seats=non_ac_seats)
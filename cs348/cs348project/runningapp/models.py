from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum

class User(AbstractUser):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    distance_miles = models.FloatField()
    time_minutes = models.FloatField()

    class Meta:
        abstract = True

    def pace(self):
        if self.distance_miles > 0:
            return self.time_minutes / self.distance_miles
        return 0

class Run(Activity):
    pass

class BikeRide(Activity):
    pass

class Swim(Activity):
    distance_meters = models.FloatField()

    def save(self, *args, **kwargs):
        self.distance_miles = self.distance_meters / 1609.34
        super().save(*args, **kwargs)

    def pace(self):
        if self.distance_meters > 0:
            return (self.time_minutes * 100) / self.distance_meters  # pace per 100 meters
        return 0
    



class Leaderboard:
    @staticmethod
    def get_leaderboard(start_date, end_date):
        users = User.objects.all()  # Adjust as necessary for filtering users

        leaderboard_data = []
        for user in users:
            total_distance = (
                (Run.objects.filter(user=user, date__range=[start_date, end_date])
                 .aggregate(total=Sum('distance_miles'))['total'] or 0) +
                (BikeRide.objects.filter(user=user, date__range=[start_date, end_date])
                 .aggregate(total=Sum('distance_miles'))['total'] or 0) +
                (Swim.objects.filter(user=user, date__range=[start_date, end_date])
                 .aggregate(total=Sum('distance_miles'))['total'] or 0)
            )
            leaderboard_data.append((user.username, total_distance))

        # Sort data by total distance in descending order
        leaderboard_data.sort(key=lambda x: x[1], reverse=True)
        return leaderboard_data
    
class ProgressReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    note = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.date_created.strftime('%Y-%m-%d')}"
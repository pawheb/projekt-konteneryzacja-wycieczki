from django.db import models
from enum import IntEnum

class City(models.Model):
    name = models.CharField(max_length=512, unique=True, default='unknown')

    def __str__(self):
        return self.name

class Trip(models.Model):
    name = models.CharField(max_length=512)
    cities = models.ManyToManyField(City, related_name='trips')  # Wycieczka może obejmować wiele miast
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    attractions = models.ManyToManyField('Attraction', related_name='trips')  # Wycieczka ma wiele atrakcji

    def __str__(self):
        return f"{self.name} ({', '.join(city.name for city in self.cities.all())})"

class Attraction(models.Model):
    name = models.CharField(max_length=512)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=512, default='unknown', null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.city})"

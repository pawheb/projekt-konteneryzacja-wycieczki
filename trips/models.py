from django.db import models

from enum import IntEnum

class Trip(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=512)
    city = models.CharField(max_length=512)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class Attraction(models.Model):
    class Category(IntEnum):
        SIGHTSEEING = 0
        RECREATION = 1
        AMUSEMENT = 2
        FOOD = 3

        @classmethod
        def choices(cls):
            return [(t.value, t.name) for t in cls]

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=512)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.CharField(max_length=4096)
    type = models.IntegerField(choices=Category.choices())
    trips = models.ManyToManyField(Trip)

    def __str__(self):
        return self.name

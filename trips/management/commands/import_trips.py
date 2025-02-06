from django.core.management.base import BaseCommand
from trips.models import Trip, City

class Command(BaseCommand):
    help = 'Import trips'

    def handle(self, *args, **kwargs):
        data = [
            ('Dubaj','2025-03-02','2025-03-06'),
            ('Amsterdam','2025-02-12','2025-02-16'),
            ('Tokio','2025-02-18','2025-02-22'),
            ('Barcelona','2025-02-20','2025-02-24'),
            ('Moskwa','2025-02-24','2025-03-04'),
            ('Wiedeń','2025-02-19','2025-02-24'),
            ('Berlin','2025-02-24','2025-03-03'),
            ('Londyn','2025-02-19','2025-02-22'),
            ('Buenos Aires','2025-02-10','2025-02-20'),
            ('Ateny','2025-02-02','2025-02-11'),
            ('Nowy Jork','2025-02-03','2025-02-13'),
            ('Paryż','2025-02-24','2025-02-27'),
            ('Budapeszt','2025-02-28','2025-03-08'),
            ('Stambuł','2025-02-06','2025-02-09'),
            ('Rzym','2025-02-10','2025-02-14'),
            ('Praga','2025-02-14','2025-02-23'),
            ('Seul','2025-02-06','2025-02-16'),
            ('Sydney','2025-02-26','2025-03-04'),
            ('Kapsztad','2025-03-03','2025-03-12'),
        ]

        cities_to_add = []
        for i in range(len(data)):
            cities_to_add.append(City(name=data[i][0]))
        City.objects.bulk_create(cities_to_add)

        data2 = [['Wycieczka do Dubaj', 46054.0, [102, 103, 113]], ['Wycieczka do Amsterdam', 488.0, [220, 227, 221, 228, 232, 233, 224]], ['Wycieczka do Tokio', 122.0, [160, 177, 158, 162, 165, 172, 159, 161]], ['Wycieczka do Barcelona', 6736.0, [62, 70, 73]], ['Wycieczka do Moskwa', 395.0, [284, 295, 285, 289, 296, 287, 290, 282]], ['Wycieczka do Wiedeń', 330.0, [404, 416, 407, 410, 399, 414, 400, 412, 403]], ['Wycieczka do Berlin', 189.0, [207, 211, 215, 209, 200, 212, 205]], ['Wycieczka do Londyn', 30492.0, [27, 24, 35, 32, 30]], ['Wycieczka do Buenos Aires', 80.0, [553, 544, 556, 540]], ['Wycieczka do Ateny', 8420.0, [153, 156, 140, 145, 157]], ['Wycieczka do Nowy Jork', 123.0, [11, 5]], ['Wycieczka do Paryż', 65624.0, [43, 56, 46, 42, 47, 41, 52]],['Wycieczka do Budapeszt', 140.0, [420, 423, 429, 428]], ['Wycieczka do Stambuł', 160.0, [273, 265, 274]], ['Wycieczka do Rzym', 3368.0, [132, 131, 121]], ['Wycieczka do Praga', 90.0, [381, 382, 393]], ['Wycieczka do Seul', 40.0, [369, 365, 364, 370]], ['Wycieczka do Sydney', 1150.0, [179, 180, 197, 182, 192, 190, 188, 185]], ['Wycieczka do Kapsztad', 495.0, [89, 82, 85, 87, 84]]]

        trips_to_add = []
        for i in range(len(data)):
            new_trip = Trip.objects.create(name=data2[i][0], start_date=data[i][1], end_date=data[i][2], price=data2[i][1])
            new_trip.cities.add(cities_to_add[i])
            new_trip.attractions.set(data2[i][2])





        self.stdout.write(self.style.SUCCESS('Successfully imported CSV data!'))

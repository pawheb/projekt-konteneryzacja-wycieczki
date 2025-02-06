import random
from django.core.management.base import BaseCommand 
from trips.models import Trip, City, Attraction

class Command(BaseCommand):
    help = 'Import trips'

    def handle(self, *args, **kwargs):
        # Lista danych: (nazwa miasta, data rozpoczęcia, data zakończenia)
        data = [
            ('Dubaj','2025-03-02','2025-03-06'),
            ('Amsterdam','2025-02-12','2025-02-16'),
            ('Tokyo','2025-02-18','2025-02-22'),
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
            ('Istanbul','2025-02-06','2025-02-09'),
            ('Rzym','2025-02-10','2025-02-14'),
            ('Praga','2025-02-14','2025-02-23'),
            ('Seul','2025-02-06','2025-02-16'),
            ('Sydney','2025-02-26','2025-03-04'),
            ('Kapsztad','2025-03-03','2025-03-12'),
        ]

        # Tworzymy rekordy dla miast – używamy bulk_create z ignore_conflicts=True,
        # dzięki czemu, jeśli rekordy o danej nazwie już istnieją, nie zostaną dodane ponownie.
        cities_to_add = [City(name=item[0]) for item in data]
        City.objects.bulk_create(cities_to_add, ignore_conflicts=True)
        
        # Pobierz utworzone miasta – kolejność nie zawsze jest gwarantowana, więc budujemy słownik wg. nazwy.
        cities_dict = { city.name: city for city in City.objects.all() }

        # Lista danych dla wycieczek: [nazwa wycieczki, [attraction_ids]]
        data2 = [
            ['Wycieczka do Dubaj', [102, 103, 113]],
            ['Wycieczka do Amsterdam', [220, 227, 221, 228, 232, 233, 224]],
            ['Wycieczka do Tokyo', [160, 177, 158, 162, 165, 172, 159, 161]],
            ['Wycieczka do Barcelona', [62, 70, 73]],
            ['Wycieczka do Moskwa', [284, 295, 285, 289, 296, 287, 290, 282]],
            ['Wycieczka do Wiedeń', [404, 416, 407, 410, 399, 414, 400, 412, 403]],
            ['Wycieczka do Berlin', [207, 211, 215, 209, 200, 212, 205]],
            ['Wycieczka do Londyn', [27, 24, 35, 32, 30]],
            ['Wycieczka do Buenos Aires', [553, 544, 556, 540]],
            ['Wycieczka do Ateny', [153, 156, 140, 145, 157]],
            ['Wycieczka do Nowy Jork', [11, 5]],
            ['Wycieczka do Paryż', [43, 56, 46, 42, 47, 41, 52]],
            ['Wycieczka do Budapeszt', [420, 423, 429, 428]],
            ['Wycieczka do Istanbul', [273, 265, 274]],
            ['Wycieczka do Rzym', [132, 131, 121]],
            ['Wycieczka do Praga', [381, 382, 393]],
            ['Wycieczka do Seul', [369, 365, 364, 370]],
            ['Wycieczka do Sydney', [179, 180, 197, 182, 192, 190, 188, 185]],
            ['Wycieczka do Kapsztad', [89, 82, 85, 87, 84]],
        ]

        trips_to_add = []
        for i in range(len(data)):
            trip_name = data2[i][0]
            # Sprawdzamy, czy wycieczka o danej nazwie już istnieje – jeśli tak, pomijamy jej tworzenie.
            if Trip.objects.filter(name=trip_name).exists():
                continue

            # Tworzymy nową wycieczkę z ustawioną ceną na 0
            new_trip = Trip.objects.create(
                name=trip_name,
                start_date=data[i][1],
                end_date=data[i][2],
                price=0
            )
            # Przypisujemy miasto na podstawie nazwy
            city_name = data[i][0]
            city_obj = cities_dict.get(city_name)
            if city_obj:
                new_trip.cities.add(city_obj)
            
            # Losowo wybieramy atrakcje dla danego miasta
            available_attractions = list(Attraction.objects.filter(city__iexact=city_name))
            if available_attractions:
                num_attractions = random.randint(5, 10)
                if len(available_attractions) < num_attractions:
                    num_attractions = len(available_attractions)
                selected_attractions = random.sample(available_attractions, num_attractions)
                new_trip.attractions.set(selected_attractions)
                # Obliczamy cenę wycieczki jako sumę cen wybranych atrakcji
                total_price = sum(attraction.price for attraction in selected_attractions)
                new_trip.price = total_price
                new_trip.save()
            
            trips_to_add.append(new_trip)

        self.stdout.write(self.style.SUCCESS('Successfully imported CSV data!'))

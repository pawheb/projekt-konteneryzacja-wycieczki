from django.core.management.base import BaseCommand
from trips.models import Trip
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Seed the database with sample Trip data'

    def handle(self, *args, **kwargs):
        # Lista 20 popularnych miast – jedno miasto na każdy plan
        cities = [
            "Nowy Jork", "Londyn", "Paryż", "Barcelona", "Kapsztad",
            "Dubaj", "Rzym", "Ateny", "Berlin", "Madryt",
            "Wiedeń", "Praga", "Amsterdam", "Budapeszt", "Moskwa",
            "Stambuł", "Sydney", "Tokio", "Seul", "Buenos Aires"
        ]
        
        self.stdout.write("Usuwanie istniejących planów z bazy...")
        Trip.objects.all().delete()

        today = date.today()

        for i, city in enumerate(cities, start=1):
            # Losowy termin rozpoczęcia (od jutra do 30 dni w przód)
            start_date = today + timedelta(days=random.randint(1, 30))
            # Losowy czas trwania wycieczki (od 3 do 10 dni)
            duration = random.randint(3, 10)
            end_date = start_date + timedelta(days=duration)
            # Losowa cena (np. od 100 do 1000 jednostek walutowych)
            price = round(random.uniform(100, 1000), 2)
            # Nazwa planu
            name = f"Plan wycieczki do {city}"
            
            trip = Trip(
                id=i,  # Ustawiamy id ręcznie (upewnij się, że nie koliduje z innymi rekordami)
                name=name,
                city=city,
                start_date=start_date,
                end_date=end_date,
                price=price
            )
            trip.save()
            self.stdout.write(f"Utworzono plan: {name} ({city})")
        
        self.stdout.write(self.style.SUCCESS('Pomyślnie zseeddowano bazę danych przykładowymi planami.'))

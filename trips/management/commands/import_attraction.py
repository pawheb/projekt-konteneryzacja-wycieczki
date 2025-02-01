import csv
from django.core.management.base import BaseCommand
from trips.models import Attraction

class Command(BaseCommand):
    help = 'Importuje atrakcje z pliku CSV do modelu Attraction'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Ścieżka do pliku CSV z danymi atrakcji')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                # Konwertujemy cenę: zamieniamy przecinek na kropkę
                price_str = row['Cena'].strip().replace(',', '.')
                try:
                    price = float(price_str)
                except ValueError:
                    price = 0.0

                attraction, created = Attraction.objects.get_or_create(
                    name=row['Nazwa Atrakcji'].strip(),
                    defaults={
                        'price': price,
                        'description': row['Opis'].strip(),
                        'category': row['Kategoria'].strip(),
                        'city': row['Miasto'].strip(),
                    }
                )
                if not created:
                    attraction.price = price
                    attraction.description = row['Opis'].strip()
                    attraction.category = row['Kategoria'].strip()
                    attraction.city = row['Miasto'].strip()
                    attraction.save()
                self.stdout.write(self.style.SUCCESS(f"Zaimportowano atrakcję: {attraction.name}"))
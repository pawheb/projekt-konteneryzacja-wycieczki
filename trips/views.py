import io
import json
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.conf import settings
from reportlab.pdfgen import canvas

# Importy niezbędne do rejestracji czcionek
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .models import Trip, Attraction, City

def list_trips(request):
    """
    Zwraca listę 20 planów wycieczkowych.
    """
    trips = Trip.objects.all()[:20]
    trips_list = []
    for trip in trips:
        trips_list.append({
            'id': trip.id,
            'name': trip.name,  # Teraz API zwraca nazwę tripa
            'start_date': trip.start_date.strftime('%Y-%m-%d'),
            'end_date': trip.end_date.strftime('%Y-%m-%d'),
            'price': str(trip.price),
        })
    return JsonResponse({'trips': trips_list})

def trip_detail(request, trip_id):
    """
    Zwraca szczegóły wybranego planu wycieczki.
    """
    try:
        trip = Trip.objects.get(id=trip_id)
    except Trip.DoesNotExist:
        raise Http404("Plan wycieczki nie został znaleziony.")

    # Pobieramy atrakcje przypisane do wycieczki – zwracamy listę nazw atrakcji.
    attractions_list = [attraction.name for attraction in trip.attractions.all()]

    trip_data = {
        'id': trip.id,
        'name': trip.name,
        'city': ", ".join(city.name for city in trip.cities.all()),
        'start_date': trip.start_date.strftime('%Y-%m-%d'),
        'end_date': trip.end_date.strftime('%Y-%m-%d'),
        'price': str(trip.price),
        'attractions': attractions_list,
    }
    return JsonResponse(trip_data)

def generate_pdf(plan_data):
    """
    Generuje PDF w pamięci przy użyciu ReportLab.
    Jeśli w danych planu znajduje się lista atrakcji, wypisuje ją w dokumencie.
    """
    # Rejestracja czcionek obsługujących polskie znaki.
    # Upewnij się, że ścieżka do plików czcionek jest poprawna.
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'fonts/DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'fonts/DejaVuSans-Bold.ttf'))
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    title = plan_data.get('name', "Twój Plan Wycieczki")
    
    # Używamy czcionki obsługującej polskie znaki
    p.setFont("DejaVuSans-Bold", 16)
    p.drawString(100, 800, title)
    p.setFont("DejaVuSans", 12)
    
    if 'city' in plan_data:
        p.drawString(100, 780, f"Miasto: {plan_data.get('city')}")
    if 'start_date' in plan_data and 'end_date' in plan_data:
        p.drawString(100, 760, f"Termin: {plan_data.get('start_date')} - {plan_data.get('end_date')}")
    if 'price' in plan_data:
        p.drawString(100, 740, f"Cena: {plan_data.get('price')}")
    if 'preferences' in plan_data:
        p.drawString(100, 720, f"Preferencje: {plan_data.get('preferences')}")
    
    # Jeśli przekazano listę atrakcji, wypisujemy ją w PDF
    if 'attractions' in plan_data:
        p.drawString(100, 700, "Atrakcje:")
        y = 680
        attractions = plan_data['attractions']
        # Jeśli atrakcje są listą, iterujemy po elementach
        if isinstance(attractions, list):
            for attraction in attractions:
                p.drawString(120, y, attraction)
                y -= 20
                if y < 50:
                    p.showPage()
                    y = 800
        # Jeśli atrakcje są tekstem, dzielimy na linie
        elif isinstance(attractions, str):
            for line in attractions.split("\n"):
                p.drawString(120, y, line)
                y -= 20
                if y < 50:
                    p.showPage()
                    y = 800

    p.drawString(100, 40, "Dziękujemy za skorzystanie z naszej aplikacji!")
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


@csrf_exempt
def generate_trip_pdf(request, trip_id):
    """
    Endpoint generujący PDF dla gotowego planu wycieczki oraz wysyłający go na podany e-mail.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Niepoprawny format JSON.'}, status=400)

        email = data.get('email', '')
        if not email:
            return JsonResponse({'error': 'Adres e-mail jest wymagany.'}, status=400)

        try:
            trip = Trip.objects.get(id=trip_id)
        except Trip.DoesNotExist:
            return JsonResponse({'error': 'Plan wycieczki nie istnieje.'}, status=404)

        # Pobieramy atrakcje przypisane do planu wycieczki
        attractions = trip.attractions.all()
        # Przygotowujemy listę, która zawiera nazwę oraz cenę każdej atrakcji.
        attractions_list = [f"{attraction.name} - {attraction.price}" for attraction in attractions]

        plan_data = {
            'name': trip.name,
            'city': ", ".join(city.name for city in trip.cities.all()),
            'start_date': trip.start_date.strftime('%Y-%m-%d'),
            'end_date': trip.end_date.strftime('%Y-%m-%d'),
            'price': str(trip.price),
            'attractions': attractions_list,
        }

        pdf_file = generate_pdf(plan_data)

        subject = "Twój gotowy plan wycieczki"
        message = "W załączniku znajdziesz swój plan wycieczki."
        email_message = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email]
        )
        email_message.attach('plan_wycieczki.pdf', pdf_file, 'application/pdf')
        try:
            email_message.send()
        except Exception as e:
            return JsonResponse({'error': f'Błąd wysyłania e-maila: {str(e)}'}, status=500)

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="plan_wycieczki.pdf"'
        return response
    else:
        return JsonResponse({'error': 'Metoda niedozwolona.'}, status=405)
@csrf_exempt
def create_individual_plan(request):
    """
    Endpoint przyjmujący dane indywidualnego planu:
      - city: nazwa miasta (np. "NOWY JORK")
      - preferences: kategoria atrakcji (np. "Zwiedzanie", "Rekreacja", "Rozrywka" itp.)
      - startDate, endDate: daty
      - email: adres e-mail odbiorcy

    Endpoint wyszukuje wszystkie atrakcje (z modelu Attraction),
    które mają pole 'city' odpowiadające wybranemu miastu (porównanie case-insensitive)
    oraz pole 'category' odpowiadające wybranym preferencjom.
    Następnie lista tych atrakcji (w postaci tekstu) jest dołączana do danych planu,
    generowany jest PDF i wysyłany na podany adres e-mail.
    """
    if request.method == "POST":
        if request.content_type.startswith('application/json'):
            try:
                data = json.loads(request.body.decode('utf-8'))
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Niepoprawny format JSON.'}, status=400)
        else:
            data = request.POST

        city = data.get('city', '').strip()
        preferences = data.get('preferences', '').strip()
        start_date = data.get('startDate', '').strip()
        end_date = data.get('endDate', '').strip()
        recipient_email = data.get('email', '').strip()

        if not all([city, preferences, start_date, end_date, recipient_email]):
            return JsonResponse({'error': 'Wszystkie pola są wymagane.'}, status=400)

        # Pobieramy atrakcje dla podanego miasta oraz o określonej kategorii (porównanie ignorujące wielkość liter)
        attractions_qs = Attraction.objects.filter(
            city__iexact=city,
            category__iexact=preferences
        )
        attractions_list = [f"{attr.name} - {attr.price}" for attr in attractions_qs]
        attractions_text = "\n".join(attractions_list) if attractions_list else "Brak atrakcji spełniających kryteria."

        # Oblicz cenę wycieczki jako sumę cen wszystkich pasujących atrakcji
        total_price = sum(attr.price for attr in attractions_qs)

        plan_data = {
            'name': "Indywidualny Plan Wycieczki",
            'city': city,
            'preferences': preferences,
            'start_date': start_date,
            'end_date': end_date,
            'attractions': attractions_text,
            'price': str(total_price)  # Dodajemy obliczoną cenę
        }

        pdf_file = generate_pdf(plan_data)

        subject = "Twój indywidualny plan wycieczki"
        message = "W załączniku znajdziesz swój indywidualny plan wycieczki."
        email_message = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email]
        )
        email_message.attach('indywidualny_plan.pdf', pdf_file, 'application/pdf')
        try:
            email_message.send()
        except Exception as e:
            return JsonResponse({'error': f'Błąd wysyłania e-maila: {str(e)}'}, status=500)

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="indywidualny_plan.pdf"'
        return response
    else:
        return JsonResponse({'error': 'Metoda niedozwolona.'}, status=405)

def list_cities(request):
    cities = City.objects.all()
    cities_list = [{'name': city.name} for city in cities]
    return JsonResponse({'cities': cities_list})

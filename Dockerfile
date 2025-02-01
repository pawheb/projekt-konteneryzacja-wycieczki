# Używamy obrazu Pythona 3.11 (lub innej odpowiedniej wersji)
FROM python:3.11-slim

# Wyłączamy generowanie plików .pyc i wymuszamy od razu wypisywanie logów
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Ustawiamy katalog roboczy
WORKDIR /app

# Aktualizujemy pip oraz instalujemy pipenv
RUN pip install --upgrade pip && pip install pipenv

# Kopiujemy pliki Pipfile i opcjonalnie Pipfile.lock (jeśli istnieje)
# Dzięki temu Docker może wykorzystać cache przy niezmienionych zależnościach
COPY Pipfile* /app/

# Instalujemy zależności system-wide korzystając z Pipenv
# Jeśli masz wygenerowany Pipfile.lock, możesz użyć opcji --deploy
RUN pipenv install --system --deploy

# Kopiujemy resztę plików projektu do kontenera
COPY . /app/

# Otwieramy port 8000 (domyślny dla Django)
EXPOSE 8000

# Domyślna komenda uruchamiająca serwer Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

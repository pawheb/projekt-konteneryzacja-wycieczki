document.addEventListener('DOMContentLoaded', function() {
    // Pobranie i wyświetlenie listy gotowych planów
    fetch('/api/trips/')
        .then(response => response.json())
        .then(data => {
            const plansContainer = document.getElementById('plany-lista');
            data.trips.forEach(trip => {
                const planDiv = document.createElement('div');
                planDiv.className = 'plan-item';
                planDiv.innerHTML = `
                    <h3>${trip.name}</h3>
                    <p>Miasto: ${trip.city}</p>
                    <p>Termin: ${trip.start_date} - ${trip.end_date}</p>
                    <p>Cena: ${trip.price}</p>
                `;
                plansContainer.appendChild(planDiv);
            });
        })
        .catch(error => console.error('Error fetching trips:', error));

    // Obsługa wysyłki formularza dla indywidualnego planu
    const form = document.getElementById('plan-form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();

        // Pobranie wartości z formularza
        // UWAGA: Upewnij się, że element <select> dla miasta ma ustawiony atrybut name="city"
        const citySelect = form.querySelector('select');
        const city = citySelect.value;
        const preferences = document.getElementById('preferences').value;
        const startDate = document.getElementById('start-date').value;
        const endDate = document.getElementById('end-date').value;
        const email = document.getElementById('global-email').value;

        // Przygotowanie danych do wysłania
        const formData = new FormData();
        formData.append('city', city);
        formData.append('preferences', preferences);
        formData.append('startDate', startDate);
        formData.append('endDate', endDate);
        formData.append('email', email);

        fetch('/api/trips/create/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById('indywidualny-plan-wynik');
            if(data.error) {
                resultDiv.innerHTML = `<p style="color: red;">${data.error}</p>`;
            } else {
                resultDiv.innerHTML = `<p style="color: green;">${data.message}</p>`;
            }
        })
        .catch(error => console.error('Error:', error));
    });
});

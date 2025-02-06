document.addEventListener('DOMContentLoaded', function() {
    // --- Obsługa gotowych planów (np. dropdown o id "city-select") ---
    fetch('/api/trips/')
        .then(response => response.json())
        .then(data => {
            console.log("Dane pobrane z API:", data);
            const planSelect = document.getElementById('city-select');

            data.trips.forEach(trip => {
                const option = document.createElement('option');
                option.value = trip.id;
                option.appendChild(document.createTextNode(trip.name));
                planSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching trips:', error));

    // --- Pobieranie miast dla formularza indywidualnego planu ---
    fetch('/api/cities/')
        .then(response => response.json())
        .then(data => {
            console.log("Dane miast pobrane z API:", data);
            const citySelect = document.getElementById('form-city');
            data.cities.forEach(city => {
                const option = document.createElement('option');
                option.value = city.name;
                option.textContent = city.name;
                citySelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching cities:', error));

    // --- Obsługa wyboru gotowego planu ---
    document.getElementById('city-select').addEventListener('change', function() {
        const selectedTripId = this.value;
        const detailsDiv = document.getElementById('plan-szczegoly');
        
        if (!selectedTripId) {
            detailsDiv.innerHTML = '';
            detailsDiv.style.display = 'none';
            return;
        }
        
        fetch(`/api/trips/${selectedTripId}/`)
            .then(response => response.json())
            .then(trip => {
                // Tworzymy HTML listę atrakcji
                const attractionsHTML = trip.attractions && trip.attractions.length
                    ? `<ul>${trip.attractions.map(item => `<li>${item}</li>`).join('')}</ul>`
                    : 'Brak atrakcji';
                
                detailsDiv.innerHTML = `
                    <h3>Plan: ${trip.name}</h3>
                    <p><strong>Termin:</strong> ${trip.start_date} - ${trip.end_date}</p>
                    <p><strong>Cena:</strong> ${trip.price}</p>
                    <p><strong>Atrakcje:</strong></p>
                    ${attractionsHTML}
                    <div class="form-group">
                      <label for="email">Podaj e-mail:</label>
                      <input type="email" id="email" placeholder="Podaj e-mail" required>
                    </div>
                    <button onclick="generatePDF('${trip.id}')">Generuj PDF</button>
                `;
                detailsDiv.style.display = 'block';
            })
            .catch(error => console.error('Error fetching trip details:', error));
    });

    // Funkcja generująca PDF dla gotowego planu i wysyłająca e-mail
    window.generatePDF = function(tripId) {
        const emailInput = document.getElementById('email');
        if (!emailInput) {
            alert('Pole e-mail nie zostało znalezione.');
            return;
        }
        const email = emailInput.value;
        if (!email) {
            alert('Podaj poprawny adres e-mail!');
            return;
        }
        
        fetch(`/api/trips/generate-pdf/${tripId}/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Błąd podczas generowania PDF.');
            }
            return response.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'plan_wycieczki.pdf';
            document.body.appendChild(a);
            a.click();
            a.remove();
        })
        .catch(error => {
            console.error('Error generating PDF:', error);
            alert('Wystąpił błąd podczas generowania planu.');
        });
    };

    // Obsługa formularza indywidualnego planu
    document.getElementById('plan-form').addEventListener('submit', function(e) {
        e.preventDefault();

        const city = document.getElementById('form-city').value;
        const preferences = document.getElementById('preferences').value;
        const startDate = document.getElementById('start-date').value;
        const endDate = document.getElementById('end-date').value;
        const email = document.getElementById('global-email').value;
        const resultDiv = document.getElementById('indywidualny-plan-wynik');

        if (!city || !preferences || !startDate || !endDate || !email) {
            alert('Proszę wypełnić wszystkie pola.');
            return;
        }

        const data = { city, preferences, startDate, endDate, email };

        fetch('/api/trips/generate-individual-pdf/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Błąd podczas generowania indywidualnego planu.');
            }
            return response.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'indywidualny_plan.pdf';
            document.body.appendChild(a);
            a.click();
            a.remove();
            resultDiv.textContent = 'Plan został wygenerowany i wysłany na podany adres e-mail.';
        })
        .catch(error => {
            console.error('Error generating individual PDF:', error);
            alert('Wystąpił błąd podczas generowania indywidualnego planu.');
        });
    });
});

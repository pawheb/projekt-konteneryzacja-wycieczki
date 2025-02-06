#!/bin/python3

import pandas as pd
import random
import locale

locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')

df = pd.read_csv('daneeee.csv', sep=";")

cities = list(set(df['Miasto']))
result = []
prices = [0 for i in range(len(cities))]
plans_made_for = []

price_index = -1
for city in cities:
    price_index += 1
    city_rows = df.loc[df['Miasto'] == city]
    print(city_rows)
    num_of_attractions = random.randint(2, 10)
    attractions = []
    indexes = []
    for i in range(num_of_attractions):
        city_attration_len = len(city_rows)
        chosen_attraction = random.randint(0, city_attration_len-1)
        print(chosen_attraction)
        if chosen_attraction not in indexes:
            attractions.append(int(city_rows.iloc[chosen_attraction].values.tolist()[0]))
            indexes.append(chosen_attraction)
            prices[price_index] += locale.atof(city_rows.iloc[chosen_attraction].values.tolist()[2])
        else:
            continue

    result.append(attractions)

print(cities)
print(result)

result2 = []

dictin = [('Rzym','2025-02-10','2025-02-14'),
         ('Ateny','2025-02-02','2025-02-11'),
         ('Berlin','2025-02-24','2025-03-03'),
         ('Madryt','2025-02-28','2025-03-09'),
         ('Wiedeń','2025-02-19','2025-02-24'),
         ('Praga','2025-02-14','2025-02-23'),
         ('Amsterdam','2025-02-12','2025-02-16'),
         ('Budapeszt','2025-02-28','2025-03-08'),
         ('Moskwa','2025-02-24','2025-03-04'),
         ('Stambuł','2025-02-06','2025-02-09'),
         ('Sydney','2025-02-26','2025-03-04'),
         ('Tokio','2025-02-18','2025-02-22'),
         ('Seul','2025-02-06','2025-02-16'),
         ('Buenos Aires','2025-02-10','2025-02-20')]


for i in range(len(cities)):
    adding = []
    adding.append(f"Wycieczka do {cities[i]}")
    adding.append(prices[i])
    adding.append(result[i])
    result2.append(adding)
print(result2)

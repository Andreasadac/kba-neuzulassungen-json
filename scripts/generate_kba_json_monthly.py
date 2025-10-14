import json
from datetime import datetime

monat = datetime.now().strftime('%B')

neuzulassungen = [
    ["Marke", "Anzahl"],
    ["VW", 45225], ["Mercedes", 20338], ["BMW", 19388], ["Skoda", 18872],
    ["Audi", 15728], ["Seat", 13247], ["Opel", 12324], ["Ford", 9065],
    ["Toyota", 7987], ["Hyundai", 7519], ["Dacia", 5703], ["Kia", 5208],
    ["Renault", 5078], ["Peugeot", 4428], ["Fiat", 4400], ["Citroen", 4315],
    ["Volvo", 4026], ["Mazda", 3809], ["Tesla", 3404], ["BYD", 3255],
    ["Nissan", 3237], ["Mini", 3072], ["MG Roewe", 2615], ["Porsche", 2247],
    ["Suzuki", 2226]
]

marktanteile = [
    ["Marke", "Prozent"],
    ["VW", 19.2], ["Mercedes", 8.6], ["BMW", 8.2], ["Skoda", 8.0],
    ["Audi", 6.7], ["Seat", 5.6], ["Opel", 5.2], ["Ford", 3.8],
    ["Toyota", 3.4], ["Hyundai", 3.2], ["Dacia", 2.4], ["Kia", 2.2],
    ["Renault", 2.2], ["Peugeot", 1.9], ["Fiat", 1.9], ["Citroen", 1.8],
    ["Volvo", 1.7], ["Mazda", 1.6], ["Tesla", 1.4], ["BYD", 1.4],
    ["Nissan", 1.4], ["Mini", 1.3], ["MG Roewe", 1.1], ["Porsche", 1.0],
    ["Suzuki", 0.9]
]

infogram_data = [
    {
        "title": f"Neuzulassungen {monat}",
        "data": neuzulassungen
    },
    {
        "title": f"Marktanteile {monat}",
        "data": marktanteile
    }
]

with open("kba_neuzulassungen_infogram.json", "w", encoding="utf-8") as f:
    json.dump(infogram_data, f, ensure_ascii=False, indent=2)

print(f"Die Datei 'kba_neuzulassungen_infogram.json' wurde erfolgreich mit dem Monatstitel '{monat}' erstellt.")

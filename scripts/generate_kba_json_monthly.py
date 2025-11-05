import pandas as pd
import json
import os

# Pfad zur Excel-Datei
excel_file = "pm_45_2025_fahrzeugzulassungen_10_2025_marken.xlsx"

# Prüfen, ob die Datei existiert
if not os.path.exists(excel_file):
    raise FileNotFoundError(f"Datei nicht gefunden: {excel_file}")

# Einlesen ab Zeile 5
df = pd.read_excel(excel_file, skiprows=4, engine="openpyxl")

# Spaltennamen setzen
df.columns = [
    "_", "Marke", "Oktober 2025", "Anteil Okt (%)", "Veränderung Okt 2024 (%)",
    "Jan-Okt 2025", "Anteil Jan-Okt (%)", "Veränderung Jan-Okt 2024 (%)"
]

# Unnötige Spalte entfernen
df = df.drop(columns=["_"])

# Ungültige Marken entfernen
df = df[df["Marke"].notna() & (df["Marke"] != "INSGESAMT")]

# In JSON konvertieren
json_data = df.to_dict(orient="records")

# Dateiname mit Monat im Namen
output_file = "kba_neuzulassungen_10_2025.json"

# Speichern
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)

print(f"✅ JSON-Datei erfolgreich erstellt: {output_file} ({len(json_data)} Marken)")

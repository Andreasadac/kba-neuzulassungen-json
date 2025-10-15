import requests
import re
import json
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from io import BytesIO

# KBA-Pressemitteilungsübersicht
base_url = "https://www.kba.de/SiteGlobals/Forms/Suche/Pressemitteilungen/Pressemitteilungensuche_Formular.html?nn=827402"

# HTML abrufen und durchsuchen
response = requests.get(base_url)
soup = BeautifulSoup(response.content, "html.parser")

# Aktuellste Pressemitteilung zur Fahrzeugzulassung finden
link_tag = soup.find("a", string=re.compile("Fahrzeugzulassungen.*2025"))
if not link_tag:
    raise Exception("Keine passende Pressemitteilung gefunden.")

# Detailseite öffnen
detail_url = "https://www.kba.de" + link_tag.get("href")
detail_response = requests.get(detail_url)
detail_soup = BeautifulSoup(detail_response.content, "html.parser")

# Excel-Link extrahieren
excel_link = detail_soup.find("a", href=re.compile(".*merkmale.*\\.xlsx"))
if not excel_link:
    raise Exception("Kein Excel-Link gefunden.")

excel_url = "https://www.kba.de" + excel_link.get("href")

# Excel-Datei herunterladen
excel_response = requests.get(excel_url)
excel_data = BytesIO(excel_response.content)

# Monat aus dem Titel extrahieren
title_text = link_tag.text
monat_match = re.search(r"im (\\w+) 2025", title_text)
monat = monat_match.group(1) if monat_match else datetime.now().strftime('%B')

# Excel-Datei verarbeiten
xls = pd.ExcelFile(excel_data, engine="openpyxl")
sheet_names = xls.sheet_names

# Tabellenblätter identifizieren
neuzulassung_sheet = next((s for s in sheet_names if "Neuzulassungen" in s), sheet_names[0])
marktanteil_sheet = next((s for s in sheet_names if "Marktanteile" in s), sheet_names[-1])

df_neu = xls.parse(neuzulassung_sheet)
df_markt = xls.parse(marktanteil_sheet)

# Daten extrahieren
neuzulassungen = [["Marke", "Anzahl"]]
marktanteile = [["Marke", "Prozent"]]

for _, row in df_neu.iterrows():
    if pd.notna(row.get("Marke")) and pd.notna(row.get("Anzahl")):
        neuzulassungen.append([row["Marke"], int(row["Anzahl"])])

for _, row in df_markt.iterrows():
    if pd.notna(row.get("Marke")) and pd.notna(row.get("Prozent")):
        marktanteile.append([row["Marke"], round(float(row["Prozent"]), 1)])

# Infogram-kompatible JSON erzeugen
infogram_data = [
    [[f"Neuzulassungen {monat} 2025"]] + neuzulassungen,
    [[f"Marktanteile {monat} 2025"]] + marktanteile
]

with open("kba_neuzulassungen_infogram.json", "w", encoding="utf-8") as f:
    json.dump(infogram_data, f, ensure_ascii=False, indent=2)

print(f"Die Datei 'kba_neuzulassungen_infogram.json' wurde erfolgreich mit dem Monatstitel '{monat} 2025' erstellt.")

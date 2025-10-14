import pandas as pd
import json
import requests
from io import BytesIO
from datetime import datetime
from bs4 import BeautifulSoup

# Prüfen ob aktuelles Datum zwischen 6. und 12. liegt
heute = datetime.today()
if heute.day < 6 or heute.day > 12:
    print("Heute ist nicht zwischen dem 6. und 12. – kein automatischer Download.")
else:
    # KBA-Seite mit Pressemitteilungen
    base_url = "https://www.kba.de/DE/Presse/Pressemitteilungen/Fahrzeugzulassungen/"

    try:
        # HTML-Inhalt laden und parsen
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Suche nach XLSX-Download-Link
        links = soup.find_all("a", href=True)
        xlsx_links = [l["href"] for l in links if l["href"].endswith(".xlsx") and "fahrzeugzulassungen" in l["href"]]

        if not xlsx_links:
            print("Keine passende XLSX-Datei gefunden.")
        else:
            # Vollständige URL zur Datei
            file_url = "https://www.kba.de" + xlsx_links[0]
            print(f"Gefundene Datei: {file_url}")

            # Datei herunterladen und verarbeiten
            file_response = requests.get(file_url)
            file_response.raise_for_status()
            xls = pd.ExcelFile(BytesIO(file_response.content), engine="openpyxl")
            df = xls.parse(xls.sheet_names[0], skiprows=5)
            df = df.iloc[:, [1, 2, 3]]
            df.columns = ["Marke", "Zulassungen", "Marktanteil"]
            df = df.dropna(subset=["Marke", "Zulassungen", "Marktanteil"])
            df = df[df["Marke"].str.upper() != "INSGESAMT"]
            df["Zulassungen"] = pd.to_numeric(df["Zulassungen"], errors="coerce")
            df["Marktanteil"] = pd.to_numeric(df["Marktanteil"], errors="coerce")
            df = df.dropna(subset=["Zulassungen", "Marktanteil"])
            df_sorted = df.sort_values(by="Zulassungen", ascending=False).head(25)

            data = {
                "neuzulassungen": [
                    {"marke": row["Marke"], "wert": int(row["Zulassungen"])} for _, row in df_sorted.iterrows()
                ],
                "marktanteile": [
                    {"marke": row["Marke"], "wert": round(float(row["Marktanteil"]), 1)} for _, row in df_sorted.iterrows()
                ]
            }

            json_filename = f"data/neuzulassungen_{heute.year}_{heute.month:02}.json"
            with open(json_filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"Die JSON-Datei wurde erfolgreich erstellt: {json_filename}")

    except Exception as e:
        print("Fehler beim Web-Scraping oder Verarbeiten der Datei:", e)

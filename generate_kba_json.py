import pandas as pd
import json
import requests
from io import BytesIO
from datetime import datetime

# Prüfen ob aktuelles Datum zwischen 6. und 12. liegt
heute = datetime.today()
if heute.day < 6 or heute.day > 12:
    print("Heute ist nicht zwischen dem 6. und 12. – kein automatischer Download.")
else:
    # Monat und Jahr für die URL bestimmen
    jahr = heute.year
    monat = heute.month

    # Beispielhafte URL-Struktur – muss ggf. angepasst werden, wenn KBA andere Dateinamen verwendet
    url = f"https://www.kba.de/SharedDocs/Downloads/DE/Pressemitteilungen/{jahr}/pm_39_{jahr}_fahrzeugzulassungen_{monat:02}_{jahr}.xlsx?__blob=publicationFile"

    try:
        response = requests.get(url)
        response.raise_for_status()
        xls = pd.ExcelFile(BytesIO(response.content), engine="openpyxl")
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

        json_filename = f"data/neuzulassungen_{jahr}_{monat:02}.json"
        with open(json_filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"Die JSON-Datei wurde erfolgreich erstellt: {json_filename}")
    except Exception as e:
        print("Fehler beim Herunterladen oder Verarbeiten der Datei:", e)

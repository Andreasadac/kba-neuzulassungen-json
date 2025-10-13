import pandas as pd
import json
import requests
from io import BytesIO
from datetime import datetime

# Aktuellen Monat und Jahr bestimmen
monat = datetime.now().month
jahr = datetime.now().year

# URL zur KBA-Datei
url = f"https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ10/{jahr}/fz10_{jahr}_{monat:02}.xlsx?__blob=publicationFile"

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

    with open("data/neuzulassungen.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("JSON-Datei erfolgreich erstellt.")
except Exception as e:
    print("Fehler beim Verarbeiten der KBA-Daten:", e)

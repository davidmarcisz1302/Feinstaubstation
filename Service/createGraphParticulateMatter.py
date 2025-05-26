import os
import re
import sqlite3
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd

from Model.MeasurementValuesParticulate import measurementValuesParticulate

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dbRoot   = os.path.join(BASE_DIR, '..', 'Model', 'feinstaubDB.sqlite')

year = "2022"
inputDateMessage = "Bitte gib ein Datum ein (dd.mm): "


def getValidDateInput():
    dateRegex = r"^\d{2}\.\d{2}$"

    while True:
        dateInput = input(inputDateMessage).strip()

        if len(dateInput) == 5 and re.match(dateRegex, dateInput):

            try:
                datetime.strptime(dateInput + "." + year, "%d.%m.%Y")
                return dateInput
            except ValueError:
                print("Ungültiges Datum. Bitte gib ein echtes Datum ein.")
        else:
            print("Ungültige Eingabe. Bitte verwende das Format dd.mm (z.B. 08.02).")


def formatToSqlDate(dateInput):
    parsedDate = datetime.strptime(dateInput + "." + year, "%d.%m.%Y")
    return parsedDate.strftime("%Y-%m-%d")


# Durchschnittliche Feinstaubwerte von 0:00-24:00 Uhr
def fetchParticulateMatterForDate():
    global connection
    dateInput = getValidDateInput()
    formattedDate = formatToSqlDate(dateInput)

    try:
        connection = sqlite3.connect(dbRoot)

        # 2-Stunden-Intervall-Daten
        timestamps = []
        pm10Values = []
        pm25Values = []

        print(f"\nFeinstaubwerte am {dateInput}.{year}\n")

        for hour in range(0, 24, 2):
            startTime = f"{hour:02}:00:00"
            endTime = f"{hour + 2:02}:00:00"
            label = f"{hour:02}:00–{hour + 2:02}:00"

            queryPmInterval = """
                              SELECT AVG(P1) AS avgP1,
                                     AVG(P2) AS avgP2
                              FROM measurementValuesParticulate
                              WHERE DATE(timestamp) = ?
                                AND TIME(timestamp) >= ?
                                AND TIME(timestamp) < ?; \
                              """

            result = pd.read_sql_query(queryPmInterval, connection, params=(formattedDate, startTime, endTime))

            avgP1 = result.iloc[0]['avgP1'] if not result.empty else None
            avgP2 = result.iloc[0]['avgP2'] if not result.empty else None

            timestamps.append(label)
            pm10Values.append(round(avgP1, 2) if avgP1 else 0)
            pm25Values.append(round(avgP2, 2) if avgP2 else 0)

            print(f"{label} Uhr:")
            print(f"  PM10 = {pm10Values[-1]} µg/m³")
            print(f"  PM2,5 = {pm25Values[-1]} µg/m³\n")

        # Diagramm erzeugen
        plt.figure(figsize=(12, 6))

        plt.plot(timestamps, pm10Values, marker='o', label='PM10 (µg/m³)', color='green')
        plt.plot(timestamps, pm25Values, marker='s', label='PM2.5 (µg/m³)', color='red')

        plt.title(f"Feinstaubverlauf am {dateInput}.{year}")

        # Label X,Y-Achse
        plt.xlabel("Zeitintervall")
        plt.ylabel("Feinstaubkonzentration (µg/m³)")

        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

        # Objekt Feinstaubsensor (Gesamtdurchschnitt über den Tag)
        maxP1 = max(pm10Values)
        minP1 = min(pm10Values)
        avgP1 = round(sum(pm10Values) / len(pm10Values), 2)

        maxP2 = max(pm25Values)
        minP2 = min(pm25Values)
        avgP2 = round(sum(pm25Values) / len(pm25Values), 2)

        particualteDatas = measurementValuesParticulate(
            maxP1, minP1, avgP1,
            maxP2, minP2, avgP2
        )

        # Objekt korrekt ausgeben
        print("Das Objekt:\n", particualteDatas)

    finally:
        connection.close()
import os
import re
import sqlite3
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd

from Model.MeasurementValuesParticulate import measurementValuesParticulate

BASE_DIR = os.path.dirname(os.path.abspath(__file__))     # …/Service
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
def fetchMeasurementValuesWeatherForDate():
    global connection
    dateInput = getValidDateInput()
    formattedDate = formatToSqlDate(dateInput)

    try:
        connection = sqlite3.connect(dbRoot)

        # 2-Stunden-Intervall-Daten
        timestamps = []
        temperatureValues = []

        print(f"\nTemperatur am {dateInput}.{year}\n")

        for hour in range(0, 24, 2):
            startTime = f"{hour:02}:00:00"
            endTime = f"{hour + 2:02}:00:00"
            label = f"{hour:02}:00–{hour + 2:02}:00"

            queryPmInterval = """
                              SELECT AVG(temperature) AS temperature
                              FROM main.measurementValuesWeather
                              WHERE DATE(timestamp) = ?
                                AND TIME(timestamp) >= ?
                                AND TIME(timestamp) < ?; \
                              """

            result = pd.read_sql_query(queryPmInterval, connection, params=(formattedDate, startTime, endTime))

            temperature = result.iloc[0]['temperature'] if not result.empty else None

            timestamps.append(label)
            temperatureValues.append(round(temperature, 2) if temperature else 0)

            print(f"{label} Uhr: {round(temperature, 2)} °C")

        # Diagramm erzeugen
        plt.figure(figsize=(12, 6))

        plt.plot(timestamps, temperatureValues, marker='o', label='Temperatur °C', color='green')

        plt.title(f"Wetter Temperatur am {dateInput}.{year}")

        # Label X,Y-Achse
        plt.xlabel("Zeitintervall t")
        plt.ylabel("Temperatur °C")

        plt.xticks(rotation=15)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

        # Objekt Feinstaubsensor (Gesamtdurchschnitt über den Tag)
        temperature = round(sum(temperatureValues) / len(temperatureValues), 2)

    finally:
        connection.close()
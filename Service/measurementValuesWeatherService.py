import re
import sqlite3
from datetime import datetime
import pandas as pd
from Model.MeasurementValuesWeather import measurementValuesWeather

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dbRoot   = os.path.join(BASE_DIR, '..', 'Model', 'feinstaubDB.sqlite')

year = "2022"
inputDateMessage = "Bitte gib ein Datum ein (dd.mm): "

# Liste für Objekte
weatherDataList = []

# Validiert das Eingabedatum
def getValidDate():
    # Eingaben validieren im Format dd.mm
    dateRegex = r"^\d{2}\.\d{2}$"

    while True:
        dateInput = input(inputDateMessage).strip()
        if len(dateInput) == 5 and re.match(dateRegex, dateInput):
            datetime.strptime(dateInput + "." + year, "%d.%m.%Y")
            return dateInput
        else:
            print("Ungültige Eingabe. Bitte verwende das Format dd.mm (z.B. 08.02).")

# Konvertiere dd.mm in yyyy-mm-dd für SQL
def formatToSqlDate(dateInput):
    parsedDate = datetime.strptime(dateInput + "." + year, "%d.%m.%Y")
    return parsedDate.strftime("%Y-%m-%d")


def getMeasurementValuesWeather():
    global connection, row, pm_row, temp_row
    dateInput = getValidDate()
    formattedDate = formatToSqlDate(dateInput)

    try:
        connection = sqlite3.connect(dbRoot)

        # Temperaturabfrage
        queryTempStats = """
                         SELECT DATE(timestamp)  AS date,
                                MAX(temperature) AS maxTemperatur,
                                MIN(temperature) AS minTemperatur,
                                AVG(temperature) AS durchschnittlicheTemperatur
                         FROM measurementValuesWeather
                         WHERE DATE(timestamp) = ?; \
                         """

        temperaturQuery = pd.read_sql_query(queryTempStats, connection, params=(formattedDate,))

        if not temperaturQuery.empty:
            temp_row = temperaturQuery.iloc[0]
            print(f"\nTemperatur am {dateInput}.{year}:")
            print(f"  Maximale Temperatur: {temp_row['maxTemperatur']} °C")
            print(f"  Minimale Temperatur: {temp_row['minTemperatur']} °C")
            print(f"  Durchschnittliche Temperatur: {round(temp_row['durchschnittlicheTemperatur'], 2)} °C")
        else:
            print("\nKeine Temperaturdaten für dieses Datum gefunden.")

        # Objekt Wetterstation
        weatherDatas = measurementValuesWeather(
            temp_row['maxTemperatur'],
            temp_row['minTemperatur'],
            round(temp_row['durchschnittlicheTemperatur'], 2))

       # Speicherung des Objekts in Array
        weatherDataList.append(weatherDatas)

        # Objekt korrekt ausgeben
        print("Das Objekt:\n", weatherDatas)

    finally:
        connection.close()
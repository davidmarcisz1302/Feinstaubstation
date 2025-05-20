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

# Validiert das Eingabedatum, dd.mm, ohne Buchstaben, Leerzeichen und genau 5 Zeichen
def getValidDate():
    # Eingaben validieren im Format dd.mm
    dateRegex = r"^\d{2}\.\d{2}$"

    while True:
        dateInput = input(inputDateMessage).strip() # Alle führenden und nachfolgenden Whitespace-Zeichen aus dem String entfernen.

        if len(dateInput) == 5 and re.match(dateRegex, dateInput):
            # konvertiert den String in ein Datum und überprüft die gültigkeit des Datums
            datetime.strptime(dateInput + "." + year, "%d.%m.%Y")
            return dateInput
        else:
            print("Ungültige Eingabe. Bitte verwende das Format dd.mm (z.B. 08.02).")

#  Von Eingabe Format "dd.mm" (z.B. "08.02") und wandelt es in das SQL-Datenformat "YYYY-MM-DD"
def formatToSqlDate(dateInput):
    parsedDate = datetime.strptime(dateInput + "." + year, "%d.%m.%Y")
    return parsedDate.strftime("%Y-%m-%d") # Format: "YYYY-MM-DD" → SQL-Datenformat


def getMeasurementValuesWeather():
    global connection, row, tempRow
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
                         WHERE DATE(timestamp) = ?; 
                         """

        temperaturQuery = pd.read_sql_query(queryTempStats, connection, params=(formattedDate,))

        if not temperaturQuery.empty:
            tempRow = temperaturQuery.iloc[0]
            print(f"\nTemperatur am {dateInput}.{year}:")
            print(f"  Maximale Temperatur: {tempRow['maxTemperatur']} °C")
            print(f"  Minimale Temperatur: {tempRow['minTemperatur']} °C")
            print(f"  Durchschnittliche Temperatur: {round(tempRow['durchschnittlicheTemperatur'], 2)} °C")
        else:
            print("\nKeine Temperaturdaten für dieses Datum gefunden.")

        # Objekt Wetter
        weatherDatas = measurementValuesWeather(
            tempRow['maxTemperatur'],
            tempRow['minTemperatur'],
            round(tempRow['durchschnittlicheTemperatur'], 2))

       # Speicherung des Objekts in Array
        weatherDataList.append(weatherDatas)

        # Objekt ausgeben
        print("Das Objekt:\n", weatherDatas)

    finally:
        connection.close()
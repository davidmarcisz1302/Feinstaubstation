import re
import sqlite3
from datetime import datetime
import pandas as pd

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


def getMeasurementValuesHumidity():
    global connection, row, pm_row, humidity_row
    dateInput = getValidDate()
    formattedDate = formatToSqlDate(dateInput)

    try:
        connection = sqlite3.connect(dbRoot)

        # Temperaturabfrage
        queryTempStats = """
                         SELECT DATE(timestamp)  AS date,
                                MAX(humidity) AS maxHumidity,
                                MIN(humidity) AS minHumidity,
                                AVG(humidity) AS avgHumidity
                         FROM measurementValuesWeather
                         WHERE DATE(timestamp) = ?; \
                         """

        temperaturQuery = pd.read_sql_query(queryTempStats, connection, params=(formattedDate,))

        if not temperaturQuery.empty:
            humidity_row = temperaturQuery.iloc[0]
            print(f"\nLuftfeuchtigkeit am {dateInput}.{year}:")
            print(f"  Maximale Luftfeuchtigkeit: {humidity_row['maxHumidity']}%")
            print(f"  Minimale Luftfeuchtigkeit: {humidity_row['minHumidity']}%")
            print(f"  Durchschnittliche Luftfeuchtigkeit: {round(humidity_row['avgHumidity'], 2)}%")
        else:
            print("\nKeine Luftfeuchtigkeitsdaten für dieses Datum gefunden.")

    finally:
        connection.close()
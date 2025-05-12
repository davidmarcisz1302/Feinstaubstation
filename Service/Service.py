import re
import sqlite3
from datetime import datetime

import pandas as pd

from Model.MeasurementValuesParticulate import measurementValuesParticulate
from Model.MeasurementValuesWeather import measurementValuesWeather
from Service import createGraph

dbRoot = "../Model/feinstaubDB.sqlite"
year = "2022"
inputDateMessage = "Bitte gib ein Datum ein (dd.mm): "

def getValidDate():
    # Eingaben validieren im Format dd.mm
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
    # Konvertiere dd.mm in yyyy-mm-dd für SQL
    parsedDate = datetime.strptime(dateInput + "." + year, "%d.%m.%Y")
    return parsedDate.strftime("%Y-%m-%d")

def main():
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
                         WHERE DATE(timestamp) = ?; 
                         """

        # Feinstaubabfrage
        queryPmAvg = """
                     SELECT AVG(P1) AS P1,
                            AVG(P2) AS P2
                     FROM measurementValuesParticulate
                     WHERE DATE(timestamp) = ?
                     GROUP BY sensorID; 
                     """

        temperaturQuery = pd.read_sql_query(queryTempStats, connection, params=(formattedDate,))

        pmQuery = pd.read_sql_query(queryPmAvg, connection, params=(formattedDate,))

        if not temperaturQuery.empty:
            temp_row  = temperaturQuery.iloc[0]
            print(f"\nTemperatur am {dateInput}.{year}:")
            print(f"  Maximale Temperatur: {temp_row['maxTemperatur']} °C")
            print(f"  Minimale Temperatur: {temp_row['minTemperatur']} °C")
            print(f"  Durchschnittliche Temperatur: {round(temp_row['durchschnittlicheTemperatur'], 2)} °C")
        else:
            print("\nKeine Temperaturdaten für dieses Datum gefunden.")

        if not pmQuery.empty:

            pm_row = pmQuery.mean()

            for index, pm_row in pmQuery.iterrows():
                print(f"")
                print(f"Durchschnittliche Feinstaubwerte:")
                print(f"  P1 = {round(pm_row['P1'], 2)}")
                print(f"  P2 = {round(pm_row['P2'], 2)}")
        else:
            print("\nKeine Feinstaubdaten für dieses Datum gefunden.")

        # Objekt Wetterstation
        weatherDatas = measurementValuesWeather(
        temp_row['maxTemperatur'],
        temp_row['minTemperatur'],
        round(temp_row['durchschnittlicheTemperatur'], 2)
        )

        # Objekt Feinstaubsensor
        particualteDatas = measurementValuesParticulate(
        pm_row['P1'],
        pm_row['P2'],
        )

        # Objekt korrekt ausgeben
        print("Das Objekt:", weatherDatas, particualteDatas)

    finally:
         connection.close()

if __name__ == "__main__":
    main()

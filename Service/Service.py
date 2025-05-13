import re
import sqlite3
from datetime import datetime
import pandas as pd
from Model.MeasurementValuesParticulate import measurementValuesParticulate
from Model.MeasurementValuesWeather import measurementValuesWeather

dbRoot = "../Model/feinstaubDB.sqlite"
year = "2022"
inputDateMessage = "Bitte gib ein Datum ein (dd.mm): "

# Liste für Objekte
weatherDataList = []
particulateDataList = []

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


def formatToSqlDate(dateInput):
    # Konvertiere dd.mm in yyyy-mm-dd für SQL
    parsedDate = datetime.strptime(dateInput + "." + year, "%d.%m.%Y")
    return parsedDate.strftime("%Y-%m-%d")


def getMeasurementValuesParticulate():
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

        # Feinstaubabfrage
        queryPmAvg = """
                     SELECT AVG(P1) AS avgP1,
                            AVG(P2) AS avgP2,
                            MAX(P1) AS maxP1,
                            MAX(P2) AS maxP2,
                            MIN(P1) AS minP1,
                            MIN(P2) AS minP2
                     FROM measurementValuesParticulate
                     WHERE DATE(timestamp) = ?
                     GROUP BY sensorID; \
                     """

        temperaturQuery = pd.read_sql_query(queryTempStats, connection, params=(formattedDate,))

        pmQuery = pd.read_sql_query(queryPmAvg, connection, params=(formattedDate,))

        if not temperaturQuery.empty:
            temp_row = temperaturQuery.iloc[0]
            print(f"\nTemperatur am {dateInput}.{year}:")
            print(f"  Maximale Temperatur: {temp_row['maxTemperatur']} °C")
            print(f"  Minimale Temperatur: {temp_row['minTemperatur']} °C")
            print(f"  Durchschnittliche Temperatur: {round(temp_row['durchschnittlicheTemperatur'], 2)} °C")
        else:
            print("\nKeine Temperaturdaten für dieses Datum gefunden.")

        if not pmQuery.empty:

            pm_row = pmQuery.mean()

            for index, pm_row in pmQuery.iterrows():
                print(f"\nDurchschnittliche Feinstaubwerte:\n")
                print(f"  Durchschnittliche Feinstaubkonzentration  PM10 = {round(pm_row['avgP1'], 2)} µg/m³")
                print(f"  Durchschnittliche Feinstaubkonzentration  PM2,5 = {round(pm_row['avgP2'], 2)} µg/m³\n\n")
                print(f"  Maximale Feinstaubkonzentration  PM10 = {round(pm_row['maxP1'], 2)} µg/m³")
                print(f"  Minimale Feinstaubkonzentration  PM10 = {round(pm_row['minP1'], 2)} µg/m³\n\n")
                print(f"  Maximale Feinstaubkonzentration  PM2,5 = {round(pm_row['maxP2'], 2)} µg/m³")
                print(f"  Minimale Feinstaubkonzentration  PM2,5 = {round(pm_row['minP2'], 2)} µg/m³")

            else:
                print("")

        # Objekt Wetterstation
        weatherDatas = measurementValuesWeather(
            temp_row['maxTemperatur'],
            temp_row['minTemperatur'],
            round(temp_row['durchschnittlicheTemperatur'], 2))

        # Objekt Feinstaubsensor
        particualteDatas = measurementValuesParticulate(
            round(pm_row['maxP1'], 2),
            round(pm_row['minP1'], 2),
            round(pm_row['avgP1'], 2),
            round(pm_row['maxP2'], 2),
            round(pm_row['minP2'], 2),
            round(pm_row['avgP2'], 2)
        )

        # Speicherung der Objekte in Array
        particulateDataList.append(particualteDatas)
        weatherDataList.append(weatherDatas)

        # Objekt korrekt ausgeben
        print("Das Objekt:\n", weatherDatas, particualteDatas)

    finally:
        connection.close()

if __name__ == "__main__":
    getMeasurementValuesParticulate()

    getMeasurementValuesParticulate()

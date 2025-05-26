import os
import re
import sqlite3
from datetime import datetime
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))     # …/Service
dbRoot   = os.path.join(BASE_DIR, '..', 'Model', 'feinstaubDB.sqlite')

year = "2022"
inputDateMessage = "Bitte gib ein Datum ein (dd.mm): "

particulateDataList = []

# Validiert das Eingabedatum
def getValidDate():
    # Eingaben validieren im Format dd.mm
    DATE_REGEX = r"^\d{2}\.\d{2}$"

    while True:
        dateInput = input(inputDateMessage).strip()
        if len(dateInput) == 5 and re.match(DATE_REGEX, dateInput):
                datetime.strptime(dateInput + "." + year, "%d.%m.%Y")
                return dateInput
        else:
            print("Ungültige Eingabe. Bitte verwende das Format dd.mm (z.B. 08.02).")

# Konvertiere dd.mm in yyyy-mm-dd für SQL
def formatToSqlDate(dateInput):
    # Konvertiere dd.mm in yyyy-mm-dd für SQL
    parsedDate = datetime.strptime(dateInput + "." + year, "%d.%m.%Y")
    return parsedDate.strftime("%Y-%m-%d")

def getMeasurementValuesParticulate():
    global row, pm_row, temp_row, connection

    from Model.MeasurementValuesParticulate import measurementValuesParticulate
    dateInput = getValidDate()
    formattedDate = formatToSqlDate(dateInput)

    try:
        connection = sqlite3.connect(dbRoot)

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
                     """

        pmQuery = pd.read_sql_query(queryPmAvg, connection, params=(formattedDate,))

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

        # Rückgabe des Objekts
        return particualteDatas

        # Objekt korrekt ausgeben
        print("Das Objekt:\n", particualteDatas)


    finally:
        if connection is not None:
            connection.close()
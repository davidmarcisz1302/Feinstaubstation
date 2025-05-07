import sqlite3
import pandas as pd

inputDateOutputMessage = "Bitte gib ein Datum ein (Format:2022-mm-dd): "
dbRoot = "../Model/feinstaubDB.sqlite"


# Verbindung zur SQLite-Datenbank
connection = sqlite3.connect(dbRoot)


# Konsole
dateInput = input(inputDateOutputMessage)

inputDateOutputMessage = "Bitte gib ein Datum ein (Format: yyyy-mm-dd): "

# Abfrage: Max, Min, Durchschnittstemperatur für ein bestimmtes Datum
queryTempStats = """
                 SELECT
                     DATE(timestamp) AS date,
                     MAX(temperature) AS maxTemperatur,
                     MIN(temperature) AS minTemperatur,
                     AVG(temperature) AS durchschnittlicheTemperatur 
                 FROM measurementValuesWeather
                 WHERE DATE(timestamp) = ?; \
                 """

# Abfrage: Durchschnittliche P1 und P2 pro Sensor für ein bestimmtes Datum
queryPmAvg = """
             SELECT
                 sensorID,
                 AVG(P1) AS avgP1,
                 AVG(P2) AS avgP2
             FROM measurementValuesParticulate
             WHERE DATE(timestamp) = ?
             GROUP BY sensorID; \
             """

# QUERYS Ausführen
#
# @pd.read_sql_query() (panda)
# DataFrame zu speichern. Der DataFrame ist eine tabellarische Datenstruktur,
# die Spalten und Zeilen enthält
#
temperaturQuery = pd.read_sql_query(queryTempStats, connection, params=(dateInput,)) # Parameter date um den Platzhalter "?" zu ersetzen.
pmQuery = pd.read_sql_query(queryPmAvg, connection, params=(dateInput,))
# Ergebnisse ausgeben
print(f"Die Temperatur am {dateInput} betrug")
print(temperaturQuery)

print(f"\nAverage particulate matter per sensor on {dateInput}:")
print(pmQuery)

# Verbindung schließen
connection.close()

# Datenbank
import sqlite3

# Verbindung zur SQLite-Datenbank herstellen (erstellt die Datei, falls sie nicht existiert)
conn = sqlite3.connect("feinstaubDB.sqlite")

# Cursor-Objekt zum Ausführen von SQL-Befehlen erstellen
cursor = conn.cursor()

# Tabelle Messgerät
cursor.execute("""
CREATE TABLE IF NOT EXISTS device (
    deviceID INTEGER PRIMARY KEY AUTOINCREMENT,
    model VARCHAR(50) NOT NULL,
    location VARCHAR(50) NOT NULL
)
""")

# Tabelle Sensor
cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor (
    sensorID INTEGER PRIMARY KEY AUTOINCREMENT,
    sensorType VARCHAR(30) NOT NULL,
    status BOOLEAN DEFAULT TRUE NOT NULL,
    deviceID INTEGER NOT NULL,
    FOREIGN KEY (deviceID) REFERENCES device(deviceID) ON DELETE CASCADE
)
""")

# Tabelle Messwerte
cursor.execute("""
CREATE TABLE IF NOT EXISTS measurementValuesParticulate (
    measurementID INTEGER PRIMARY KEY AUTOINCREMENT,
    sensorID INTEGER NOT NULL,
    timestamp DATETIME NOT NULL,
    PM2_5 DECIMAL(6,3),
    PM10Wert DECIMAL(6,3),
    FOREIGN KEY (sensorID) REFERENCES sensor(sensorID) ON DELETE CASCADE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS measurementValuesWeather (
    measurementID INTEGER PRIMARY KEY,
    sensorID INTEGER NOT NULL UNIQUE,
    timestamp DATETIME NOT NULL,
    temperature DECIMAL(5,2),
    humidity DECIMAL(5,2),
    FOREIGN KEY (sensorID) REFERENCES sensor(sensorID)
)
""")

# Änderungen speichern und Verbindung schließen
conn.commit()
conn.close()


def sqlite():
    return None
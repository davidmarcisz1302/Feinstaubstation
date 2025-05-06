# Datenbank
import sqlite3

dht22_path = "dht22_combined.csv"
sds011_path = "sds011_combined.csv"
conn = sqlite3.connect("feinstaubDB.sqlite")

# Cursor-Objekt
cursor = conn.cursor()

# Tabelle Messgerät
cursor.execute("""
CREATE TABLE IF NOT EXISTS location (
    locationID INTEGER PRIMARY KEY,
latitude DECIMAL(9,6) NOT NULL,
longitude DECIMAL(9,6) NOT NULL
);
               """)

# Tabelle Gerät
cursor.execute("""
               CREATE TABLE IF NOT EXISTS device (
                deviceID INTEGER PRIMARY KEY AUTOINCREMENT,
                model VARCHAR(50) NOT NULL,
                locationID INTEGER NOT NULL,
                FOREIGN KEY (locationID) REFERENCES location(locationID) ON DELETE CASCADE
                )
               """)


# Tabelle Sensor
cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor (
    sensorID INTEGER PRIMARY KEY,
    sensorType VARCHAR(30) NOT NULL,
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
    P1 DECIMAL(6,2),
    durP1 DECIMAL(6,2),
    ratioP1 DECIMAL(5,2),
    P2 DECIMAL(6,2),
    durP2 DECIMAL(6,2),
    ratioP2 DECIMAL(5,2),
    FOREIGN KEY (sensorID) REFERENCES sensor(sensorID) ON DELETE CASCADE
)
""")

# Tabelle Wetter
cursor.execute("""
CREATE TABLE IF NOT EXISTS measurementValuesWeather (
    measurementID INTEGER PRIMARY KEY AUTOINCREMENT,
    sensorID INTEGER NOT NULL,
    timestamp DATETIME NOT NULL,
    temperature DECIMAL(5,2),
    humidity DECIMAL(5,2),
    FOREIGN KEY (sensorID) REFERENCES sensor(sensorID) ON DELETE CASCADE
)
""")

conn.commit()
conn.close()

def sqlite():
    return None
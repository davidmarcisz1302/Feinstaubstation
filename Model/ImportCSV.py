# Verbindung zur DB
import csv
import sqlite3

from MeasurementValuesWeather.DatabaseModel import dht22_path, sds011_path

conn = sqlite3.connect("feinstaubDB.sqlite")
cursor = conn.cursor()

# Hilfsfunktionen
def persistLocation(lat, lon):
    cursor.execute("SELECT locationID FROM location WHERE latitude=? AND longitude=?", (lat, lon))
    result = cursor.fetchone() # Rückgabe der Zeile
    if result:
        return result[0]
    cursor.execute("INSERT INTO location (latitude, longitude) VALUES (?, ?)", (lat, lon))
    return cursor.lastrowid # *lastrowid gibt nur nach einem INSERT-Befehl eine sinnvolle ID zurück.

def persistDevice(model, location_id):
    cursor.execute("SELECT deviceID FROM device WHERE model=? AND locationID=?", (model, location_id))
    result = cursor.fetchone()
    if result:
        return result[0]
    cursor.execute("INSERT INTO device (model, locationID) VALUES (?, ?)", (model, location_id))
    return cursor.lastrowid

def persistSensor(sensorID, sensorType, device_id):
    cursor.execute("SELECT sensorID FROM sensor WHERE sensorID=?", (sensorID,))
    result = cursor.fetchone()
    if result:
        return result[0]
    cursor.execute("INSERT INTO sensor (sensorID, sensorType, deviceID) VALUES (?, ?, ?)",
                   (sensorID, sensorType, device_id))
    return sensorID

# Import DHT22 
with open(dht22_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        sensorID = int(row['sensorID'])
        sensorType = row['sensorType']
        location = int(row['location'])
        lat = float(row['lat'])
        lon = float(row['lon'])
        timestamp = row['timestamp']
        temperature = float(row['temperature']) if row['temperature'] else None
        humidity = float(row['humidity']) if row['humidity'] else None

        locationID = persistLocation(lat, lon)
        deviceID = persistDevice(f"device_{location}", locationID)
        persistSensor(sensorID, sensorType, deviceID)

        cursor.execute("""
                       INSERT INTO measurementValuesWeather (sensorID, timestamp, temperature, humidity)
                       VALUES (?, ?, ?, ?)
                       """, (sensorID, timestamp, temperature, humidity))

# Import SDS011 
with open(sds011_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        sensorID = int(row['sensorID'])
        sensorType = row['sensorType']
        location = int(row['location'])
        lat = float(row['lat'])
        lon = float(row['lon'])
        timestamp = row['timestamp']
        P1 = float(row['P1']) if row['P1'] else None
        durP1 = float(row['durP1']) if row['durP1'] else None
        ratioP1 = float(row['ratioP1']) if row['ratioP1'] else None
        P2 = float(row['P2']) if row['P2'] else None
        durP2 = float(row['durP2']) if row['durP2'] else None
        ratioP2 = float(row['ratioP2']) if row['ratioP2'] else None

        locationID = persistLocation(lat, lon)
        deviceID = persistDevice(f"device_{location}", locationID)
        persistSensor(sensorID, sensorType, deviceID)

        cursor.execute("""
                       INSERT INTO measurementValuesParticulate (sensorID, timestamp, P1, durP1, ratioP1, P2, durP2, ratioP2)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                       """, (sensorID, timestamp, P1, durP1, ratioP1, P2, durP2, ratioP2))

# Speichern & schließen
conn.commit()
conn.close()

import csv
import datetime
import gzip
import urllib.request
import urllib.error
from pathlib import Path

class CSVGZDownloader2022:
    # class Konstruktor
    def __init__(self, sensorInfos):
        self.sensorURL = "https://archive.sensor.community/2022/"
        self.startDate = datetime.datetime(2022, 1, 1)
        self.endDate = datetime.datetime(2022, 12, 31)
        self.sensorInfos = sensorInfos
        self.outputDir = Path("C:/Entwicklung/Feinstaubprojekt/csv")
        self.outputDir.mkdir(parents=True, exist_ok=True)

    def main(self):
        urls = self.getGzURL()
        self.downloadFiles(urls)
        print("\nAlle .csv.gz Dateien aus 2022 wurden gespeichert in:", self.outputDir)

    def getGzURL(self):
        date = self.startDate
        urls = []
        while date <= self.endDate:
            dateStr = date.strftime("%Y-%m-%d")
            for sensor_type, sensor_id in self.sensorInfos:
                filename = f"{dateStr}_{sensor_type}_sensor_{sensor_id}.csv.gz"
                url = f"{self.sensorURL}{dateStr}/{filename}"
                urls.append((url, filename))
            date += datetime.timedelta(days=1)
        return urls

    def downloadFiles(self, urls):
        for url, filename in urls:
            destPath = self.outputDir / filename
            if destPath.exists():
                print(f" Überspringe (bereits vorhanden): {filename}")
                continue
            try:
                print(f"Downloade: {url}")
                urllib.request.urlretrieve(url, destPath)
            except (urllib.error.HTTPError, urllib.error.URLError) as e:
                print(f"Fehler bei {filename}: {e}")

# Beispiel: SDS011 (3659) & DHT22 (3660)
if __name__ == "__main__":
    sensorList = [("sds011", 3659), ("dht22", 3660)]
    downloader = CSVGZDownloader2022(sensorList)
    downloader.main()


import gzip
import csv
from pathlib import Path

def extract_and_split_by_sensor(input_dir, output_dir):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Starte das Entpacken und Aufteilen nach Sensortyp...")

    writers = {}
    files = {}
    headers_written = {}

    for gz_file in sorted(input_dir.glob("*.csv.gz")):
        try:
            with gzip.open(gz_file, 'rt', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)
                for row in reader:
                    if len(row) < 2:
                        continue  # Leere oder fehlerhafte Zeile
                    sensor_type = row[1].lower()  # z.B. 'sds011' oder 'dht22'
                    if sensor_type not in writers:
                        output_path = output_dir / f"{sensor_type}_2022.csv"
                        file = open(output_path, mode='w', newline='', encoding='utf-8')
                        writer = csv.writer(file)
                        writer.writerow(header)
                        writers[sensor_type] = writer
                        files[sensor_type] = file
                        headers_written[sensor_type] = True
                    writers[sensor_type].writerow(row)
        except Exception as e:
            print(f"Fehler beim Verarbeiten von {gz_file.name}: {e}")

    # Alle Dateien schließen
    for file in files.values():
        file.close()

    print("Aufteilen abgeschlossen. Dateien gespeichert in:", output_dir)


extract_and_split_by_sensor(
    input_dir="C:/Entwicklung/Feinstaubprojekt/csv",
    output_dir="C:/Entwicklung/Feinstaubprojekt/ausgabe"
)

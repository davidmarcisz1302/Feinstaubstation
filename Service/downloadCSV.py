import datetime
import urllib.request
import urllib.error
from pathlib import Path

class CSVGZDownloader2022:
    def __init__(self, sensorInfos):
        self.sensorURL = "https://archive.sensor.community/2022/"
        self.startDate = datetime.datetime(2022, 1, 1)
        self.endDate = datetime.datetime(2022, 12, 31)
        self.sensorInfos = sensorInfos  # z. B. [("sds011", 3659), ("dht22", 3660)]
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
            dest_path = self.outputDir / filename
            if dest_path.exists():
                print(f" Überspringe (bereits vorhanden): {filename}")
                continue
            try:
                print(f"Downloade: {url}")
                urllib.request.urlretrieve(url, dest_path)
            except (urllib.error.HTTPError, urllib.error.URLError) as e:
                print(f"Fehler bei {filename}: {e}")

# Beispiel: SDS011 (3659) & DHT22 (3660)
if __name__ == "__main__":
    sensorList = [("sds011", 3659), ("dht22", 3660)]
    downloader = CSVGZDownloader2022(sensorList)
    downloader.main()

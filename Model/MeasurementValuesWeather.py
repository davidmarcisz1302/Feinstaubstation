class measurementValuesWeather:
    def __init__(self, maxTemp, minTemp, avgTemp):
        self.maxTemp = maxTemp
        self.minTemp = minTemp
        self.avgTemp = avgTemp

    # Getter-Methoden
    def getMaxTemp(self):
        return self.maxTemp

    def getMinTemp(self):
        return self.minTemp

    def getAvgTemp(self):
        return self.avgTemp

    # Setter-Methoden
    def setMaxTemp(self, value):
        self.maxTemp = value

    def setMinTemp(self, value):
        self.minTemp = value

    def setAvgTemp(self, value):
        self.avgTemp = value

    def __str__(self):
        return f"\nMax: {self.maxTemp} °C\nMin: {self.minTemp} °C´\nDurchschnitt: {self.avgTemp} °C\n\n"
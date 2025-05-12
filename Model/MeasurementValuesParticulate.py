class measurementValuesParticulate:
    def __init__(self, maxP1, minP1, avgP1, maxP2, minP2, avgP2):
        self.maxP1 = maxP1
        self.minP1 = minP1
        self.avgP1 = avgP1
        self.maxP2 = maxP2
        self.minP2 = minP2
        self.avgP2 = avgP2

    # Getter und Setter P1
    def getMaxP1(self):
        return self.maxP1

    def setMaxP1(self, value):
        self.maxP1 = value

    def getMinP1(self):
        return self.minP1

    def setMinP1(self, value):
        self.minP1 = value

    def getAvgP1(self):
        return self.avgP1

    def setAvgP1(self, value):
        self.avgP1 = value

    # Getter und Setter P2
    def getMaxP2(self):
        return self.maxP2

    def setMaxP2(self, value):
        self.maxP2 = value

    def getMinP2(self):
        return self.minP2

    def setMinP2(self, value):
        self.minP2 = value

    def getAvgP2(self):
        return self.avgP2

    def setAvgP2(self, value):
        self.avgP2 = value

    def __str__(self):
        return (
            f"Feinstaub Messwerte:\n"
            f"Maximale Feinstaubkonzentration  PM10 = {self.maxP1}µg/m³\n"
            f"Minimale Feinstaubkonzentration  PM10 = {self.minP1}µg/m³\n"
            f"Durchschnittliche Feinstaubkonzentration  PM10 = {self.avgP1}µg/m³\n\n"
            f"Maximale Feinstaubkonzentration  PM2,5 = {self.maxP2}µg/m³\n"
            f"Minimale Feinstaubkonzentration  PM2,5 = {self.minP2}µg/m³\n"
            f"Durchschnittliche Feinstaubkonzentration  PM2,5 = {self.avgP2}µg/m³\n"
            f")"
        )

class measurementValuesWeather:
    def __init__(self, max_temp, min_temp, avg_temp):
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.avg_temp = avg_temp

    def __str__(self):
        return f"Max: {self.max_temp} °C, Min: {self.min_temp} °C, Durchschnitt: {self.avg_temp} °C"

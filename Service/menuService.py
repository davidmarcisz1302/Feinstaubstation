import re
import sys

MENU_INPUT_REGEX = r"^[0-3]$"

# Validierung der Benutzereingabe
def validateMenuInputUser(inputUser):
    while True:
        if re.match(MENU_INPUT_REGEX, inputUser):
            return

        else:
            print("Ungültige Eingabe. Bitte gebe eine Zahl von 0-3 ein")
            inputUser = input(": ")

# Menüfunktionen Hauptmenü
def editMainMenuInput(inputUser):
    from View.View import (menuMeasurementValuesParticulateIO, menuMeasurementValuesWeatherIO,
                           menuMeasurementValuesHumidityIO)

    match int(inputUser):
        case 0:
            import sys
            sys.exit(0)
        case 1:
            menuMeasurementValuesParticulateIO()
        case 2:
            menuMeasurementValuesWeatherIO()
        case 3:
            menuMeasurementValuesHumidityIO()
        case _:
            from View.View import mainMenu
            mainMenu()

# Menüfunktionen Feinstaub
def editMeasurementValuesParticulateMenuInput(inputUser):
    match int(inputUser):
        case 0:
            sys.exit(0)
        case 1:
            from Service.measurementParticulateService import getMeasurementValuesParticulate
            # Funktion ausführen (DB Auswertung)
            getMeasurementValuesParticulate()

            # Graph generieren (überträgt Datum)
            from Service.createGraphParticulateMatter import fetchParticulateMatterForDate
            fetchParticulateMatterForDate()

        case 2:
            from Service.measurementParticulateService import getMeasurementValuesParticulate

            obj1 = getMeasurementValuesParticulate()
            obj2 = getMeasurementValuesParticulate()

            print("\n1Objekte:\n", obj1, obj2)

        case 3:
            from View.View import mainMenu
            mainMenu()
        case _:
            from View.View import mainMenu
            mainMenu()

# Menüfunktionen Temperatur
def editMeasurementValuesWeatherMenuInput(inputUser):
    match int(inputUser):
        case 0:
            sys.exit(0)
        case 1:
            from Service.measurementValuesWeatherService import getMeasurementValuesWeather
            getMeasurementValuesWeather()

            # Graph generieren (überträgt Datum)
            from Service.createGraphWeather import fetchMeasurementValuesWeatherForDate
            fetchMeasurementValuesWeatherForDate()

        case 2:
            from Service.measurementValuesWeatherService import getMeasurementValuesWeather
            getMeasurementValuesWeather()
            getMeasurementValuesWeather()
        case 3:
            from View.View import mainMenu
            mainMenu()
        case _:
            from View.View import mainMenu
            mainMenu()

def editMeasurementValuesHumidityInput(inputUser):
    match int(inputUser):
        case 0:
            sys.exit(0)
        case 1:
            from Service.measurementValuesHumidity import getMeasurementValuesHumidity
            getMeasurementValuesHumidity()
        case 2:
            from View.View import mainMenu
            mainMenu()
        case _:
            from View.View import mainMenu
            mainMenu()
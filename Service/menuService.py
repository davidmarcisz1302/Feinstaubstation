import re
import sys

from View.View import menuMeasurementValuesParticulateIO, menuMeasurementValuesWeatherIO, menuMeasurementValuesHumidityIO, mainMenu

MENU_INPUT_REGEX = r"^[0-4]$"

# Validierung der Benutzereingabe
def validateMenuInputUser(inputUser):
    while True:
        if re.match(MENU_INPUT_REGEX, inputUser):
            return

        else:
            print("Ungültige Eingabe. Bitte gebe eine Zahl von 0-4 ein")
            inputUser = input(": ")

# Menüfunktionen Hauptmenü
def editMainMenuInput(inputUser):
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
            mainMenu()

# Menüfunktionen Feinstaub
def editMeasurementValuesParticulateMenuInput(inputUser):
    match int(inputUser):
        case 0:
            sys.exit(0)
        case 1:
            menuMeasurementValuesParticulateIO()
        case 2:
            menuMeasurementValuesWeatherIO()
        case 3:
            menuMeasurementValuesHumidityIO()
        case _:
            mainMenu()

# Menüfunktionen Temperatur
def editMeasurementValuesWeatherMenuInput(inputUser):
    match int(inputUser):
        case 0:
            sys.exit(0)
        case 1:
            menuMeasurementValuesParticulateIO()
        case 2:
            menuMeasurementValuesWeatherIO()
        case 3:
            menuMeasurementValuesHumidityIO()
        case _:
            mainMenu()
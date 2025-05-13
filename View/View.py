displayInput = ":"

# Hauptmenü
def mainMenu():
    print("=" * 70)
    print("🌫️  Willkommen bei der Feinstaubstation  🌫️".center(70))
    print("=" * 70)
    print()
    # Hauptmenü
    print("\n" + "=" * 40)
    print("🌫️  Feinstaubstation – Hauptmenü  🌫️\n" + "=" * 40 + """
    1. Feinstaubdaten anzeigen
    2. Temperaturdaten anzeigen
    3. Luftfeuchtigkeitsdaten anzeigen
    0. Programm beenden
    """ + "=" * 40)

    # Benutzereingabe und validierung
    inputUser = input(displayInput)
    from Service.menuService import validateMenuInputUser, editMainMenuInput
    validateMenuInputUser(inputUser)
    editMainMenuInput(inputUser)

    # Weiterleitung der Menübereiche
    editMainMenuInput(inputUser)

def menuMeasurementValuesParticulateIO():
    # Feinstaub-Menü
    print("\n" + "=" * 40)
    print("🌫️  Feinstaub – Menü  🌫️\n" + "=" * 40 + """
    1. Feinstaubwerte nach Datum anzeigen
    2. Zwei Feinstaubwerte vergleichen
    3. Durchschnittliche Feinstaubbelastung im Jahr
    4. Zurück zum Hauptmenü
    0. Programm beenden
    """ + "=" * 40)

    # Benutzereingabe und validierung
    inputUser = input(displayInput)
    from Service.menuService import validateMenuInputUser, editMeasurementValuesParticulateMenuInput
    validateMenuInputUser(inputUser)

    # Weiterleitung der Menübereiche
    editMeasurementValuesParticulateMenuInput(inputUser)

def menuMeasurementValuesWeatherIO():
    # Temperatur-Menü
    print("\n" + "=" * 40)
    print("🌫️  Temperatur – Menü  🌫️\n" + "=" * 40 + """
    1. Temperatur nach Datum anzeigen
    2. Zwei Temperaturwerte vergleichen
    3. Durchschnittstemperatur im Jahr
    4. Zurück zum Hauptmenü
    0. Programm beenden
    """ + "=" * 40)

    # Benutzereingabe und validierung
    inputUser = input(displayInput)
    from Service.menuService import validateMenuInputUser, editMeasurementValuesWeatherMenuInput
    validateMenuInputUser(inputUser)

    # Weiterleitung der Menübereiche
    editMeasurementValuesWeatherMenuInput(inputUser)

def menuMeasurementValuesHumidityIO():
    print("\n" + "=" * 40)
    # Luftfeuchtigkeits-Menü
    print("\n" + "=" * 40)
    print("🌫️  Luftfeuchtigkeit – Menü  🌫️\n" + "=" * 40 + """
    1. Luftfeuchtigkeit nach Datum anzeigen
    2. Zwei Luftfeuchtigkeitswerte vergleichen
    3. Durchschnittliche Luftfeuchtigkeit im Jahr
    4. Zurück zum Hauptmenü
    0. Programm beenden
    """ + "=" * 40)

    # Benutzereingabe und validierung
    inputUser = input(displayInput)
    from Service.menuService import validateMenuInputUser
    validateMenuInputUser(inputUser)

    # Weiterleitung der Menübereiche

# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 13:51:27 2024

@author: simulator
"""

import ephem
from datetime import datetime

def mond_info(datum, latitude=0.0, longitude=0.0):
    """
    Berechnet Mondinformationen basierend auf dem Datum und den Koordinaten.
    
    Parameter:
    - datum (str): Datum im Format 'YYYY-MM-DD HH:MM:SS' (z.B. '2023-10-10 22:00:00').
    - latitude (float): Breite des Standorts (Standard: 0.0 für Äquator).
    - longitude (float): Länge des Standorts (Standard: 0.0 für den Nullmeridian).
    
    Rückgabe:
    - Dikt mit Mondinformationen (Phase, Beleuchtung, Azimut, Höhe).
    """
    
    # Standort und Datum festlegen
    observer = ephem.Observer()
    observer.lat, observer.lon = str(latitude), str(longitude)
    observer.date = datum
    
    # Mondobjekt erstellen
    mond = ephem.Moon(observer)
    
    # Mondphase und Beleuchtung berechnen
    illumination = mond.phase  # Beleuchtung des Mondes in Prozent
    azimuth = mond.az  # Azimut des Mondes (Position in Grad vom Norden aus)
    altitude = mond.alt  # Höhe des Mondes (in Grad über dem Horizont)
    
    # Mondalter (Zeit seit Neumond) und Distanz zur Erde
    age = observer.date - ephem.previous_new_moon(observer.date)  # in Tagen
    distance = mond.earth_distance * 384400  # Entfernung in km, 384400 km als Durchschnitt
    
    # Ausgabe zusammenstellen
    info = {
        "Datum": datum,
        "Latitude": latitude,
        "Longitude": longitude,
        "Beleuchtung (%)": illumination,
        "Azimut (Grad)": azimuth * (180 / 3.14159),  # von Radiant in Grad
        "Höhe (Grad)": altitude * (180 / 3.14159),   # von Radiant in Grad
        "Mondalter (Tage)": age,
        "Entfernung (km)": distance
    }
    
    return info

# Beispiel für die Verwendung des Skripts
datum = "2011-02-07 00:45:00"  # Beispiel-Datum
latitude = 30.342  # Beispiel: München, Breitengrad
longitude = -87.039  # Beispiel: München, Längengrad

mond_daten = mond_info(datum, latitude, longitude)
print(mond_daten)

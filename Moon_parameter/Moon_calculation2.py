# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 14:06:02 2024

@author: simulator
"""

import ephem
from datetime import datetime, timedelta

def finde_datum_fuer_beleuchtung(target_illumination, latitude=0.0, longitude=0.0, start_date=None, tolerance=0.5):
    """
    Findet das Datum und die Position (Azimut und Höhe), an dem der Mond eine bestimmte Beleuchtung erreicht.
    
    Parameter:
    - target_illumination (float): Gewünschte Mondbeleuchtung in Prozent (0 bis 100).
    - latitude (float): Breitengrad des Standorts.
    - longitude (float): Längengrad des Standorts.
    - start_date (str): Optionales Startdatum im Format 'YYYY-MM-DD HH:MM:SS'.
    - tolerance (float): Toleranz für die Beleuchtung (%), z.B. 0.5 für +/- 0,5%.
    
    Rückgabe:
    - Dikt mit Datum, Uhrzeit, Beleuchtung, Azimut und Höhe des Mondes.
    """
    
    # Startdatum festlegen
    if start_date is None:
        date = datetime.utcnow()
    else:
        date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    
    # Standort festlegen
    observer = ephem.Observer()
    observer.lat, observer.lon = str(latitude), str(longitude)
    
    # Iterative Suche
    step = timedelta(hours=1)  # Suchschritt auf 1 Stunde einstellen
    closest_date = date
    closest_illumination_diff = float('inf')
    closest_azimuth = None
    closest_elevation = None
    closest_illumination = None
    
    for _ in range(365 * 24):  # Schleife für maximal 30 Tage (30 * 24 Stunden)
        observer.date = date
        mond = ephem.Moon(observer)
        
        # Beleuchtung berechnen
        illumination = mond.phase  # Beleuchtung in Prozent
        azimuth = mond.az * (180 / 3.14159)  # Azimut in Grad
        elevation = mond.alt * (180 / 3.14159)  # Höhe in Grad
        
        # Prüfen, ob die Beleuchtung innerhalb der Toleranz liegt
        illumination_diff = abs(illumination - target_illumination)
        if illumination_diff < closest_illumination_diff:
            closest_illumination_diff = illumination_diff
            closest_date = date
            closest_azimuth = azimuth
            closest_elevation = elevation
            closest_illumination = illumination
        
        if illumination_diff <= tolerance:
            # Wenn wir innerhalb der Toleranz sind, abbrechen
            break
        
        # Datum anpassen: vorwärts oder rückwärts
        if illumination < target_illumination:
            date += step
        else:
            date -= step
    
    # Rückgabe des nächsten Datums mit der gewünschten Beleuchtung und Position
    return {
        "Datum": closest_date.strftime('%Y-%m-%d %H:%M:%S'),
        "Beleuchtung (%)": closest_illumination,
        "Azimut (Grad)": closest_azimuth,
        "Höhe (Grad)": closest_elevation
    }

# Beispiel für die Verwendung des Skripts
target_illumination = 76 # Zielbeleuchtung in Prozent
latitude = 33.5  # Beispiel: München, Breitengrad
longitude = -111.6  # Beispiel: München, Längengrad
start_date = "2010-01-01 00:00:00" 

mond_daten = finde_datum_fuer_beleuchtung(target_illumination, latitude, longitude, start_date)
print(mond_daten)

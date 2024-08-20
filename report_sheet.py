# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 12:35:24 2024

@author: simulator
"""

import os
import json
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader


def create_comparison_table(QTG_path):
    for dirpath, dirnames, filenames in os.walk(QTG_path):
        for file in filenames:
            if 'FTD1_log_init_cond' in file:
                file_path = os.path.join(dirpath, file)
                with open(file_path, 'r') as json_file:
                    Init_cond = json.load(json_file)
            if 'Reference_init_cond' in file:
                print(file)
                file_path = os.path.join(dirpath, file)
                with open(file_path, 'r') as json_file:
                    Ref_Init_cond = json.load(json_file)

    # Erstellen der Tabellendaten
    table_data = [
        ["Parameter [UoM]", "Reference*", "FSTD"],
        ["Mass Properties", "", ""]
    ]

    # Werte aus dict1 und dict2 zusammenführen
    for key in Ref_Init_cond:
        table_data.append([key, Ref_Init_cond[key], Init_cond.get(key, "")])
        if key == "Moment of Inertia ZZ":
            table_data.append(["Environment Parameters", "", ""])
        if key == "Wind Speed":
            table_data.append(["Flight Parameters", "", ""])

    # DataFrame für die Tabelle erstellen
    df = pd.DataFrame(table_data)    # HTML(string=html_out).


    # Erstellen der Tabelle mit matplotlib
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=None, cellLoc='center', loc='center')

    # Zellen-Formatierung
    for i, key in enumerate(table_data):
        if key[0] in ["Parameter [UoM]", "Mass Properties", "Environment Parameters", "Flight Parameters"]:
            for j in range(3):
                cell = table[(i, j)]
                cell.set_facecolor('lightgray')
                cell.set_text_props(ha='center', weight='bold')

    for key, cell in table.get_celld().items():
        cell.set_height(0.05)

        # Tabelle in PDF speichern
    table_path = os.path.join(QTG_path, "0_Init_cond_table.pdf")
    with PdfPages(table_path) as pdf:
        pdf.savefig(fig, bbox_inches='tight')

    print(f"Tabelle erfolgreich als {table_path} gespeichert.")


if __name__ == "__main__":
    QTG_path = r'Pfad eingeben'
    create_comparison_table(QTG_path)

"""
Hi i brauch dei Hilfe :)
    1. Oben siesht a function, welche a tabelle als PDF erstellt. Es funktioniert zwar (siehe foto), ist aber ein pfusch. Bitte neu machen
    vlt sogar mit html? Die Werte und namen welche in der Tabelle sind, kommen aus einem dict, welches in ein JSON File gespeichert sind.
    Dies wird am Anfang der Funktion geladen. BTW, das ist die Tabelle der initial conditions.
    2. Es fehlen auch noch die Einheiten, bitte eine dritte spalten mit Units hinzufuegen. Die units kannst du aus dem MQTG 
    vom FTD3 entnehmen.
    3. Ich brauche noch den Report eines QTGs. Als BSP. hab i dir den Ordner von einem einzigen QTG (1.c.(1)_A1) mitgeschickt,
    welchen ich erstellt habe.
    Als Vorlage kannst du das Reiser MQTG nehmen. Es sollte moeglichst gleich aussehen. Die Plots habi schon, brauchst also net 
    machen. Also nur das vom Anfang eines QTGs bis einschließlich der Notes und Rationales tabelle.
    
    Die Texte und tabllen kann ich dann selbst ausfuellen du muesstest mir eine sozusagen eine Vorlage machen.
    Unten siehst du noch die Variablen, welche als Titel fuer die einzelnen Tests dienen.
    
    
    Danke 
    
    
   
"""

# Engine Assessments

# Take-off
d1c1A1 = " Take Off-All Engines-CAT A on Runway"  # 1
d1c2A1 = " Take Off-OEI CAT A on Runway"  # 2

# Hover Performance
d1d1A1 = " Light GW - 3ft AGL"
d1d1A2 = " Light GW - 10ft AGL"
d1d1A3 = " Light GW - 25ft AGL"
d1d1A4 = " Light GW - 70ft AGL"
d1d1B1 = " Heavy GW - 3ft AGL"
d1d1B2 = " Heavy GW - 10ft AGL"
d1d1B3 = " Heavy GW - 25ft AGL"
d1d1B4 = " Heavy GW - 70ft AGL"

# Vertical climb Performance
d1e1A1 = " Light GW - AEO TOP"
d1e1B1 = " Heavy GW - AEO MCP"

# Level flight  Performance and Trimmed Flight Condition
# Info:
# VH Maximum speed in level flight at maximum continuous power.
d1f1A1 = " Light GW - VY"
d1f1A2 = " Light GW - VH"
d1f1B1 = " Heavy GW - VY"
d1f1B2 = " Heavy GW - VH"

# Climb Performance and Trimmed Flight Control Position
# Info:
# MCP = Maximum continuous power
# TOP = Take off Power
d1g1A1 = " Light GW - AEO MCP VY"
d1g1A2 = " Light GW - AEO TOP VY"
d1g1A3 = " Light GW - OEI MCP VY"
d1g1A4 = " Light GW - OEI 2MIN VTOSS"
d1g1B1 = " Heavy GW - AEO MCP VY"
d1g1B2 = " Heavy GW - AEO TOP VY"
d1g1B3 = " Heavy GW - OEI MCP VY"
d1g1B4 = " Heavy GW - OEI 2MIN VTOSS"

# Descent Performance and Trimmed Flight Control Position
d1h1A1 = " Light GW - 90KIAS -1000fpm"
d1h1B1 = " Heavy GW - 90KIAS -1000fpm"

# Landing
d1j1A1 = " Landing - All Enignes CAT A"

d1j2A1 = " OEI TM - CAT A"
d1j2A2 = " OEI TM - CAT B"

# ----Handling Qualities

# Cycliv Force vs Position
d2a1A1 = " Cyclic Longitudinal - Trim ON"
d2a1A2 = " Cyclic Longitudinal - Trim OFF"
d2a1B1 = " Cyclic Lateral - Trim ON"
d2a1B2 = " Cyclic Lateral - Trim OFF"

# Collective/Pedals Force vs Position
d2a2A1 = " Collective - Trim ON"
d2a2B1 = " Pedals - Trim ON"

# Trim System Rate
d2a4A1 = " Longitudinal Cyclic - ATRIM"
d2a4B1 = " Lateral Cyclic - ATRIM"

# Longitudinal Static Stability
d2c2A1 = " Cruise Trim Speed Up - 120 KIAS, Trim Speed"
d2c2A2 = " Cruise Trim Speed Up - 125 KIAS"
d2c2A3 = " Cruise Trim Speed Up - 130 KIAS"
d2c2B1 = " Cruise Trim Speed Down - 120 KIAS, Trim Speed"
d2c2B2 = " Cruise Trim Speed Down - 115 KIAS"
d2c2B3 = " Cruise Trim Speed Down - 110 KIAS"
d2c2C1 = " Autorotation Trim Speed Up - 75 KIAS, Trim Speed"
d2c2C2 = " Autorotation Trim Speed Up - 85 KIAS"
d2c2C3 = " Autorotation Trim Speed Up - 90 KIAS"
d2c2D1 = " Autorotation Trim Speed Up - 75 KIAS, Trim Speed"
d2c2D2 = " Autorotation Trim Speed Up - 65 KIAS"
d2c2D3 = " Autorotation Trim Speed Up - 55 KIAS"

# Manoeuvring Stability
d2c4A1 = " Right Turn, Vy, 0 Bank"
d2c4A2 = " Right Turn, Vy, 30 Bank"
d2c4A3 = " Right Turn, Vy, 45 Bank"
d2c4B1 = " Left Turn, Vy, 0 Bank"
d2c4B2 = " Left Turn, Vy, 30 Bank"
d2c4B3 = " Left Turn, Vy, 45 Bank"
d2c4C1 = " Right Turn, 120 KIAS, 0 Bank"
d2c4C2 = " Right Turn, 120 KIAS, 30 Bank"
d2c4C3 = " Right Turn, 120 KIAS, 45 Bank"
d2c4D1 = " Left Turn, 120 KIAS, 0 Bank"
d2c4D2 = " Left Turn, 120 KIAS, 30 Bank"
d2c4D3 = " Left Turn, 120 KIAS, 45 Bank"

# Diractional static stability
d2d2A1 = " Mid Speed, 100 KIAS"
d2d2A2 = " Mid Speed, 100 KIAS Right Sideslip 1"
d2d2A3 = " Mid Speed, 100 KIAS Right Sideslip 2"
d2d2B1 = " Mid Speed, 100 KIAS"
d2d2B2 = " Mid Speed, 100 KIAS Left Sideslip 1"
d2d2B3 = " Mid Speed, 100 KIAS Left Sideslip 2"

# Lateral directional oscillations
d2d3iA1 = " Mid Speed Vy, DSAS, Left Pedal input"
d2d3iA2 = " Mid Speed Vy, AFCS OFF, Left Pedal input"
d2d3iB1 = " High Speed 90 KIAS, DSAS, Left Pedal input"
d2d3iB2 = " High Speed 90, AFCS OFF, Left Pedal input"

# Spiral Stability
d2d3iiA1 = " Right Input, Vy, DSAS"
d2d3iiA2 = " Right Input, Vy, AFCS OFF"
d2d3iiB1 = " Left Input, Vy, DSAS"
d2d3iiB2 = " Left Input, Vy, AFCS OFF"

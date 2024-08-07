# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 21:29:38 2024

@author: user
"""

"""
Version 3:
    -Hier nochmal eine Version um alle Parameter aus den init cond von Reiser zu entnehmen.
    -Und um das dict eine Bessere struktur zu geben. 
    -Und um die Moment of inertia 
"""

import os
import xml.etree.ElementTree as ET
import numpy as np
import csv
import pandas as pd
import json


import shutil



root_dir = r'D:\entity\rotorsky\as532\resources\MQTG_Comparison_with_MQTG_FTD3\MQTG_fuer_FTD1'
dest_dir = r'D:\entity\rotorsky\as532\resources\MQTG_Comparison_with_MQTG_FTD3\Reference_data_Init_flyout_V2'



def get_init_cond_from_xml(path):


    tree = ET.parse(path)
    root = tree.getroot()


        
    test_name = root[0][0].attrib.get('content')+root[0][1].attrib.get('content') + root[0][2].attrib.get('content')    

    init_cond_dict = {
        #Mass and Balance
        root[4][0][0].attrib.get('name') : root[4][0][0].attrib.get('valueSIM'),                #[GW]           kg
        root[4][0][1].attrib.get('name') : root[4][0][1].attrib.get('valueSIM'),                 #[Fuelweight]   kg
        root[4][0][2].attrib.get('name') : root[4][0][2].attrib.get('valueSIM'),               #[CG_Lon]       mm
        root[4][0][3].attrib.get('name') : root[4][0][3].attrib.get('valueSIM'),               #[CG_Lat]       mm
        'Moment of Inertia XX' : root[4][0][4].attrib.get('valueSIMX'),              #[MOM_XX]       kgm^2
        'Moment of Inertia XZ' : root[4][0][4].attrib.get('valueSIMZ'),              #[MOM_XZ]       kgm^2
        'Moment of Inertia YY' : root[4][0][5].attrib.get('valueSIMY'),              #[MOM_YY]       kgm^2
        'Moment of Inertia ZZ' : root[4][0][6].attrib.get('valueSIMZ'),              #[MOM_ZZ]       kgm^2
        
        #Environment Parameters
        root[4][1][0].attrib.get('name') : root[4][1][0].attrib.get('valueSIM'),                   #[Pressure Altitude]  ft
        root[4][1][1].attrib.get('name') : root[4][1][1].attrib.get('valueSIM'),                  #[Outside Air Temp]   degC
        root[4][1][2].attrib.get('name') : root[4][1][2].attrib.get('valueSIM'),                   #[Wind direction]     deg
        root[4][1][3].attrib.get('name') : root[4][1][3].attrib.get('valueSIM'),                   #[Wind speed]         kt
        
        #Flight Parameters
        root[4][2][0].attrib.get('name') : root[4][2][0].attrib.get('valueSIM'),                   #[Airspeed]  kt
        root[4][2][1].attrib.get('name') : root[4][2][1].attrib.get('valueSIM'),                   #[Gorundspeed] kt
        root[4][2][2].attrib.get('name') : root[4][2][2].attrib.get('valueSIM'),                   #[Vertical veloc] ft/min
        root[4][2][3].attrib.get('name') : root[4][2][3].attrib.get('valueSIM'),                  #[Radar alt] ft
        root[4][2][4].attrib.get('name') : root[4][2][4].attrib.get('valueSIM'),                   #[Rotorspeed] %
        root[4][2][5].attrib.get('name') : root[4][2][5].attrib.get('valueSIM'),                  #[Eng1 TRQ] %
        root[4][2][6].attrib.get('name') : root[4][2][6].attrib.get('valueSIM'),                  #[Eng1 TRQ] %
        root[4][2][7].attrib.get('name') : root[4][2][7].attrib.get('valueSIM'),                #[Pitch] deg
        root[4][2][8].attrib.get('name') : root[4][2][8].attrib.get('valueSIM'),                 #[Bank] deg
        root[4][2][9].attrib.get('name') : root[4][2][9].attrib.get('valueSIM'),                  #[Heading] deg
        root[4][2][10].attrib.get('name') : root[4][2][10].attrib.get('valueSIM'),              #[PitchRate] deg/s
        root[4][2][11].attrib.get('name') : root[4][2][11].attrib.get('valueSIM'),               #[RollRate] deg/s  
        root[4][2][12].attrib.get('name') : root[4][2][12].attrib.get('valueSIM'),                #[YawRate] deg/s  
        root[4][2][13].attrib.get('name') : root[4][2][13].attrib.get('valueSIM'),                #[X_acc] m/s^2
        root[4][2][14].attrib.get('name') : root[4][2][14].attrib.get('valueSIM'),                #[y_acc] m/s^2    
        root[4][2][15].attrib.get('name') : root[4][2][15].attrib.get('valueSIM'),                #[Z_acc] m/s^2    
        root[4][2][16].attrib.get('name') : root[4][2][16].attrib.get('valueSIM'),              #[LongCyc] %
        root[4][2][17].attrib.get('name') : root[4][2][17].attrib.get('valueSIM'),               #[LatCyc] %
        root[4][2][18].attrib.get('name') : root[4][2][18].attrib.get('valueSIM'),                #[Ped] %
        root[4][2][19].attrib.get('name') : root[4][2][19].attrib.get('valueSIM'),                #[Coll] %
        root[4][2][20].attrib.get('name') : root[4][2][20].attrib.get('valueSIM'),                  #Engine 1 Main Switch
        root[4][2][21].attrib.get('name') : root[4][2][21].attrib.get('valueSIM'),                  #Engine 2 Main Switch
        root[4][2][22].attrib.get('name') : root[4][2][22].attrib.get('valueSIM'),                  #AFCS State
        root[4][2][23].attrib.get('name') : root[4][2][23].attrib.get('valueSIM')                 #HINR Button

        
        
    }
    #print(test_name)
    return init_cond_dict, test_name

def find_results_xml(root_dir):
    results_xml_paths = []
    data_paths = []
    for subdir, _, files in os.walk(root_dir):
        if 'Results.xml' in files:
            xml_path = os.path.join(subdir, 'Results.xml')
            
            init_cond_dict, test_name = get_init_cond_from_xml(xml_path)
            json_file_path = os.path.join(subdir, 'Reference_init_cond.json')
            with open(json_file_path, 'w') as json_file:
                json.dump(init_cond_dict, json_file,indent=4)
            
            
           # print(init_cond_dict)
        
    return results_xml_paths, data_paths



results_xml_paths, data_paths = find_results_xml(dest_dir)



#Das war 1. 
def ensure_dir_exists(path):
    """Erstellt das Verzeichnis, wenn es nicht existiert."""
    if not os.path.exists(path):
        os.makedirs(path)

# Funktion zum Suchen und Kopieren
def search_and_copy_files(root_dir, dest_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Relativen Pfad des Verzeichnisses bestimmen
        rel_path = os.path.relpath(dirpath, root_dir)
        dest_path = os.path.join(dest_dir, rel_path)

        # Zielverzeichnis erstellen
        ensure_dir_exists(dest_path)

        # Kopieren der Result.xml Datei, falls vorhanden
        if 'Results.xml' in filenames:
            source_file = os.path.join(dirpath, 'Results.xml')
            dest_file = os.path.join(dest_path, 'Results.xml')
            shutil.copy2(source_file, dest_file)
            print(f'Kopiert: {source_file} -> {dest_file}')

        # Alle .sim Dateien im aktuellen Verzeichnis kopieren
        for filename in filenames:
            if filename.endswith('.sim'):
                source_file = os.path.join(dirpath, filename)
                dest_file = os.path.join(dest_path, filename)
                shutil.copy2(source_file, dest_file)
                print(f'Kopiert: {source_file} -> {dest_file}')

# Funktion aufrufen
#search_and_copy_files(root_dir, dest_dir)

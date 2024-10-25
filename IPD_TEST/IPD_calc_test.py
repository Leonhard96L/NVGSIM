# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 14:37:06 2024

@author: simulator
"""

import pandas as pd
import numpy as np


# Funktion zur Berechnung der Punkte mit minimalem Abstand auf zwei Geraden
def closest_points_between_lines(O1, D1, O2, D2, IDP):
    # Differenz der Ursprungsvektoren
    O_diff = np.array(O2) - np.array(O1)
    
    # Skalarprodukte
    D1_dot_D1 = np.dot(D1, D1)
    D2_dot_D2 = np.dot(D2, D2)
    D1_dot_D2 = np.dot(D1, D2)
    O_diff_dot_D1 = np.dot(O_diff, D1)
    O_diff_dot_D2 = np.dot(O_diff, D2)
    
    # Parameter t und s berechnen
    denominator = D1_dot_D1 * D2_dot_D2 - D1_dot_D2 ** 2
    t = (O_diff_dot_D2 * D1_dot_D2 - O_diff_dot_D1 * D2_dot_D2) / denominator
    s = (O_diff_dot_D1 * D1_dot_D2 - O_diff_dot_D2 * D1_dot_D1) / denominator
    
    # Berechne die Punkte auf den Geraden
    closest_point_on_line1 = np.array(O1) + t * np.array(D1)
    closest_point_on_line2 = np.array(O2) + s * np.array(D2)
    distance = np.linalg.norm(closest_point_on_line1 - closest_point_on_line2)
    mean_intersection_point = (closest_point_on_line1+closest_point_on_line2)/2
    
    betweenEye = np.array([IDP/2, 0, 0])/np.linalg.norm(np.array([IDP/2, 0, 0]))

    vector = mean_intersection_point-betweenEye
    distance_object = np.linalg.norm(vector)
    
    return closest_point_on_line1, closest_point_on_line2, distance, mean_intersection_point, distance_object


file_path = r'D:\entity\rotorsky\ec135\resources\NVGSIM\IPD_TEST\varjo_gaze_output_2024-10-25_11-58-25-415_3m.csv'  # Pfad zur CSV-Datei
data = pd.read_csv(file_path)
distance_object_lis = [] 
for index, row in data.iterrows():
    left_origin = [row['left_origin_x'], row['left_origin_y'], row['left_origin_z']]
    left_direction = [row['left_forward_x'], row['left_forward_y'], row['left_forward_z']]
    
    IDP = row['inter_pupillary_distance_in_mm']
    
    right_origin = [row['right_origin_x'], row['right_origin_y'], row['right_origin_z']]
    right_direction = [row['right_forward_x'], row['right_forward_y'], row['right_forward_z']]
    
    closest_point_on_line1, closest_point_on_line2, distance, mean_intersection_point, distance_object = closest_points_between_lines(left_origin, left_direction, right_origin, right_direction, IDP)
    print(f"Punkt auf Gerade 1: {closest_point_on_line1}")
    print(f"Punkt auf Gerade 2: {closest_point_on_line2}")
    print(f"Minimaler Abstand zwischen den Geraden: {distance}")
    print(f"Koordinate des geringsten abstandes: {mean_intersection_point}")
    print(f"Objekt Distanz: {distance_object}")
    distance_object_lis.append(distance_object)
    
print("Mittelwert des Abstands:")
print(np.mean(distance_object_lis)*3)
    
#3m: 3.003226688946665
#10m: 10.035241473991693
#20m: 20.343174910660494m 
    

# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 08:28:05 2024

@author: simulator
"""
import json
import numpy as np


import os, sys, enum, ctypes
from enum import IntEnum
import socket
import struct

import matplotlib.pyplot as plt
from PyPDF2 import PdfMerger
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages


file_path = r"D:\entity\rotorsky\ec135\resources\NVGSIM\Dummy data\2.d.3.ii_B1\Pitch Angle.XY.qtgplot.sim"
dirpath = r"D:\entity\rotorsky\ec135\resources\NVGSIM\Dummy data\Dummy_output_2.d.3.ii_B1"

with open(file_path, 'r') as json_file:
    data = json.load(json_file)
    
    sc_fac = 1.5
    x_label = 'Time(s)'
    y_label = 'Pitch Angle (deg)'
    
    x_Ref = data['Storage'][0]['x']
    y_Ref = data['Storage'][0]['y']
    x = data['FTD1']['x']
    y = data['FTD1']['y']
  
    y=np.rad2deg(y)

    y[-1] = y[-2]
    x[-1] = x[-2]
    
    plot_title = "Pitch Angle"

    pdfname = f"5_{plot_title}.svg"
    pdfname_refer = f"5_{plot_title}_refer.svg"

    plt.figure(figsize=(10, 6))

    
    plt.plot(x_Ref, y_Ref, label='Reference')
    plt.plot(x, y, label='FTD1_MQTG')

    
    ##Section for scale
    
    plt.autoscale()
    y_min, y_max = plt.ylim()
    x_min, x_max = plt.xlim()
    
    y_range = y_max - y_min
    plt.ylim(y_min - y_range*sc_fac, y_max + y_range*sc_fac)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(plot_title)
    plt.legend()
    plt.grid(True)
    #plt.show() 
    save_path = os.path.join(dirpath, pdfname)
    
    plt.savefig(save_path, format='svg')
    plt.close()
    
    ##Neuer Plot (dient als Referenz)
    x_max_snapshot = 1/x_max*x[-1]
    x_min_snapshot = 1/(x_max-x_min)*-x_min
    
    plt.figure(figsize=(10, 6))

    plt.plot(x, y, label='Reference')

    ##Section for scale
    plt.ylim(y_min - y_range*sc_fac, y_max + y_range*sc_fac)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(plot_title)
    plt.legend()
    plt.grid(True)
    #plt.show() 
    save_path = os.path.join(dirpath, pdfname_refer)
    
    plt.savefig(save_path, format='svg')
    plt.close()
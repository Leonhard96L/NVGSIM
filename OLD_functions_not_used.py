# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 10:49:49 2024

@author: simulator
"""

###From Init_flyuout.py

# =============================================================================
# def create_comparison_table(QTG_path):
#     for dirpath, dirnames, filenames in os.walk(QTG_path):
#         for file in filenames:
#             if 'init_conditions' in file:
#                 file_path = os.path.join(dirpath, file)
#                 with open(file_path, 'r') as json_file:
#                     data = json.load(json_file)
# 
#     Init_cond = data["Init_condition_MQTG"]
#     Ref_Init_cond = data["Init_condition_Reference"]
#     init_cond_di_avi = units_conversion(Init_cond, 'Avi')
# 
#     # Erstellen der Tabellendaten
#     table_data = [
#         ["Parameter [UoM]", "Reference*", "FSTD"],
#         ["Mass Properties", "", ""]
#     ]
# 
#     # Werte aus dict1 und dict2 zusammenführen
#     for key in Ref_Init_cond:
#         table_data.append([key, Ref_Init_cond[key], init_cond_di_avi.get(key, "")])
#         if key == "Moment of Inertia ZZ":
#             table_data.append(["Environment Parameters", "", ""])
#         if key == "Wind Speed":
#             table_data.append(["Flight Parameters", "", ""])
# 
#     # DataFrame für die Tabelle erstellen
#     df = pd.DataFrame(table_data)
# 
#     # Erstellen der Tabelle mit matplotlib
#     fig, ax = plt.subplots(figsize=(10, 8))
#     ax.axis('tight')
#     ax.axis('off')
#     table = ax.table(cellText=df.values, colLabels=None, cellLoc='center', loc='center')
# 
#     # Zellen-Formatierung
#     for i, key in enumerate(table_data):
#         if key[0] in ["Parameter [UoM]", "Mass Properties", "Environment Parameters", "Flight Parameters"]:
#             for j in range(3):
#                 cell = table[(i, j)]
#                 cell.set_facecolor('lightgray')
#                 cell.set_text_props(ha='center', weight='bold')
# 
#     for key, cell in table.get_celld().items():
#         cell.set_height(0.05)
# 
#         # Tabelle in PDF speichern
#     table_path = os.path.join(QTG_path, "0_Init_cond_table.pdf")
#     with PdfPages(table_path) as pdf:
#         pdf.savefig(fig, bbox_inches='tight')
# 
#     print(f"Tabelle erfolgreich als {table_path} gespeichert.")
# =============================================================================


# =============================================================================
# def create_plots(QTG_path):
#     for dirpath, dirnames, filenames in os.walk(QTG_path):
#         for file in filenames:
#             if not file.endswith('.sim'):
#                 continue
# 
#             file_path = os.path.join(dirpath, file)
# 
#             with open(file_path, 'r') as json_file:
#                 data = json.load(json_file)
#             if 'FTD1' in data.keys():
#                 plot_title = file.split('.')[0]
# 
#                 x_Ref = data['Storage'][0]['x']
#                 y_Ref = data['Storage'][0]['y']
#                 x = data['FTD1']['x']
#                 y = data['FTD1']['y']
# 
#                 y[-1] = y[-2]
#                 x[-1] = x[-2]
#                 x_label = 'Time(s)'
# 
#                 # Korrektur mit richitgen Einheiten
#                 plt.figure(figsize=(10, 6))
#                 if 'Angle' in plot_title:
#                     pdfname = f"7_{plot_title}.svg"
#                     y = np.rad2deg(y)
#                     y_label = plot_title + ' (deg)'
#                     if 'Angle Rate' in plot_title:
#                         pdfname = f"9_{plot_title}.svg"
#                         y_label = plot_title + ' (deg/s)'
#                     if 'Yaw Angle Unwrapped' in plot_title:
#                         y = [map360(i) for i in y]
#                         plot_title = 'Heading'
#                         pdfname = f"7_{plot_title}.svg"
#                         y_label = plot_title + ' (deg)'
#                 elif 'Control Position' in plot_title:
#                     if 'Control Position Pitch' in plot_title:  # Pitch position Signal ist bei der Referenz invertiert
#                         y = [i * -1 for i in y]
#                     pdfname = f"8_{plot_title}.svg"
#                     y = [map_control(i) for i in y]
#                     y_label = plot_title + ' (%)'
#                 elif 'TRQ' in plot_title:
#                     pdfname = f"5_{plot_title}.svg"
#                     y_label = plot_title + ' (%)'
#                 elif 'Control QTG Force Pitch' in plot_title:
#                     y = [pitch_brun2N(i) for i in y]
#                     x = [pitch_brun2angle(i) for i in x]
#                     pdfname = f"10_{plot_title}.svg"
#                     y_label = 'Force Pitch (N)'
#                     x_label = 'Position (deg)'
#                 elif 'Control QTG Force Roll' in plot_title:
#                     y = [roll_brun2N(i) for i in y]
#                     x = [roll_brun2angle(i) for i in x]
#                     pdfname = f"10_{plot_title}.svg"
#                     y_label = 'Force Roll (N)'
#                     x_label = 'Position (deg)'
#                 elif 'Control QTG Force Collective' in plot_title:
#                     y = [coll_brun2N(i) for i in y]
#                     x = [coll_brun2angle(i) for i in x]
#                     pdfname = f"10_{plot_title}.svg"
#                     y_label = 'Force Collective (N)'
#                     x_label = 'Position (deg)'
#                 elif 'Control QTG Force Yaw' in plot_title:
#                     x = [yaw_brun2angle(i) for i in x]
#                     y = [i * -1000 for i in y]
#                     pdfname = f"10_{plot_title}.svg"
#                     y_label = 'Force Yaw (N)'
#                     x_label = 'Position (deg)'
#                 elif 'Control QTG Position Pitch Velocity' in plot_title:
#                     y = [pitch_brun2angle(i) for i in y]
#                     y, x = ATRIM_calc(x, y)
#                     pdfname = f"11_{plot_title}.svg"
#                     y_label = 'Long. Cyclic Pos. Rate (deg/s)'
#                 elif 'Control QTG Position Roll Velocity' in plot_title:
#                     y = [roll_brun2angle(i) for i in y]
#                     y, x = ATRIM_calc(x, y)
#                     pdfname = f"11_{plot_title}.svg"
#                     y_label = 'Lat. Cyclic Pos. Rate (deg/s)'
#                 elif 'Groundspeed' in plot_title:
#                     pdfname = f"2_{plot_title}.svg"
#                     y = [mps2kt(i) for i in y]
#                     y_label = plot_title + ' (kt)'
#                 elif 'Airspeed' in plot_title:
#                     pdfname = f"1_{plot_title}.svg"
#                     y = [mps2kt(i) for i in y]
#                     y_label = plot_title + ' (kt)'
#                 elif 'RadarAltitude' in plot_title:
#                     pdfname = f"3_{plot_title}.svg"
#                     y_label = plot_title + ' (ft)'
#                 elif 'Barometric Altitude' in plot_title:
#                     pdfname = f"3_{plot_title}.svg"
#                     y = [m2ft(i) for i in y]
#                     y_label = plot_title + ' (ft)'
#                 elif 'Vertical' in plot_title:
#                     pdfname = f"4_{plot_title}.svg"
#                     y = [mps2fpm(-i) for i in y]
#                     y_label = plot_title + ' (ft/min)'
#                 elif 'Rotor' in plot_title:
#                     pdfname = f"6_{plot_title}.svg"
#                     y = [rpm2perc(i) for i in y]
#                     y_label = plot_title + ' (%)'
#                 else:
#                     y_label = plot_title + ' (??)'
#                     pdfname = f"{plot_title}.svg"
# 
#                 plt.plot(x_Ref, y_Ref, label='Reference')
#                 plt.plot(x, y, label='FTD1')
#                 ##Section for scale
#                 sc_fac = 2.5
#                 plt.autoscale()
#                 y_min, y_max = plt.ylim()
#                 y_range = y_max - y_min
#                 plt.ylim(y_min - y_range * sc_fac, y_max + y_range * sc_fac)
# 
#                 plt.xlabel(x_label)
#                 plt.ylabel(y_label)
#                 plt.title(plot_title)
#                 plt.legend()
#                 plt.grid(True)
#                 # plt.show()
#                 save_path = os.path.join(dirpath, pdfname)
# 
#                 plt.savefig(save_path, format='png')
#                 plt.close()
#                 print(plot_title + '.svg created')
# =============================================================================


# =============================================================================
# def create_report(QTG_path, report_file):
#     output_path = os.path.join(QTG_path, report_file)
#     if os.path.exists(output_path):
#         os.remove(output_path)
# 
#     pdf_merger = PdfMerger()
#     # Gehe durch alle Dateien im Ordner
#     for root, dirs, files in os.walk(QTG_path):
#         for file in sorted(files):
#             if file.endswith('.pdf'):
#                 # Voller Pfad der PDF-Datei
#                 file_path = os.path.join(root, file)
#                 pdf_merger.append(file_path)
# 
#     # Speichere die zusammengeführte PDF
# 
#     pdf_merger.write(output_path)
#     pdf_merger.close()
# =============================================================================


# =============================================================================
# def math_pilot(QTG_path, T):
#     ref_input_matrix = np.empty((len(T), INPUT.NUMBER_OF_INPUTS))
#     output_matrix = np.empty((len(T), OUTPUT.NUMBER_OF_OUTPUTS))
#     input_matrix = np.empty((len(T), INPUT.NUMBER_OF_INPUTS))
# 
#     # Get Reference control arrays
#     Input_paths = [
#         os.path.join(QTG_path, 'Control Position Collective.XY.qtgplot.sim'),
#         os.path.join(QTG_path, 'Control Position Roll.XY.qtgplot.sim'),
#         os.path.join(QTG_path, 'Control Position Pitch.XY.qtgplot.sim'),
#         os.path.join(QTG_path, 'Control Position Yaw.XY.qtgplot.sim')]
# 
#     for path, i in zip(Input_paths, range(INPUT.NUMBER_OF_INPUTS)):
#         with open(path, 'r') as json_file:
#             data = json.load(json_file)
#         ref_input_matrix[:, i] = data['Storage'][0]['y']
# 
#     # Moog2Brunner - Value mapping
#     vectorized_function = np.vectorize(inv_map_control)
#     ref_input_matrix = vectorized_function(ref_input_matrix)
# 
#     brunner_task = DSim.Variable.Enum(DSim.Node(dsim_host, "host/sim1-model/entity/ec135_1/task/io_brunner_cls/mode"))
#     brunner_task.write(TASK_MODE.FORCE_STOP)
# 
#     i = 0
#     simulation_mode.write(SIM_MODE.RUN)
# 
#     while i < len(T) - 1:
#         hardware_pilot_collective_position.write(ref_input_matrix[i, INPUT.COLLECTIVE] - 0.8)
#         hardware_pilot_cyclic_lateral_position.write(ref_input_matrix[i, INPUT.CYCLIC_LATERAL])
#         hardware_pilot_cyclic_longitudinal_position.write(-ref_input_matrix[i, INPUT.CYCLIC_LONGITUDINAL])
#         hardware_pilot_pedals_position.write(-ref_input_matrix[i, INPUT.PEDALS] - 0.2)
# 
#         input_matrix[i, INPUT.COLLECTIVE] = hardware_pilot_collective_position.read()
#         input_matrix[i, INPUT.CYCLIC_LATERAL] = hardware_pilot_cyclic_lateral_position.read()
#         input_matrix[i, INPUT.CYCLIC_LONGITUDINAL] = hardware_pilot_cyclic_longitudinal_position.read()
#         input_matrix[i, INPUT.PEDALS] = hardware_pilot_pedals_position.read()
# 
#         output_matrix[i, OUTPUT.AIRSPEED] = reference_frame_body_freestream_airspeed.read()
#         output_matrix[i, OUTPUT.GROUNDSPEED] = reference_frame_inertial_position_v_xy.read()
#         output_matrix[i, OUTPUT.RADARALT] = radio_altimeter_altitude.read()
#         output_matrix[i, OUTPUT.E1TRQ] = engine_1_torque.read()
#         output_matrix[i, OUTPUT.E2TRQ] = engine_2_torque.read()
#         output_matrix[i, OUTPUT.ROTORSPEED] = transmisson_n_r.read()
#         output_matrix[i, OUTPUT.PITCH] = reference_frame_inertial_attitude_theta.read()
#         output_matrix[i, OUTPUT.BANK] = reference_frame_inertial_attitude_phi.read()
#         output_matrix[i, OUTPUT.HEADING] = reference_frame_inertial_attitude_psi.read()
#         output_matrix[i, OUTPUT.PITCHRATE] = reference_frame_body_attitude_q.read()
#         output_matrix[i, OUTPUT.ROLLRATE] = reference_frame_body_attitude_p.read()
#         output_matrix[i, OUTPUT.YAWRATE] = reference_frame_body_attitude_r.read()
#         output_matrix[i, OUTPUT.VERTICALSPEED] = reference_frame_inertial_position_v_z.read()
#         output_matrix[i, OUTPUT.SIDESLIP] = reference_frame_body_freestream_beta.read()
# 
#         # sleep for dT amount of seconds
#         dT = T[i + 1] - T[i]
#         time.sleep(dT)
#         # increment data row index
#         i += 1
# 
#     simulation_mode.write(SIM_MODE.PAUSE)
#     return input_matrix, output_matrix
# =============================================================================


### From RecurrentQTGs_manu.py
# =============================================================================
# def save_io_files(QTG_path, input_matrix, output_matrix, T):
#     Input_paths = [
#         os.path.join(QTG_path,'Control Position Collective.XY.qtgplot.sim'),
#         os.path.join(QTG_path,'Control Position Roll.XY.qtgplot.sim'),
#         os.path.join(QTG_path,'Control Position Pitch.XY.qtgplot.sim'),
#         os.path.join(QTG_path,'Control Position Yaw.XY.qtgplot.sim')
#     ]
# 
#     Output_paths = [
#         os.path.join(QTG_path,'Indicated Airspeed.XY.qtgplot.sim'),
#         os.path.join(QTG_path,'Groundspeed.XY.qtgplot.sim'),
#         os.path.join(QTG_path,'RadarAltitude.XY.qtgplot.sim'),
#         os.path.join(QTG_path,'Engine1 TRQ Indicated.XY.qtgplot.sim'),
#         os.path.join(QTG_path,'Engine2 TRQ Indicated.XY.qtgplot.sim'),
#         os.path.join(QTG_path,'Rotor RPM.XY.qtgplot.sim'),
#         os.path.join(QTG_path,'Pitch Angle.XY.qtgplot.sim'),
#         os.path.join(QTG_path,'Roll Angle.XY.qtgplot.sim'),
#         os.path.join(QTG_path,'Yaw Angle Unwrapped.XY.qtgplot.sim'),
#         os.path.join(QTG_path,'Pitch Angle Rate.XY.qtgplot.sim'),
#         os.path.join(QTG_path,'Roll Angle Rate.XY.qtgplot.sim'),
#         os.path.join(QTG_path,'Yaw Angle Rate.XY.qtgplot.sim'),
#         os.path.join(QTG_path,'Vertical Speed.XY.qtgplot.sim'),
#         os.path.join(QTG_path,'Angle of Sideslip.XY.qtgplot.sim')
#     ]
# 
#     for path, i in zip(Input_paths,range(INPUT.NUMBER_OF_INPUTS)):
#         
#         with open(path, 'r') as json_file:
#             data = json.load(json_file)
# 
#         data["FTD1_Recurrent"] = {
#             "x": T.tolist(), "y": input_matrix[:, i].tolist()
#         }
#         with open(path, 'w') as json_file:
#             json.dump(data, json_file, indent=4)
# 
#     for path, i in zip(Output_paths,range(OUTPUT.NUMBER_OF_OUTPUTS)):
#         try:
#             with open(path, 'r') as json_file:
#                 data = json.load(json_file)
#         except:
#             continue
#             
#         data["FTD1_Recurrent"] = {
#             "x": T.tolist(), "y": output_matrix[:, i].tolist()
#         }
#         with open(path, 'w') as json_file:
#             json.dump(data, json_file, indent=4)
# =============================================================================

# =============================================================================
# def create_report(QTG_path, report_file):
#     output_path = os.path.join(QTG_path, report_file)
#     if os.path.exists(output_path):
#         os.remove(output_path)
#     
#     pdf_merger = PdfMerger()
#     # Gehe durch alle Dateien im Ordner
#     for root, dirs, files in os.walk(QTG_path):
#         for file in sorted(files):
#             if file.endswith('.pdf'):
#                 # Voller Pfad der PDF-Datei
#                 file_path = os.path.join(root, file)
#                 pdf_merger.append(file_path)
# 
#     # Speichere die zusammengeführte PDF
#     
#     pdf_merger.write(output_path)
#     pdf_merger.close()
# =============================================================================
    

# =============================================================================
# def create_plots(QTG_path):
# 
#     #os.system('"qtg_data_structure.py"')
# 
#     for dirpath, dirnames, filenames in os.walk(QTG_path): 
#         for file in filenames:
#             if not file.endswith('.sim'):
#                 continue
# 
#             file_path = os.path.join(dirpath, file)
# 
#             with open(file_path, 'r') as json_file:
#                 data = json.load(json_file)
#             if 'FTD1' in data.keys():
#                 plot_title = file.split('.')[0]
#                 
#                 x_Ref = data['Storage'][0]['x']
#                 y_Ref = data['Storage'][0]['y']
#                 x = data['FTD1']['x']
#                 y = data['FTD1']['y']
#                 x_Rec = data['FTD1_Recurrent']['x']
#                 y_Rec = data['FTD1_Recurrent']['y']
#                 
#                 
#                 y[-1] = y[-2]
#                 x[-1] = x[-2]
#                 y_Rec[-1] = y_Rec[-2]
#                 x_Rec[-1] = x_Rec[-2]
#                 #y_uptol = y
#                 #y_lotol = y
#                 
#                 x_label = 'Time(s)'
# 
#                 #Korrektur mit richitgen Einheiten
#                 plt.figure(figsize=(10, 6))
#                 
#                 if 'Yaw Angle Unwrapped' in plot_title:
#                     y = [map360(i) for i in y]
#                     y_uptol = [i+2 for i in y]
#                     y_lotol = [i-2 for i in y]
#                     y_Rec = [map360(i) for i in y_Rec]
#                     plot_title = 'Heading'
#                     pdfname = f"7_{plot_title}.pdf"
#                     y_label = plot_title + ' (deg)'
#                     plt.plot(x, y_uptol, linewidth=0.5, color='orange', linestyle='dashed')
#                     plt.plot(x, y_lotol, linewidth=0.5, color='orange', linestyle='dashed')
#                 elif 'Roll Angle' in plot_title:
#                     pdfname = f"7_{plot_title}.pdf"
#                     y=np.rad2deg(y)
#                     y_uptol = [i+1.5 for i in y]
#                     y_lotol = [i-1.5 for i in y]
#                     y_Rec=np.rad2deg(y_Rec)
#                     y_label = plot_title + ' (deg)'
#                     plt.plot(x, y_uptol, linewidth=0.5, color='orange', linestyle='dashed')
#                     plt.plot(x, y_lotol, linewidth=0.5, color='orange', linestyle='dashed')
#                 elif 'Pitch Angle' in plot_title:
#                     pdfname = f"7_{plot_title}.pdf"
#                     y=np.rad2deg(y)
#                     y_uptol = [i+2 for i in y]
#                     y_lotol = [i-2 for i in y]
#                     y_Rec=np.rad2deg(y_Rec)
#                     y_label = plot_title + ' (deg)'                    
#                     plt.plot(x, y_uptol, linewidth=0.5, color='orange', linestyle='dashed')
#                     plt.plot(x, y_lotol, linewidth=0.5, color='orange', linestyle='dashed')
#                 elif 'Angle of Sideslip' in plot_title:
#                     pdfname = f"7_{plot_title}.pdf"
#                     y=np.rad2deg(y)
#                     y_Rec=np.rad2deg(y_Rec)
#                     y_label = plot_title + ' (deg)'
#                 elif 'Angle Rate' in plot_title:
#                     pdfname = f"9_{plot_title}.pdf"
#                     y_label = plot_title + ' (deg/s)'
#                 elif 'Control Position Pitch' in plot_title: #Pitch position Signal ist bei der Referenz invertiert
#                     pdfname = f"8_{plot_title}.pdf"
#                     y=[map_control(-i) for i in y]
#                     y_Rec=[map_control(-i) for i in y_Rec]
#                     y_label = plot_title + ' (%)'
#                 elif 'Control Position Collective' in plot_title:
#                     pdfname = f"8_{plot_title}.pdf"
#                     y=[map_control(i) for i in y]
#                     y_Rec=[map_control(i) for i in y_Rec]
#                     y_label = plot_title + ' (%)'
#                 elif 'Control Position Roll' in plot_title:
#                     pdfname = f"8_{plot_title}.pdf"
#                     y=[map_control(i) for i in y]
#                     y_Rec=[map_control(i) for i in y_Rec]
#                     y_label = plot_title + ' (%)'
#                 elif 'Control Position Yaw' in plot_title:
#                     pdfname = f"8_{plot_title}.pdf"
#                     y=[map_control(i) for i in y]
#                     y_Rec=[map_control(i) for i in y_Rec]
#                     y_label = plot_title + ' (%)'               
#                 elif 'TRQ' in plot_title:
#                     y_uptol = [i+3 for i in y]
#                     y_lotol = [i-3 for i in y]
#                     pdfname = f"5_{plot_title}.pdf"
#                     y_label = plot_title + ' (%)'
#                     plt.plot(x, y_uptol, linewidth=0.5, color='orange', linestyle='dashed')
#                     plt.plot(x, y_lotol, linewidth=0.5, color='orange', linestyle='dashed')
#                 elif 'Control QTG Force Pitch' in plot_title:
#                     y = [pitch_brun2N(i) for i in y]
#                     x = [pitch_brun2angle(i) for i in x]
#                     y_Rec = [pitch_brun2N(i) for i in y_Rec]
#                     x_Rec = [pitch_brun2angle(i) for i in x_Rec]
#                     pdfname = f"10_{plot_title}.pdf"
#                     y_label = 'Force Pitch (N)'
#                     x_label = 'Position (deg)'
#                 elif 'Control QTG Force Roll' in plot_title:
#                     y = [roll_brun2N(i) for i in y]
#                     x = [roll_brun2angle(i) for i in x]
#                     y_Rec = [roll_brun2N(i) for i in y_Rec]
#                     x_Rec = [roll_brun2angle(i) for i in x_Rec]
#                     pdfname = f"10_{plot_title}.pdf"
#                     y_label = 'Force Roll (N)'
#                     x_label = 'Position (deg)'
#                 elif 'Control QTG Force Collective' in plot_title:
#                     y = [coll_brun2N(i) for i in y]
#                     x = [coll_brun2angle(i) for i in x]
#                     y_Rec = [coll_brun2N(i) for i in y_Rec]
#                     x_Rec = [coll_brun2angle(i) for i in x_Rec]
#                     pdfname = f"10_{plot_title}.pdf"
#                     y_label = 'Force Collective (N)'
#                     x_label = 'Position (deg)' 
#                 elif 'Control QTG Force Yaw' in plot_title:
#                     x = [yaw_brun2angle(i) for i in x]
#                     y = [i*-1000 for i in y]
#                     x_Rec = [yaw_brun2angle(i) for i in x_Rec]
#                     y_Rec = [i*-1000 for i in y_Rec]
#                     pdfname = f"10_{plot_title}.pdf"
#                     y_label = 'Force Yaw (N)'
#                     x_label = 'Position (deg)'    
#                 elif 'Control QTG Position Pitch Velocity' in plot_title:
#                     y = [pitch_brun2angle(i) for i in y]
#                     y,x = ATRIM_calc(x, y)
#                     y_Rec = [pitch_brun2angle(i) for i in y_Rec]
#                     y_Rec,x_Rec = ATRIM_calc(x_Rec, y_Rec)
#                     pdfname = f"11_{plot_title}.pdf"
#                     y_label = 'Long. Cyclic Pos. Rate (deg/s)'
#                 elif 'Control QTG Position Roll Velocity' in plot_title:
#                     y = [coll_brun2angle(i) for i in y]
#                     y,x = ATRIM_calc(x, y)
#                     y_Rec = [coll_brun2angle(i) for i in y_Rec]
#                     y_Rec,x_Rec = ATRIM_calc(x_Rec, y_Rec)
#                     pdfname = f"11_{plot_title}.pdf"
#                     y_label = 'Lat. Cyclic Pos. Rate (deg/s)'                
#                 elif 'Groundspeed' in plot_title:
#                     pdfname = f"2_{plot_title}.pdf"
#                     y=[mps2kt(i) for i in y]
#                     y_Rec=[mps2kt(i) for i in y_Rec]
#                     y_label = plot_title + ' (kt)'
#                 elif 'Airspeed' in plot_title:
#                     pdfname = f"1_{plot_title}.pdf"
#                     y=[mps2kt(i) for i in y]
#                     y_uptol = [i+3 for i in y]
#                     y_lotol = [i-3 for i in y]
#                     y_Rec=[mps2kt(i) for i in y_Rec]
#                     y_label = plot_title + ' (kt)'
#                     plt.plot(x, y_uptol, linewidth=0.5, color='orange', linestyle='dashed')
#                     plt.plot(x, y_lotol, linewidth=0.5, color='orange', linestyle='dashed')
#                 elif 'RadarAltitude' in plot_title:
#                     pdfname = f"3_{plot_title}.pdf"
#                     y_uptol = [i+20 for i in y]
#                     y_lotol = [i-20 for i in y]
#                     y_label = plot_title + ' (ft)'
#                     plt.plot(x, y_uptol, linewidth=0.5, color='orange', linestyle='dashed')
#                     plt.plot(x, y_lotol, linewidth=0.5, color='orange', linestyle='dashed')
#                 elif 'Barometric Altitude' in plot_title:   
#                     pdfname = f"3_{plot_title}.pdf"
#                     y=[m2ft(i) for i in y]
#                     y_Rec=[m2ft(i) for i in y_Rec]
#                     y_label = plot_title + ' (ft)'
#                 elif 'Vertical' in plot_title:
#                     pdfname = f"4_{plot_title}.pdf"
#                     y=[mps2fpm(-i) for i in y]
#                     y_Rec=[mps2fpm(-i) for i in y_Rec]
#                     y_label = plot_title + ' (ft/min)'
#                 elif 'Rotor' in plot_title:
#                     pdfname = f"6_{plot_title}.pdf"
#                     y=[rpm2perc(i) for i in y]
#                     y_Rec=[rpm2perc(i) for i in y_Rec]
#                     y_label = plot_title + ' (%)'
#                 else:
#                     y_label = plot_title +' (??)'
#                     pdfname = f"{plot_title}.pdf"
#                 
#                 
#                 plt.plot(x_Ref, y_Ref, label='Reference')
#                 plt.plot(x, y, label='FTD1_MQTG')
#                 plt.plot(x_Rec, y_Rec, label='Reccurent', color='green', linestyle='dashed')
# 
#                 
#                 ##Section for scale
#                 sc_fac = 0.5
#                 plt.autoscale()
#                 y_min, y_max = plt.ylim()
#                 y_range = y_max - y_min
#                 plt.ylim(y_min - y_range*sc_fac, y_max + y_range*sc_fac)
# 
#                 plt.xlabel(x_label)
#                 plt.ylabel(y_label)
#                 plt.title(plot_title)
#                 plt.legend()
#                 plt.grid(True)
#                 #plt.show() 
#                 save_path = os.path.join(dirpath, pdfname)
#                 
#                 plt.savefig(save_path, format='pdf')
#                 plt.close()
# =============================================================================

# def split_string(QTG_name):
#     # Find the positions of the first and last dots
#     first_dot = QTG_name.find('.')
#     last_dot = QTG_name.rfind('_')
#
#     # Split the string based on the dot positions
#     test_id = QTG_name[:first_dot]
#     part_id = QTG_name[first_dot + 1:last_dot]
#     case_id = QTG_name[last_dot + 1:]
#     return test_id, part_id, case_id


# =============================================================================
# def create_comparison_table(QTG_path):
# 
#     for dirpath, dirnames, filenames in os.walk(QTG_path): 
#         for file in filenames:
#             if 'init_conditions' in file:
#                 file_path = os.path.join(dirpath, file)
#                 with open(file_path, 'r') as json_file:
#                     data = json.load(json_file)
#                     
#                     
# 
#     Init_cond = data["Init_condition_Reccurent"]
#     Ref_Init_cond = data["Init_condition_MQTG"]
#     
#     init_cond_di_avi = units_conversion(Init_cond,'Avi')
#     Ref_Init_cond = units_conversion(Ref_Init_cond,'Avi')
# 
#     # Erstellen der Tabellendaten
#     table_data = [
#         ["Parameter [UoM]", "MQTG", "Recurrent"],
#         ["Mass Properties", "", ""]
#     ]
#     
#     # Werte aus dict1 und dict2 zusammenführen
#     for key in Ref_Init_cond:
#         table_data.append([key, Ref_Init_cond[key], init_cond_di_avi.get(key, "")])
#         if key == "Moment of Inertia ZZ":
#             table_data.append(["Environment Parameters", "", ""])
#         if key == "Wind Speed":
#             table_data.append(["Flight Parameters", "", ""])
#     
#     # DataFrame für die Tabelle erstellen
#     df = pd.DataFrame(table_data)
#     
#     # Erstellen der Tabelle mit matplotlib
#     fig, ax = plt.subplots(figsize=(10, 8))
#     ax.axis('tight')
#     ax.axis('off')
#     table = ax.table(cellText=df.values, colLabels=None, cellLoc='center', loc='center')
#     
#     # Zellen-Formatierung
#     for i, key in enumerate(table_data):
#         if key[0] in ["Parameter [UoM]", "Mass Properties", "Environment Parameters", "Flight Parameters"]:
#             for j in range(3):
#                 cell = table[(i, j)]
#                 cell.set_facecolor('lightgray')
#                 cell.set_text_props(ha='center', weight='bold')
#     
#     
#     for key, cell in table.get_celld().items():
#         cell.set_height(0.05)            
#     
#     
#     # Tabelle in PDF speichern
#     table_path = os.path.join(QTG_path,"0_Init_cond_table.pdf")
#     with PdfPages(table_path) as pdf:
#         pdf.savefig(fig, bbox_inches='tight')
#     
#     print(f"Tabelle erfolgreich als {table_path} gespeichert.")
# =============================================================================


# =============================================================================
# def math_pilot(QTG_path,T):
#     MQTG_input_matrix = np.empty((len(T),INPUT.NUMBER_OF_INPUTS))
#     output_matrix = np.empty((len(T),OUTPUT.NUMBER_OF_OUTPUTS))
#     input_matrix = np.empty((len(T),INPUT.NUMBER_OF_INPUTS))
#     
#     #Get Reference control arrays
#     Input_paths = [
#     os.path.join(QTG_path,'Control Position Collective.XY.qtgplot.sim'),
#     os.path.join(QTG_path,'Control Position Roll.XY.qtgplot.sim'),
#     os.path.join(QTG_path,'Control Position Pitch.XY.qtgplot.sim'),
#     os.path.join(QTG_path,'Control Position Yaw.XY.qtgplot.sim')]
#     
#     for path, i in zip(Input_paths,range(INPUT.NUMBER_OF_INPUTS)):
#         with open(path, 'r') as json_file:
#             data = json.load(json_file)
#         MQTG_input_matrix[:,i] = data["FTD1"]["y"]
#     
# 
# 
#     
# 
#     i = 0
#     simulation_mode.write(SIM_MODE.RUN) 
#     
#     while i < len(T)-1:
#         hardware_pilot_collective_position.write(MQTG_input_matrix[i,INPUT.COLLECTIVE])
#         hardware_pilot_cyclic_lateral_position.write(MQTG_input_matrix[i,INPUT.CYCLIC_LATERAL])
#         hardware_pilot_cyclic_longitudinal_position.write(MQTG_input_matrix[i,INPUT.CYCLIC_LONGITUDINAL])
#         hardware_pilot_pedals_position.write(MQTG_input_matrix[i,INPUT.PEDALS])
#         
#         input_matrix[i,INPUT.COLLECTIVE] = hardware_pilot_collective_position.read()
#         input_matrix[i,INPUT.CYCLIC_LATERAL] = hardware_pilot_cyclic_lateral_position.read()
#         input_matrix[i,INPUT.CYCLIC_LONGITUDINAL] = hardware_pilot_cyclic_longitudinal_position.read()
#         input_matrix[i,INPUT.PEDALS] = hardware_pilot_pedals_position.read()
# 
#         output_matrix[i,OUTPUT.AIRSPEED] = reference_frame_body_freestream_airspeed.read()
#         output_matrix[i,OUTPUT.GROUNDSPEED] = reference_frame_inertial_position_v_xy.read()
#         output_matrix[i,OUTPUT.RADARALT] = radio_altimeter_altitude.read()
#         output_matrix[i,OUTPUT.E1TRQ] = engine_1_torque.read()
#         output_matrix[i,OUTPUT.E2TRQ] = engine_2_torque.read()
#         output_matrix[i,OUTPUT.ROTORSPEED] = transmisson_n_r.read()
#         output_matrix[i,OUTPUT.PITCH] = reference_frame_inertial_attitude_theta.read()
#         output_matrix[i,OUTPUT.BANK] = reference_frame_inertial_attitude_phi.read()
#         output_matrix[i,OUTPUT.HEADING] = reference_frame_inertial_attitude_psi.read()
#         output_matrix[i,OUTPUT.PITCHRATE] = reference_frame_body_attitude_q.read()
#         output_matrix[i,OUTPUT.ROLLRATE] = reference_frame_body_attitude_p.read()
#         output_matrix[i,OUTPUT.YAWRATE] = reference_frame_body_attitude_r.read()
#         output_matrix[i,OUTPUT.VERTICALSPEED] = reference_frame_inertial_position_v_z.read()
#         output_matrix[i,OUTPUT.SIDESLIP] = reference_frame_body_freestream_beta.read()
# 
#         # sleep for dT amount of seconds
#         dT = T[i+1]-T[i]
#         time.sleep(dT)
#         # increment data row index
#         i += 1
# 
#     simulation_mode.write(SIM_MODE.PAUSE)
#     return input_matrix, output_matrix
# =============================================================================

# =============================================================================
# def log_flyout_input_output(T, gui_output):
#     # pre-define numpy data matrix containing flight data (see enum above for column definitions)
#     input_matrix = np.empty((len(T),INPUT.NUMBER_OF_INPUTS))
#     output_matrix = np.empty((len(T),OUTPUT.NUMBER_OF_OUTPUTS))
#     
#     sock, remoteEndpoint, query_readforce_pitch_roll, query_readforce_yaw_coll = CLS_READER_INIT()
#     force_pitch, force_roll, force_yaw, force_coll = 0,0,0,0
#     prev_force_pitch, prev_force_roll, prev_force_yaw, prev_force_coll = 0,0,0,0
#     def sendThenReceive(send_data, targetAddr, sock):
#         # after each send you HAVE to do a read, even if you don't do anything with the reponse
#         sock.sendto(send_data, targetAddr)
#         response, address = sock.recvfrom(8192)
#         return response
# 
#     number_format = '{:+.5f}'
#     force_matrix = np.empty((len(T),INPUT.NUMBER_OF_INPUTS))
# 
# 
#     accumulated_time = 0
#     i = 0
# 
#     while i < len(T)-1:
#         input_matrix[i,INPUT.COLLECTIVE] = hardware_pilot_collective_position.read()
#         input_matrix[i,INPUT.CYCLIC_LATERAL] = hardware_pilot_cyclic_lateral_position.read()
#         input_matrix[i,INPUT.CYCLIC_LONGITUDINAL] = hardware_pilot_cyclic_longitudinal_position.read()
#         input_matrix[i,INPUT.PEDALS] = hardware_pilot_pedals_position.read()
#         
#         output_matrix[i,OUTPUT.AIRSPEED] = reference_frame_body_freestream_airspeed.read()
#         output_matrix[i,OUTPUT.GROUNDSPEED] = reference_frame_inertial_position_v_xy.read()
#         output_matrix[i,OUTPUT.RADARALT] = radio_altimeter_altitude.read()
#         output_matrix[i,OUTPUT.E1TRQ] = engine_1_torque.read()
#         output_matrix[i,OUTPUT.E2TRQ] = engine_2_torque.read()
#         output_matrix[i,OUTPUT.ROTORSPEED] = transmisson_n_r.read()
#         output_matrix[i,OUTPUT.PITCH] = reference_frame_inertial_attitude_theta.read()
#         output_matrix[i,OUTPUT.BANK] = reference_frame_inertial_attitude_phi.read()
#         output_matrix[i,OUTPUT.HEADING] = reference_frame_inertial_attitude_psi.read()
#         output_matrix[i,OUTPUT.PITCHRATE] = reference_frame_body_attitude_q.read()
#         output_matrix[i,OUTPUT.ROLLRATE] = reference_frame_body_attitude_p.read()
#         output_matrix[i,OUTPUT.YAWRATE] = reference_frame_body_attitude_r.read()
#         output_matrix[i,OUTPUT.VERTICALSPEED] = reference_frame_inertial_position_v_z.read()
#         output_matrix[i,OUTPUT.SIDESLIP] = reference_frame_body_freestream_beta.read()
#         
# 
#         #Read control forces
#         force_response_pitch_roll = sendThenReceive(query_readforce_pitch_roll, remoteEndpoint, sock)
#         force_response_yaw_coll = sendThenReceive(query_readforce_yaw_coll, remoteEndpoint, sock)
#         length, status, node_pitch, force_pitch, node_roll, force_roll = struct.unpack('<HBHfHf', force_response_pitch_roll[0:15])
#         length, status, node_yaw, force_yaw, node_coll, force_coll = struct.unpack('<HBHfHf', force_response_yaw_coll[0:15])
#         force_matrix[i,INPUT.CYCLIC_LONGITUDINAL] = number_format.format(force_pitch)
#         force_matrix[i,INPUT.CYCLIC_LATERAL] = number_format.format(force_roll)
#         force_matrix[i,INPUT.PEDALS] = number_format.format(force_yaw)    
#         force_matrix[i,INPUT.COLLECTIVE] = number_format.format(force_coll)  
#         # sleep for dT amount of seconds
#         dT = T[i+1]-T[i]
#         accumulated_time +=dT
#         time.sleep(dT)
#         
#         if int(accumulated_time) > int(accumulated_time - dT):
#             print(round(accumulated_time-dT))
#             gui_output(str(round(accumulated_time - dT)))
#             
#         if prev_force_pitch != force_pitch \
#             or prev_force_roll != force_roll \
#             or prev_force_yaw != force_yaw \
#             or prev_force_coll != force_coll:
#             prev_force_pitch = force_pitch
#             prev_force_roll = force_roll
#             prev_force_yaw = force_yaw
#             prev_force_coll = force_coll
# 
#         
#         # increment data row index
#         i += 1
#     sock.close()
#     simulation_mode.write(SIM_MODE.PAUSE)
#     return input_matrix, output_matrix, force_matrix
# =============================================================================


# =============================================================================
# def create_plots(QTG_path, part):
# 
#     params = part['tolerances_recurrent_criteria']
#     para_file_dict = {
#         'Engine 1 Torque':'Engine1 TRQ Indicated',
#         'Engine 2 Torque':'Engine2 TRQ Indicated',
#         'Rotor Speed' : 'Rotor RPM',
#         'Pitch Angle' : 'Pitch Angle',
#         'Bank Angle' : 'Roll Angle',
#         'Heading' : 'Yaw Angle Unwrapped',
#         'Sideslip Angle' : 'Angle of Sideslip',
#         'Airspeed' : 'Indicated Airspeed',
#         'Radar Altitude' : 'RadarAltitude',
#         'Vertical Velocity' : 'Vertical Speed',
#         'Longitudinal Cyclic Pos.' : 'Control Position Pitch',
#         'Lateral Cyclic Pos.' : 'Control Position Roll',
#         'Pedals Pos.' : 'Control Position Yaw',
#         'Collective Pos.' : 'Control Position Collective',
#         'Pitch Rate' : 'Pitch Angle Rate',
#         'Roll Rate' : 'Roll Angle Rate' ,
#         'Yaw Rate' : 'Yaw Angle Rate',
#         'Correct Trend on Bank' : 'Roll Angle',
#         'Force' : 'Control QTG Force',
#         'Breakout' : 'dummy'
#          
#     }
#     
#     
#     for count,param in enumerate(params):
#         count = count+1
#         plot_title = param['parameter']
#         tol = float(param['tolerance'][1:])
#         for dirpath, dirnames, filenames in os.walk(QTG_path):     
#             for file in filenames:
#                 #if file.split('.')[0] == para_file_dict[plot_title] and file.endswith('.sim'):
#                 if para_file_dict[plot_title] in file.split('.')[0]  and file.endswith('.sim'):
#                     file_path = os.path.join(dirpath, file)
#                     compare_name = file.split('.')[0]
#                     break
# 
# 
#         try:
#             print(file_path)
#             with open(file_path, 'r') as json_file:
#                 data = json.load(json_file)
#         except:
#             continue
#         
#         if 'FTD1' in data.keys():
#             x_Ref = data['Storage'][0]['x']
#             y_Ref = data['Storage'][0]['y']
#             x = data['FTD1']['x']
#             y = data['FTD1']['y']
#             x_Rec = data['FTD1_Recurrent']['x']
#             y_Rec = data['FTD1_Recurrent']['y']       
#         
#             y[-1] = y[-2]
#             x[-1] = x[-2]
#             y_Rec[-1] = y_Rec[-2]
#             x_Rec[-1] = x_Rec[-2]
#         
#             x_label = 'Time(s)'     
#             
#             if 'Yaw Angle Unwrapped' in para_file_dict[plot_title]:
#                 y = [map360(i) for i in y]
#                 y_Rec = [map360(i) for i in y_Rec]
#             elif 'Roll Angle' in para_file_dict[plot_title]:
#                 y=np.rad2deg(y)
#                 y_Rec=np.rad2deg(y_Rec)
#             elif 'Pitch Angle' in para_file_dict[plot_title]:
#                 y=np.rad2deg(y)
#                 y_Rec=np.rad2deg(y_Rec)
#             elif 'Angle of Sideslip' in para_file_dict[plot_title]:
#                 y=np.rad2deg(y)
#                 y_Rec=np.rad2deg(y_Rec)
#             elif 'Angle Rate' in para_file_dict[plot_title]:
#                 y=np.rad2deg(y)
#                 y_Rec=np.rad2deg(y_Rec)
#             elif 'Control Position Pitch' in para_file_dict[plot_title]: 
#                 y=[map_control(i, 'pitch') for i in y]
#                 y_Rec=[map_control(i, 'pitch') for i in y_Rec]
#             elif 'Control Position Collective' in para_file_dict[plot_title]:
#                 y=[map_control(i, 'collective') for i in y]
#                 y_Rec=[map_control(i, 'collective') for i in y_Rec]
#             elif 'Control Position Roll' in para_file_dict[plot_title]:
#                 y=[map_control(i, 'roll') for i in y]
#                 y_Rec=[map_control(i, 'roll') for i in y_Rec]
#             elif 'Control Position Yaw' in para_file_dict[plot_title]:
#                 y=[map_control(i, 'pedal') for i in y]
#                 y_Rec=[map_control(i, 'pedal') for i in y_Rec] 
#             elif 'Control QTG Force Pitch' in compare_name:
#                 y = [pitch_brun2N(i) for i in y]
#                 x = [pitch_brun2angle(i) for i in x]
#                 y_Rec = [pitch_brun2N(i) for i in y_Rec]
#                 x_Rec = [pitch_brun2angle(i) for i in x_Rec]
#                 x_label = 'Position (deg)'
#             elif 'Control QTG Force Roll' in compare_name:
#                 y = [roll_brun2N(i) for i in y]
#                 x = [roll_brun2angle(i) for i in x]
#                 y_Rec = [roll_brun2N(i) for i in y_Rec]
#                 x_Rec = [roll_brun2angle(i) for i in x_Rec]
#                 x_label = 'Position (deg)'
#             elif 'Control QTG Force Collective' in compare_name:
#                 y = [coll_brun2N(i) for i in y]
#                 x = [coll_brun2angle(i) for i in x]
#                 y_Rec = [coll_brun2N(i) for i in y_Rec]
#                 x_Rec = [coll_brun2angle(i) for i in x_Rec]
#                 x_label = 'Position (deg)'
#             elif 'Control QTG Force Yaw' in compare_name:
#                 x = [yaw_brun2angle(i) for i in x]
#                 y = [i*-1000 for i in y]
#                 x_Rec = [yaw_brun2angle(i) for i in x_Rec]
#                 y_Rec = [i*-1000 for i in y_Rec]
#                 x_label = 'Position (deg)'
#             elif 'Control QTG Position Pitch Velocity' in para_file_dict[plot_title]:
#                 y = [pitch_brun2angle(i) for i in y]
#                 y,x = ATRIM_calc(x, y)
#                 y_Rec = [pitch_brun2angle(i) for i in y_Rec]
#                 y_Rec,x_Rec = ATRIM_calc(x_Rec, y_Rec)
#             elif 'Control QTG Position Roll Velocity' in para_file_dict[plot_title]:
#                 y = [coll_brun2angle(i) for i in y]
#                 y,x = ATRIM_calc(x, y)
#                 y_Rec = [coll_brun2angle(i) for i in y_Rec]
#                 y_Rec,x_Rec = ATRIM_calc(x_Rec, y_Rec)
#             elif 'Groundspeed' in para_file_dict[plot_title]:
#                 y=[mps2kt(i) for i in y]
#                 y_Rec=[mps2kt(i) for i in y_Rec]
#             elif 'Airspeed' in para_file_dict[plot_title]:
#                 y=[mps2kt(i) for i in y]
#                 y_Rec=[mps2kt(i) for i in y_Rec]
#             elif 'Barometric Altitude' in para_file_dict[plot_title]:
#                 y=[m2ft(i) for i in y]
#                 y_Rec=[m2ft(i) for i in y_Rec]
#             elif 'Vertical' in para_file_dict[plot_title]:
#                 y=[mps2fpm(-i) for i in y]
#                 y_Rec=[mps2fpm(-i) for i in y_Rec]
#             elif 'Rotor' in para_file_dict[plot_title]:
#                 y=[rpm2perc(i) for i in y]
#                 y_Rec=[rpm2perc(i) for i in y_Rec]
#             else:
#                 y_label = plot_title +' (??)'
#                 pdfname = f"{plot_title}.svg"
#             
#             
#             
#             y_uptol = [i+tol for i in y]
#             y_lotol = [i-tol for i in y]
#             
#             pdfname = f"{count}_{plot_title}.svg"
#             y_label = plot_title +' '+ param['unit']
#     
#             plt.figure(figsize=(10, 6))
#             plt.plot(x, y_uptol, linewidth=0.5, color='orange', linestyle='dashed')
#             plt.plot(x, y_lotol, linewidth=0.5, color='orange', linestyle='dashed')
#             
#             
#             plt.plot(x_Ref, y_Ref, label='Reference')
#             plt.plot(x, y, label='FTD1_MQTG')
#             plt.plot(x_Rec, y_Rec, label='Reccurent', color='green', linestyle='dashed')
#     
#             
#             ##Section for scale
#             sc_fac = 2.5
#             plt.autoscale()
#             y_min, y_max = plt.ylim()
#             y_range = y_max - y_min
#             plt.ylim(y_min - y_range*sc_fac, y_max + y_range*sc_fac)
#     
#             plt.xlabel(x_label)
#             plt.ylabel(y_label)
#             plt.title(plot_title)
#             plt.legend()
#             plt.grid(True)
#             #plt.show() 
#             save_path = os.path.join(dirpath, pdfname)
#             
#             plt.savefig(save_path, format='svg')
#             plt.close()
# =============================================================================


# =============================================================================
# def create_plots(QTG_path, part):
# 
#     params = part['tolerances_recurrent_criteria']
#     para_file_dict = {
#         'Engine 1 Torque':'Engine1 TRQ Indicated',
#         'Engine 2 Torque':'Engine2 TRQ Indicated',
#         'Rotor Speed' : 'Rotor RPM',
#         'Pitch Angle' : 'Pitch Angle',
#         'Bank Angle' : 'Roll Angle',
#         'Heading' : 'Yaw Angle Unwrapped',
#         'Sideslip Angle' : 'Angle of Sideslip',
#         'Airspeed' : 'Indicated Airspeed',
#         'Radar Altitude' : 'RadarAltitude',
#         'Vertical Velocity' : 'Vertical Speed',
#         'Longitudinal Cyclic Pos.' : 'Control Position Pitch',
#         'Lateral Cyclic Pos.' : 'Control Position Roll',
#         'Pedals Pos.' : 'Control Position Yaw',
#         'Collective Pos.' : 'Control Position Collective',
#         'Pitch Rate' : 'Pitch Angle Rate',
#         'Roll Rate' : 'Roll Angle Rate' ,
#         'Yaw Rate' : 'Yaw Angle Rate',
#         'Correct Trend on Bank' : 'Roll Angle',
#         'Force' : 'Control QTG Force',
#         'Breakout' : 'dummy'
#          
#     }
#     
#     
#     for count,param in enumerate(params):
#         count = count+1
#         plot_title = param['parameter']
#         tol = float(param['tolerance'][1:])
#         for dirpath, dirnames, filenames in os.walk(QTG_path):     
#             for file in filenames:
#                 #if file.split('.')[0] == para_file_dict[plot_title] and file.endswith('.sim'):
#                 if para_file_dict[plot_title] in file.split('.')[0]  and file.endswith('.sim'):
#                     file_path = os.path.join(dirpath, file)
#                     compare_name = file.split('.')[0]
#                     break
# 
# 
#         try:
#             print(file_path)
#             with open(file_path, 'r') as json_file:
#                 data = json.load(json_file)
#         except:
#             continue
#         
#         if 'FTD1' in data.keys():
#             x_Ref = data['Storage'][0]['x']
#             y_Ref = data['Storage'][0]['y']
#             x = data['FTD1']['x']
#             y = data['FTD1']['y']
#             x_Rec = data['FTD1_Recurrent']['x']
#             y_Rec = data['FTD1_Recurrent']['y']       
#         
#             y[-1] = y[-2]
#             x[-1] = x[-2]
#             y_Rec[-1] = y_Rec[-2]
#             x_Rec[-1] = x_Rec[-2]
#         
#             x_label = 'Time(s)'     
#             
#             if 'Yaw Angle Unwrapped' in para_file_dict[plot_title]:
#                 y = [map360(i) for i in y]
#                 y_Rec = [map360(i) for i in y_Rec]
#             elif 'Roll Angle' in para_file_dict[plot_title]:
#                 y=np.rad2deg(y)
#                 y_Rec=np.rad2deg(y_Rec)
#             elif 'Pitch Angle' in para_file_dict[plot_title]:
#                 y=np.rad2deg(y)
#                 y_Rec=np.rad2deg(y_Rec)
#             elif 'Angle of Sideslip' in para_file_dict[plot_title]:
#                 y=np.rad2deg(y)
#                 y_Rec=np.rad2deg(y_Rec)
#             elif 'Angle Rate' in para_file_dict[plot_title]:
#                 y=np.rad2deg(y)
#                 y_Rec=np.rad2deg(y_Rec)
#             elif 'Control Position Pitch' in para_file_dict[plot_title]: 
#                 y=[map_control(i, 'pitch') for i in y]
#                 y_Rec=[map_control(i, 'pitch') for i in y_Rec]
#             elif 'Control Position Collective' in para_file_dict[plot_title]:
#                 y=[map_control(i, 'collective') for i in y]
#                 y_Rec=[map_control(i, 'collective') for i in y_Rec]
#             elif 'Control Position Roll' in para_file_dict[plot_title]:
#                 y=[map_control(i, 'roll') for i in y]
#                 y_Rec=[map_control(i, 'roll') for i in y_Rec]
#             elif 'Control Position Yaw' in para_file_dict[plot_title]:
#                 y=[map_control(i, 'pedal') for i in y]
#                 y_Rec=[map_control(i, 'pedal') for i in y_Rec] 
#             elif 'Control QTG Force Pitch' in compare_name:
#                 y = [pitch_brun2N(i) for i in y]
#                 x = [pitch_brun2angle(i) for i in x]
#                 y_Rec = [pitch_brun2N(i) for i in y_Rec]
#                 x_Rec = [pitch_brun2angle(i) for i in x_Rec]
#                 x_label = 'Position (deg)'
#             elif 'Control QTG Force Roll' in compare_name:
#                 y = [roll_brun2N(i) for i in y]
#                 x = [roll_brun2angle(i) for i in x]
#                 y_Rec = [roll_brun2N(i) for i in y_Rec]
#                 x_Rec = [roll_brun2angle(i) for i in x_Rec]
#                 x_label = 'Position (deg)'
#             elif 'Control QTG Force Collective' in compare_name:
#                 y = [coll_brun2N(i) for i in y]
#                 x = [coll_brun2angle(i) for i in x]
#                 y_Rec = [coll_brun2N(i) for i in y_Rec]
#                 x_Rec = [coll_brun2angle(i) for i in x_Rec]
#                 x_label = 'Position (deg)'
#             elif 'Control QTG Force Yaw' in compare_name:
#                 x = [yaw_brun2angle(i) for i in x]
#                 y = [i*-1000 for i in y]
#                 x_Rec = [yaw_brun2angle(i) for i in x_Rec]
#                 y_Rec = [i*-1000 for i in y_Rec]
#                 x_label = 'Position (deg)'
#             elif 'Control QTG Position Pitch Velocity' in para_file_dict[plot_title]:
#                 y = [pitch_brun2angle(i) for i in y]
#                 y,x = ATRIM_calc(x, y)
#                 y_Rec = [pitch_brun2angle(i) for i in y_Rec]
#                 y_Rec,x_Rec = ATRIM_calc(x_Rec, y_Rec)
#             elif 'Control QTG Position Roll Velocity' in para_file_dict[plot_title]:
#                 y = [coll_brun2angle(i) for i in y]
#                 y,x = ATRIM_calc(x, y)
#                 y_Rec = [coll_brun2angle(i) for i in y_Rec]
#                 y_Rec,x_Rec = ATRIM_calc(x_Rec, y_Rec)
#             elif 'Groundspeed' in para_file_dict[plot_title]:
#                 y=[mps2kt(i) for i in y]
#                 y_Rec=[mps2kt(i) for i in y_Rec]
#             elif 'Airspeed' in para_file_dict[plot_title]:
#                 y=[mps2kt(i) for i in y]
#                 y_Rec=[mps2kt(i) for i in y_Rec]
#             elif 'Barometric Altitude' in para_file_dict[plot_title]:
#                 y=[m2ft(i) for i in y]
#                 y_Rec=[m2ft(i) for i in y_Rec]
#             elif 'Vertical' in para_file_dict[plot_title]:
#                 y=[mps2fpm(-i) for i in y]
#                 y_Rec=[mps2fpm(-i) for i in y_Rec]
#             elif 'Rotor' in para_file_dict[plot_title]:
#                 y=[rpm2perc(i) for i in y]
#                 y_Rec=[rpm2perc(i) for i in y_Rec]
#             else:
#                 y_label = plot_title +' (??)'
#                 pdfname = f"{plot_title}.svg"
#             
#             
#             
#             y_uptol = [i+tol for i in y]
#             y_lotol = [i-tol for i in y]
#             
#             pdfname = f"{count}_{plot_title}.svg"
#             y_label = plot_title +' '+ param['unit']
#     
#             plt.figure(figsize=(10, 6))
#             plt.plot(x, y_uptol, linewidth=0.5, color='orange', linestyle='dashed')
#             plt.plot(x, y_lotol, linewidth=0.5, color='orange', linestyle='dashed')
#             
#             
#             plt.plot(x_Ref, y_Ref, label='Reference')
#             plt.plot(x, y, label='FTD1_MQTG')
#             plt.plot(x_Rec, y_Rec, label='Reccurent', color='green', linestyle='dashed')
#     
#             
#             ##Section for scale
#             sc_fac = 2.5
#             plt.autoscale()
#             y_min, y_max = plt.ylim()
#             y_range = y_max - y_min
#             plt.ylim(y_min - y_range*sc_fac, y_max + y_range*sc_fac)
#     
#             plt.xlabel(x_label)
#             plt.ylabel(y_label)
#             plt.title(plot_title)
#             plt.legend()
#             plt.grid(True)
#             #plt.show() 
#             save_path = os.path.join(dirpath, pdfname)
#             
#             plt.savefig(save_path, format='svg')
#             plt.close()
# =============================================================================


###RecurrentQTGs_auto.py

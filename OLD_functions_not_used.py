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
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 14:11:41 2024

@author: simulator
"""

import json

import os, sys, enum, ctypes
from enum import IntEnum
import socket
import struct

import matplotlib.pyplot as plt
from PyPDF2 import PdfMerger
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

from function_lib import ft2m, map360, map_control, pitch_brun2N, pitch_brun2angle, roll_brun2N, roll_brun2angle, \
    coll_brun2N, coll_brun2angle, yaw_brun2angle, ATRIM_calc, mps2kt, m2ft, mps2fpm, rpm2perc, units_conversion, \
    split_string

dsim_root_directory = os.path.join(os.path.dirname(sys.path[0]), "D:/")
sys.path.append(os.path.join(dsim_root_directory, "entity/multisim/dsim/sdk/python/include"))
sys.path.append(os.path.join(dsim_root_directory, "entity/multisim/simulation/sdk/python/include"))


import DSim
import ctypes
import qtg_data_structure
import numpy as np



import time
from datetime import datetime

# get more accurate timer (using windows multimedia dll)
winmm = ctypes.WinDLL('winmm')
winmm.timeBeginPeriod(1)

# host definition
dsim_host = DSim.Entity("sim1")
# entity definition
dsim_entity   = DSim.Entity("as532_1")

dworld_entity = DSim.Entity("world")
# control simulation mode in D-SIM
simulation_mode  = DSim.Variable.Enum(DSim.Node(dsim_entity, "SIMULATION/mode"))

class TASK_MODE(enum.IntEnum):
    AUTO = 0
    FORCE_STOP = 1
    FORCE_RUN = 2

class SIM_MODE(enum.IntEnum):
    TRIM = 0
    RUN = 1
    PAUSE = 2
    REPLAY = 3
class INPUT(enum.IntEnum):
    COLLECTIVE = 0
    CYCLIC_LATERAL = 1
    CYCLIC_LONGITUDINAL = 2
    PEDALS = 3
    NUMBER_OF_INPUTS = 4
    
class OUTPUT(enum.IntEnum):
    AIRSPEED = 0
    GROUNDSPEED = 1
    RADARALT = 2
    E1TRQ = 3
    E2TRQ = 4
    ROTORSPEED = 5
    PITCH = 6
    BANK = 7
    HEADING = 8
    PITCHRATE = 9
    ROLLRATE = 10
    YAWRATE = 11
    VERTICALSPEED = 12
    SIDESLIP = 13    
    NUMBER_OF_OUTPUTS = 14

class AxisBitmask(enum.IntEnum):
    Elevator     = 0x1  #1 - Pitch
    Aileron      = 0x2  #2 - ROLL
    Rudder       = 0x4  #3 - YAW
    Collective   = 0x8  #4 - COLL	




###All needed NVGSIM Variables

#read
reference_frame_inertial_position_latitude = DSim.Variable.Double(DSim.Node(dsim_entity,"reference_frame/inertial/position/latitude"))
reference_frame_inertial_position_longitude = DSim.Variable.Double(DSim.Node(dsim_entity,"reference_frame/inertial/position/longitude"))
reference_frame_inertial_position_altitude = DSim.Variable.Double(DSim.Node(dsim_entity,"reference_frame/inertial/position/altitude"))
reference_frame_inertial_position_v_xy = DSim.Variable.Double(DSim.Node(dsim_entity,"reference_frame/inertial/position/v_xy")) #Forward speed
reference_frame_inertial_position_v_z = DSim.Variable.Double(DSim.Node(dsim_entity,"reference_frame/inertial/position/v_z"))   #vertical veloc (negativ)
reference_frame_inertial_attitude_phi = DSim.Variable.Double(DSim.Node(dsim_entity,"reference_frame/inertial/attitude/phi"))
reference_frame_inertial_attitude_theta = DSim.Variable.Double(DSim.Node(dsim_entity,"reference_frame/inertial/attitude/theta"))
reference_frame_inertial_attitude_psi = DSim.Variable.Double(DSim.Node(dsim_entity,"reference_frame/inertial/attitude/psi"))
reference_frame_body_attitude_p = DSim.Variable.Double(DSim.Node(dsim_entity,"reference_frame/body/attitude/p"))
reference_frame_body_attitude_q = DSim.Variable.Double(DSim.Node(dsim_entity,"reference_frame/body/attitude/q"))
reference_frame_body_attitude_r = DSim.Variable.Double(DSim.Node(dsim_entity,"reference_frame/body/attitude/r"))
reference_frame_body_freestream_airspeed = DSim.Variable.Double(DSim.Node(dsim_entity,"reference_frame/body/freestream/v_x"))
reference_frame_body_freestream_alpha = DSim.Variable.Double(DSim.Node(dsim_entity,"reference_frame/body/freestream/alpha"))
reference_frame_body_freestream_beta = DSim.Variable.Double(DSim.Node(dsim_entity,"reference_frame/body/freestream/beta"))

reference_frame_inertial_position_a_x = DSim.Variable.Double(DSim.Node(dsim_entity,"reference_frame/inertial/position/a_x"))
reference_frame_inertial_position_a_y = DSim.Variable.Double(DSim.Node(dsim_entity,"reference_frame/inertial/position/a_y"))
reference_frame_inertial_position_a_z = DSim.Variable.Double(DSim.Node(dsim_entity,"reference_frame/inertial/position/a_z"))

engine_1_torque = DSim.Variable.Double(DSim.Node(dsim_entity,"engine/1/torque"))
engine_2_torque = DSim.Variable.Double(DSim.Node(dsim_entity,"engine/2/torque"))
transmisson_n_r = DSim.Variable.Double(DSim.Node(dsim_entity,"transmission/n_r"))
radio_altimeter_altitude = DSim.Variable.Double(DSim.Node(dsim_entity,"radio_altimeter/altitude"))

configuration_loading_fuel_mass = DSim.Variable.Double(DSim.Node(dsim_entity,"configuration/loading/fuel/mass"))
flightmodel_configuration_cg_x = DSim.Variable.Double(DSim.Node(dsim_entity,"flightmodel/configuration/cg/x"))
flightmodel_configuration_cg_y = DSim.Variable.Double(DSim.Node(dsim_entity,"flightmodel/configuration/cg/y"))

#written
hardware_pilot_collective_position = DSim.Variable.Double(DSim.Node(dsim_entity,"hardware/pilot/collective/position_uncalibrated"))
hardware_pilot_collective_trim_position = DSim.Variable.Double(DSim.Node(dsim_entity,"hardware/pilot/collective/trim/position"))
hardware_pilot_cyclic_lateral_position = DSim.Variable.Double(DSim.Node(dsim_entity,"hardware/pilot/cyclic/lateral/position"))
hardware_pilot_cyclic_lateral_trim_position = DSim.Variable.Double(DSim.Node(dsim_entity,"hardware/pilot/cyclic/lateral/trim/position"))
hardware_pilot_cyclic_longitudinal_position = DSim.Variable.Double(DSim.Node(dsim_entity,"hardware/pilot/cyclic/longitudinal/position"))
hardware_pilot_cyclic_longitudinal_trim_position = DSim.Variable.Double(DSim.Node(dsim_entity,"hardware/pilot/cyclic/longitudinal/trim/position"))
hardware_pilot_pedals_position = DSim.Variable.Double(DSim.Node(dsim_entity,"hardware/pilot/pedals/position"))
hardware_pilot_pedals_trim_position = DSim.Variable.Double(DSim.Node(dsim_entity,"hardware/pilot/pedals/trim/position"))

configuration_failure_engine_1_failed= DSim.Variable.Bool(DSim.Node(dsim_entity,"configuration/failure/engine/1/failed")) #run=false
configuration_failure_engine_2_failed= DSim.Variable.Bool(DSim.Node(dsim_entity,"configuration/failure/engine/2/failed"))
configuration_loading_empty_mass = DSim.Variable.Double(DSim.Node(dsim_entity,"configuration/loading/empty/mass"))

flightmodel_configuration_inertia_i_xx = DSim.Variable.Double(DSim.Node(dsim_entity,"flightmodel/configuration/inertia/i_xx"))
flightmodel_configuration_inertia_i_xz = DSim.Variable.Double(DSim.Node(dsim_entity,"flightmodel/configuration/inertia/i_xz"))
flightmodel_configuration_inertia_i_yy = DSim.Variable.Double(DSim.Node(dsim_entity,"flightmodel/configuration/inertia/i_yy"))
flightmodel_configuration_inertia_i_zz = DSim.Variable.Double(DSim.Node(dsim_entity,"flightmodel/configuration/inertia/i_zz"))

flightmodel_module_simple_scas_input_scas_pitch_on = DSim.Variable.Double(DSim.Node(dsim_entity,"flightmodel/module/simple_scas/input/scas/pitch_on"))
flightmodel_module_simple_scas_input_scas_roll_on = DSim.Variable.Double(DSim.Node(dsim_entity,"flightmodel/module/simple_scas/input/scas/roll_on"))
flightmodel_module_simple_scas_input_scas_yaw_on = DSim.Variable.Double(DSim.Node(dsim_entity,"flightmodel/module/simple_scas/input/scas/yaw_on"))

hardware_panel_center_hydraulics_xmsn_nr_p10 = DSim.Variable.Double(DSim.Node(dsim_entity,"hardware/panel/center/hydraulics_xmsn/nr_p10"))


environment_weather_temperature = DSim.Variable.Double(DSim.Node(dworld_entity,"environment/weather/temperature"))
environment_weather_layer_1_wind_direction = DSim.Variable.Double(DSim.Node(dworld_entity,"environment/weather/layer/1/wind/direction"))
environment_weather_layer_1_wind_speed = DSim.Variable.Double(DSim.Node(dworld_entity,"environment/weather/layer/1/wind/speed"))
environment_weather_layer_1_top = DSim.Variable.Double(DSim.Node(dworld_entity,"environment/weather/layer/1/top"))

def CLS(inp):
    brunner_task = DSim.Variable.Enum(DSim.Node(dsim_host,"host/sim1-model/entity/as532_1/task/io_brunner_cls/mode"))
    if inp == 'S':
        brunner_task.write(TASK_MODE.FORCE_STOP) 
    elif inp == 'R':
        brunner_task.write(TASK_MODE.FORCE_RUN)

def CLS_val_INIT():
    return 0,0,0,0,0,0,0,0
        
def CLS_READER_INIT():
    def build_get_pos_query(axisbitmask):
        return struct.pack('<III', 0xD0, axisbitmask, 0x11)

    def build_get_force_query(axisbitmask):
        return struct.pack('<III', 0xD0, axisbitmask, 0x21)

    timeout = 8
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 5)
    sock.settimeout(timeout)
    sock.bind(('', 0))

    # set IP of computer running CLS2Sim
    remoteEndpoint = ('10.12.1.11', 15090)
    # define binary byte sequences for commands to send over network

    # Command GetData(0xD0), For axes 0x1 and 0x2 (pitch,roll) (= 0x3) and read force as float (dataid 0x21)
    query_readforce_pitch_roll = build_get_force_query(AxisBitmask.Elevator + AxisBitmask.Aileron)
    query_readforce_yaw_coll = build_get_force_query(AxisBitmask.Rudder + AxisBitmask.Collective)
    return sock, remoteEndpoint, query_readforce_pitch_roll, query_readforce_yaw_coll

def logandsave_flyout_init_cond(QTG_path):

    Eng1state = 'FLIGHT' if configuration_failure_engine_1_failed.read() == False else 'OFF'
    Eng2state = 'FLIGHT' if configuration_failure_engine_2_failed.read() == False else 'OFF'
    HINR = 'NORMAL' if hardware_panel_center_hydraulics_xmsn_nr_p10.read() == False else 'HINR'
    AFCS = 'OFF' if flightmodel_module_simple_scas_input_scas_pitch_on.read() == False and flightmodel_module_simple_scas_input_scas_roll_on.read() == False and flightmodel_module_simple_scas_input_scas_yaw_on.read() == False else 'SCAS'
    TM = ' - '
    
    init_cond_log_dict = {                                                                              #FTD3 -> FTD1
       'Gross Weight': configuration_loading_empty_mass.read(),                                         #kg -> kg
       'Fuel Weigth' : configuration_loading_fuel_mass.read(),                                          #kg -> kg
       'CG Longitudinal': flightmodel_configuration_cg_x.read(),                                        #m -> mm
       'CG Lateral': flightmodel_configuration_cg_y.read(),                                             #m -> mm
       'Moment of Inertia XX' : flightmodel_configuration_inertia_i_xx.read(),                          #kgm2 -> kgm2
       'Moment of Inertia XZ' : flightmodel_configuration_inertia_i_xz.read(),                          #kgm2 -> kgm2
       'Moment of Inertia YY' : flightmodel_configuration_inertia_i_yy.read(),                          #kgm2 -> kgm2
       'Moment of Inertia ZZ' : flightmodel_configuration_inertia_i_zz.read(),                          #kgm2 -> kgm2
       'Pressure Altitude' : reference_frame_inertial_position_altitude.read(),                         #m -> ft
       'OAT' : environment_weather_temperature.read(),                                                  #C -> C
       'Wind Direction' : environment_weather_layer_1_wind_direction.read(),                            #deg -> deg
       'Wind Speed' : environment_weather_layer_1_wind_speed.read(),                                    #kt -> kt
       'Airspeed' : reference_frame_body_freestream_airspeed.read(),                                    #m/s -> kt
       'Ground Speed' : reference_frame_inertial_position_v_xy.read(),                                  #m/s -> kt
       'Vertical Velocity' : reference_frame_inertial_position_v_z.read(),                              #m/s -> fpm
       'Radar Altitude' : radio_altimeter_altitude.read(),                                              #ft -> ft
       'Rotor Speed' : transmisson_n_r.read(),                                                          #rad/s -> %
       'Engine 1 Torque' : engine_1_torque.read(),                                                      #% -> %
       'Engine 2 Torque' : engine_2_torque.read(),                                                      #% -> %
       'Pitch Angle' : reference_frame_inertial_attitude_theta.read(),                                  #deg -> deg
       'Bank Angle' : reference_frame_inertial_attitude_phi.read(),                                     #deg -> deg
       'Heading' : reference_frame_inertial_attitude_psi.read(),                                        #deg -> deg
       'Pitch Rate' : reference_frame_body_attitude_q.read(),                                           #deg/s -> deg/s
       'Roll Rate' : reference_frame_body_attitude_p.read(),                                            #deg/s -> deg/s
       'Yaw Rate' : reference_frame_body_attitude_r.read(),                                             #deg/s -> deg/s
       'X Body Acceleration' : reference_frame_inertial_position_a_x.read(),                            #m/s2 -> m/s2
       'Y Body Acceleration' : reference_frame_inertial_position_a_y.read(),                            #m/s2 -> m/s2
       'Z Body Acceleration' : reference_frame_inertial_position_a_z.read(),                            #m/s2 -> m/s2
       'Longitudinal Cyclic Pos.' : hardware_pilot_cyclic_longitudinal_position.read(),                 #% -> 1
       'Lateral Cyclic Pos.' : hardware_pilot_cyclic_lateral_position.read(),                           #% -> 1
       'Pedals Pos.' : hardware_pilot_pedals_position.read(),                                           #% -> 1
       'Collective Pos.' : hardware_pilot_collective_position.read(),                                   #% -> 1
       'Engine 1 Main Switch' : Eng1state,
       'Engine 2 Main Switch' : Eng2state,
       'AFCS State' : AFCS,                                                                 #SCAS on =5e-324 SCAS off = 0.0
       'HINR Button' : HINR,                                                                 #HINR on = 5e-324 HINR off = 0.0
       'Training Mode' : TM
        }
    
    #Save the date
    date = datetime.now()
    date = date.strftime("_%Y_%m_%d_%H_%M")
    
    filename_date = 'init_conditions.json'
    
    
    init_cond_FTD_path = os.path.join(QTG_path, filename_date)
    
    with open(init_cond_FTD_path, 'r') as json_file:
        data = json.load(json_file)
    
    data["Init_condition_Reccurent"] = init_cond_log_dict
    with open(init_cond_FTD_path, 'w') as json_file:
         json.dump(data, json_file, indent=4)
    
    
        
    print(filename_date + ' wurde unter ' + QTG_path + ' gespeichert!')
    
def math_pilot(QTG_path,T):
    MQTG_input_matrix = np.empty((len(T),INPUT.NUMBER_OF_INPUTS))
    output_matrix = np.empty((len(T),OUTPUT.NUMBER_OF_OUTPUTS))
    input_matrix = np.empty((len(T),INPUT.NUMBER_OF_INPUTS))
    
    #Get Reference control arrays
    Input_paths = [
    os.path.join(QTG_path,'Control Position Collective.XY.qtgplot.sim'),
    os.path.join(QTG_path,'Control Position Roll.XY.qtgplot.sim'),
    os.path.join(QTG_path,'Control Position Pitch.XY.qtgplot.sim'),
    os.path.join(QTG_path,'Control Position Yaw.XY.qtgplot.sim')]
    
    for path, i in zip(Input_paths,range(INPUT.NUMBER_OF_INPUTS)):
        with open(path, 'r') as json_file:
            data = json.load(json_file)
        MQTG_input_matrix[:,i] = data["FTD1"]["y"]
    


    

    i = 0
    simulation_mode.write(SIM_MODE.RUN) 
    
    while i < len(T)-1:
        hardware_pilot_collective_position.write(MQTG_input_matrix[i,INPUT.COLLECTIVE])
        hardware_pilot_cyclic_lateral_position.write(MQTG_input_matrix[i,INPUT.CYCLIC_LATERAL])
        hardware_pilot_cyclic_longitudinal_position.write(MQTG_input_matrix[i,INPUT.CYCLIC_LONGITUDINAL])
        hardware_pilot_pedals_position.write(MQTG_input_matrix[i,INPUT.PEDALS])
        
        input_matrix[i,INPUT.COLLECTIVE] = hardware_pilot_collective_position.read()
        input_matrix[i,INPUT.CYCLIC_LATERAL] = hardware_pilot_cyclic_lateral_position.read()
        input_matrix[i,INPUT.CYCLIC_LONGITUDINAL] = hardware_pilot_cyclic_longitudinal_position.read()
        input_matrix[i,INPUT.PEDALS] = hardware_pilot_pedals_position.read()

        output_matrix[i,OUTPUT.AIRSPEED] = reference_frame_body_freestream_airspeed.read()
        output_matrix[i,OUTPUT.GROUNDSPEED] = reference_frame_inertial_position_v_xy.read()
        output_matrix[i,OUTPUT.RADARALT] = radio_altimeter_altitude.read()
        output_matrix[i,OUTPUT.E1TRQ] = engine_1_torque.read()
        output_matrix[i,OUTPUT.E2TRQ] = engine_2_torque.read()
        output_matrix[i,OUTPUT.ROTORSPEED] = transmisson_n_r.read()
        output_matrix[i,OUTPUT.PITCH] = reference_frame_inertial_attitude_theta.read()
        output_matrix[i,OUTPUT.BANK] = reference_frame_inertial_attitude_phi.read()
        output_matrix[i,OUTPUT.HEADING] = reference_frame_inertial_attitude_psi.read()
        output_matrix[i,OUTPUT.PITCHRATE] = reference_frame_body_attitude_q.read()
        output_matrix[i,OUTPUT.ROLLRATE] = reference_frame_body_attitude_p.read()
        output_matrix[i,OUTPUT.YAWRATE] = reference_frame_body_attitude_r.read()
        output_matrix[i,OUTPUT.VERTICALSPEED] = reference_frame_inertial_position_v_z.read()
        output_matrix[i,OUTPUT.SIDESLIP] = reference_frame_body_freestream_beta.read()

        # sleep for dT amount of seconds
        dT = T[i+1]-T[i]
        time.sleep(dT)
        # increment data row index
        i += 1

    simulation_mode.write(SIM_MODE.PAUSE)
    return input_matrix, output_matrix

def log_flyout_input_output(T):
    # pre-define numpy data matrix containing flight data (see enum above for column definitions)
    input_matrix = np.empty((len(T),INPUT.NUMBER_OF_INPUTS))
    output_matrix = np.empty((len(T),OUTPUT.NUMBER_OF_OUTPUTS))
    
    sock, remoteEndpoint, query_readforce_pitch_roll, query_readforce_yaw_coll = CLS_READER_INIT()
    force_pitch, force_roll, force_yaw, force_coll = 0,0,0,0
    prev_force_pitch, prev_force_roll, prev_force_yaw, prev_force_coll = 0,0,0,0
    def sendThenReceive(send_data, targetAddr, sock):
        # after each send you HAVE to do a read, even if you don't do anything with the reponse
        sock.sendto(send_data, targetAddr)
        response, address = sock.recvfrom(8192)
        return response

    number_format = '{:+.5f}'
    force_matrix = np.empty((len(T),INPUT.NUMBER_OF_INPUTS))


    accumulated_time = 0
    i = 0

    while i < len(T)-1:
        input_matrix[i,INPUT.COLLECTIVE] = hardware_pilot_collective_position.read()
        input_matrix[i,INPUT.CYCLIC_LATERAL] = hardware_pilot_cyclic_lateral_position.read()
        input_matrix[i,INPUT.CYCLIC_LONGITUDINAL] = hardware_pilot_cyclic_longitudinal_position.read()
        input_matrix[i,INPUT.PEDALS] = hardware_pilot_pedals_position.read()
        
        output_matrix[i,OUTPUT.AIRSPEED] = reference_frame_body_freestream_airspeed.read()
        output_matrix[i,OUTPUT.GROUNDSPEED] = reference_frame_inertial_position_v_xy.read()
        output_matrix[i,OUTPUT.RADARALT] = radio_altimeter_altitude.read()
        output_matrix[i,OUTPUT.E1TRQ] = engine_1_torque.read()
        output_matrix[i,OUTPUT.E2TRQ] = engine_2_torque.read()
        output_matrix[i,OUTPUT.ROTORSPEED] = transmisson_n_r.read()
        output_matrix[i,OUTPUT.PITCH] = reference_frame_inertial_attitude_theta.read()
        output_matrix[i,OUTPUT.BANK] = reference_frame_inertial_attitude_phi.read()
        output_matrix[i,OUTPUT.HEADING] = reference_frame_inertial_attitude_psi.read()
        output_matrix[i,OUTPUT.PITCHRATE] = reference_frame_body_attitude_q.read()
        output_matrix[i,OUTPUT.ROLLRATE] = reference_frame_body_attitude_p.read()
        output_matrix[i,OUTPUT.YAWRATE] = reference_frame_body_attitude_r.read()
        output_matrix[i,OUTPUT.VERTICALSPEED] = reference_frame_inertial_position_v_z.read()
        output_matrix[i,OUTPUT.SIDESLIP] = reference_frame_body_freestream_beta.read()
        

        #Read control forces
        force_response_pitch_roll = sendThenReceive(query_readforce_pitch_roll, remoteEndpoint, sock)
        force_response_yaw_coll = sendThenReceive(query_readforce_yaw_coll, remoteEndpoint, sock)
        length, status, node_pitch, force_pitch, node_roll, force_roll = struct.unpack('<HBHfHf', force_response_pitch_roll)
        length, status, node_yaw, force_yaw, node_coll, force_coll = struct.unpack('<HBHfHf', force_response_yaw_coll)
        force_matrix[i,INPUT.CYCLIC_LONGITUDINAL] = number_format.format(force_pitch)
        force_matrix[i,INPUT.CYCLIC_LATERAL] = number_format.format(force_roll)
        force_matrix[i,INPUT.PEDALS] = number_format.format(force_yaw)    
        force_matrix[i,INPUT.COLLECTIVE] = number_format.format(force_coll)  
        # sleep for dT amount of seconds
        dT = T[i+1]-T[i]
        accumulated_time +=dT
        time.sleep(dT)
        
        if int(accumulated_time) > int(accumulated_time - dT):
            print(round(accumulated_time-dT))
            
        if prev_force_pitch != force_pitch \
            or prev_force_roll != force_roll \
            or prev_force_yaw != force_yaw \
            or prev_force_coll != force_coll:
            prev_force_pitch = force_pitch
            prev_force_roll = force_roll
            prev_force_yaw = force_yaw
            prev_force_coll = force_coll

        
        # increment data row index
        i += 1
    sock.close()
    simulation_mode.write(SIM_MODE.PAUSE)
    return input_matrix, output_matrix, force_matrix


def save_io_files(QTG_path, input_matrix, output_matrix, force_matrix, T):
    Input_paths = [
        os.path.join(QTG_path, 'Control Position Collective.XY.qtgplot.sim'),
        os.path.join(QTG_path, 'Control Position Roll.XY.qtgplot.sim'),
        os.path.join(QTG_path, 'Control Position Pitch.XY.qtgplot.sim'),
        os.path.join(QTG_path, 'Control Position Yaw.XY.qtgplot.sim')]

    Output_paths = [
        os.path.join(QTG_path, 'Indicated Airspeed.XY.qtgplot.sim'),
        os.path.join(QTG_path, 'Groundspeed.XY.qtgplot.sim'),
        os.path.join(QTG_path, 'RadarAltitude.XY.qtgplot.sim'),
        os.path.join(QTG_path, 'Engine1 TRQ Indicated.XY.qtgplot.sim'),
        os.path.join(QTG_path, 'Engine2 TRQ Indicated.XY.qtgplot.sim'),
        os.path.join(QTG_path, 'Rotor RPM.XY.qtgplot.sim'),
        os.path.join(QTG_path, 'Pitch Angle.XY.qtgplot.sim'),
        os.path.join(QTG_path, 'Roll Angle.XY.qtgplot.sim'),
        os.path.join(QTG_path, 'Yaw Angle Unwrapped.XY.qtgplot.sim'),
        os.path.join(QTG_path, 'Pitch Angle Rate.XY.qtgplot.sim'),
        os.path.join(QTG_path, 'Roll Angle Rate.XY.qtgplot.sim'),
        os.path.join(QTG_path, 'Yaw Angle Rate.XY.qtgplot.sim'),
        os.path.join(QTG_path, 'Vertical Speed.XY.qtgplot.sim'),
        os.path.join(QTG_path, 'Angle of Sideslip.XY.qtgplot.sim')  	
    ]

    Force_paths = [
        os.path.join(QTG_path, 'Control QTG Force Collective.XY.qtgplot.sim'),
        os.path.join(QTG_path, 'Control QTG Force Roll.XY.qtgplot.sim'),
        os.path.join(QTG_path, 'Control QTG Force Pitch.XY.qtgplot.sim'),
        os.path.join(QTG_path, 'Control QTG Force Yaw.XY.qtgplot.sim')]

    Atrim_paths = [
        os.path.join(QTG_path, 'Control QTG Position Roll Velocity.XY.qtgplot.sim'),
        os.path.join(QTG_path, 'Control QTG Position Pitch Velocity.XY.qtgplot.sim')]

    for path, i in zip(Input_paths, range(INPUT.NUMBER_OF_INPUTS)):
        with open(path, 'r') as json_file:
            data = json.load(json_file)

        data["FTD1_Recurrent"] = {
            "x": T.tolist(), "y": input_matrix[:, i].tolist()
        }
        with open(path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    for path, i in zip(Output_paths, range(OUTPUT.NUMBER_OF_OUTPUTS)):
        try:
            with open(path, 'r') as json_file:
                data = json.load(json_file)
        except:
            continue

        data["FTD1_Recurrent"] = {
            "x": T.tolist(), "y": output_matrix[:, i].tolist()
        }
        with open(path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    for path, i in zip(Force_paths, range(INPUT.NUMBER_OF_INPUTS)):
        try:
            with open(path, 'r') as json_file:
                data = json.load(json_file)
        except:
            continue
        data["FTD1_Recurrent"] = {
            "x": input_matrix[:, i].tolist(), "y": force_matrix[:, i].tolist()
        }
        with open(path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    for path, i in zip(Atrim_paths, range(1, 3)):
        try:
            with open(path, 'r') as json_file:
                data = json.load(json_file)
        except:
            continue
        data["FTD1_Recurrent"] = {
            "x": T.tolist(), "y": input_matrix[:, i].tolist()
        }
        with open(path, 'w') as json_file:
            json.dump(data, json_file, indent=4)


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

             
             
             
        
    #print(filename_date + ' wurde unter ' + QTG_path + ' gespeichert!')
# def map_control(x):return round(50 * (x + 1),2)#Brunner2Moog
# def inv_map_control(x):return (x/50)-1 #Moog2Brunner
# def rpm2perc(x): return round((np.rad2deg(x) / 1590) * 100,2)
# def perc2rpm(x): return round(((np.deg2rad(x) / 100) * 1590),2)
# def m2ft(x): return x*3.281
# def ft2m(x): return x*(1/3.281)
# def mps2fpm(x): return x*196.9
# def fpm2mps(x): return x*(1/196.9)
# def mps2kt(x): return x*1.944
# def kt2mps(x): return x*(1/1.944)
# def map360(x): return round(x%360,2)
#
# def pitch_brun2angle(x):
#     #Factors for the control angles
#     pitchP_factor_pos = 12.5
#     pitchP_factor_neg = 12.3
#     x=x*pitchP_factor_pos if x > 0 else x*pitchP_factor_neg
#     #x[x>0] *= pitchP_factor_pos
#     #x[x<0] *= pitchP_factor_neg
#     return x
#
# def roll_brun2angle(x):
#     #Factors for the control angles
#     rollP_factor_pos = 10.2
#     rollP_factor_neg = 10.1
#     x=x*rollP_factor_pos if x > 0 else x*rollP_factor_neg
#     #x[x>0] *= rollP_factor_pos
#     #x[x<0] *= rollP_factor_neg
#     return x
#
# def yaw_brun2angle(x):
#     yawP_factor_pos = 17.5
#     yawP_factor_neg = 21.7
#     x=x*yawP_factor_pos if x > 0 else x*yawP_factor_neg
#     #x[x>0] *= yawP_factor_pos
#     #x[x<0] *= yawP_factor_neg
#     return x
#
# def coll_brun2angle(x):
#     collP_factor_pos = 28
#     x=x*collP_factor_pos
#     #x[x>0] *= collP_factor_pos
#     return x
#
# def pitch_brun2N(x):
#     #Cyclic: Abstand Griff zu Drehpunkt_Longitudinal
#     L_P = 0.7124
#     x = x*100/L_P
#     return x
# def roll_brun2N(x):
#     #Cyclic: Abstand Griff zu Drehpunkt_Lateral_Longitudinal
#     L_R = 0.7806
#     x = x*100/L_R
#     return x
#
# def coll_brun2N(x):
#     #Collective: Abstand Griff zu Drehpunkt
#     LC = 0.61
#     x = x*100/LC
#     return x
#
# def ATRIM_calc(x,y):
#
#     x = np.array(x)
#     x = x[::60]
#     y = abs(np.array(y))
#     y = y[::60]
#     rate = np.diff(y)/np.diff(x)
#     return rate, x[:-1]
#
#
# #Gross Weight
# #Linear interpolation of GW:
# #EC135T2+ min. GW = 1700kg max.GW = 2980kg
# #AS532 min. GW = 4500kg max.GW = 8600kg
# def GW_map(x):
#     return 4500+(4100/1280)*(float(x)-1700)
#
# #CG_Long
# #Linear interpolation of CG_x:
# #EC135T2+ max.AFT = 4541mm max.FWD=4121mm
# #AS532 max.AFT = -4.97m max.FWD=-4.47m
# def CG_x_map(x):
#     return -4.97+(0.5/-0.42)*(x-4.541)
#
# def units_conversion(init_cond_dict,unit):
#
#     m2ft = 3.281
#     ft2m = 1/m2ft
#     mps2fpm = 196.9
#     fpm2mps = 1/mps2fpm
#     mps2kt = 1.944
#     kt2mps = 1/mps2kt
#     m2mm = 1e3
#     mm2m = 1/m2mm
#
#     if unit == 'SI':
#         init_cond_dict_SI = init_cond_dict
#
#         init_cond_dict_SI['CG Longitudinal'] = round(float(init_cond_dict['CG Longitudinal'])*mm2m,2)
#         init_cond_dict_SI['CG Lateral'] = round(float(init_cond_dict['CG Lateral'])*mm2m,2)
#         init_cond_dict_SI['Pressure Altitude']  = round(float(init_cond_dict['Pressure Altitude'])*ft2m,2)
#         init_cond_dict_SI['Wind Direction'] = round(np.deg2rad(float(init_cond_dict['Wind Direction'])),2)
#         init_cond_dict_SI['Wind Speed'] = round(float(init_cond_dict['Wind Speed'])*kt2mps,2)
#         init_cond_dict_SI['Airspeed'] = round(float(init_cond_dict['Airspeed'])*kt2mps,2)
#         init_cond_dict_SI['Ground Speed'] = round(float(init_cond_dict['Ground Speed'])*kt2mps,2)
#         init_cond_dict_SI['Vertical Velocity'] = round(float(init_cond_dict['Vertical Velocity'])*fpm2mps,2)
#         if init_cond_dict['Radar Altitude'] == 'N/A':
#             init_cond_dict_SI['Radar Altitude'] = 'N/A'
#         else:
#             init_cond_dict_SI['Radar Altitude'] = round(float(init_cond_dict['Radar Altitude'])*ft2m,2)
#         init_cond_dict_SI['Rotor Speed'] = perc2rpm(float(init_cond_dict['Rotor Speed']))
#         init_cond_dict_SI['Engine 1 Torque'] = round(float(init_cond_dict['Engine 1 Torque']),2)
#         init_cond_dict_SI['Engine 2 Torque'] = round(float(init_cond_dict['Engine 2 Torque']),2)
#         init_cond_dict_SI['Pitch Angle'] = round(np.deg2rad(float(init_cond_dict['Pitch Angle'])),2)
#         init_cond_dict_SI['Bank Angle']  = round(np.deg2rad(float(init_cond_dict['Bank Angle'])),2)
#         init_cond_dict_SI['Heading'] = round(np.deg2rad(float(init_cond_dict['Heading'])),2)
#         init_cond_dict_SI['Pitch Rate'] = round(np.deg2rad(float(init_cond_dict['Pitch Rate'])),2)
#         init_cond_dict_SI['Roll Rate'] = round(np.deg2rad(float(init_cond_dict['Roll Rate'])),2)
#         init_cond_dict_SI['Yaw Rate'] = round(np.deg2rad(float(init_cond_dict['Yaw Rate'])),2)
#         init_cond_dict_SI['Longitudinal Cyclic Pos.'] = inv_map_control(float(init_cond_dict['Longitudinal Cyclic Pos.']))
#         init_cond_dict_SI['Lateral Cyclic Pos.'] = inv_map_control(float(init_cond_dict['Lateral Cyclic Pos.']))
#         init_cond_dict_SI['Pedals Pos.'] = inv_map_control(float(init_cond_dict['Pedals Pos.']))
#         init_cond_dict_SI['Collective Pos.'] = inv_map_control(float(init_cond_dict['Collective Pos.']))
#         return init_cond_dict_SI
#
#     elif unit == 'Avi':
#         init_cond_dict_Avi = init_cond_dict
#         init_cond_dict_Avi['CG Longitudinal'] = round(float(init_cond_dict['CG Longitudinal'])*m2mm,2)
#         init_cond_dict_Avi['CG Lateral'] = round(float(init_cond_dict['CG Lateral'])*m2mm,1)
#         init_cond_dict_Avi['Pressure Altitude']  = round(float(init_cond_dict['Pressure Altitude'])*m2ft,2)
#         init_cond_dict_Avi['Wind Direction'] = round(np.rad2deg(float(init_cond_dict['Wind Direction'])),2)
#         init_cond_dict_Avi['Wind Speed'] = round(float(init_cond_dict['Wind Speed'])*mps2kt,2)
#         init_cond_dict_Avi['Airspeed'] = round(float(init_cond_dict['Airspeed'])*mps2kt,2)
#         init_cond_dict_Avi['Ground Speed'] = round(float(init_cond_dict['Ground Speed'])*mps2kt,2)
#         init_cond_dict_Avi['Vertical Velocity'] = round(float(init_cond_dict['Vertical Velocity'])*mps2fpm,2)
#         init_cond_dict_Avi['Radar Altitude'] = round(float(init_cond_dict['Radar Altitude']),2)
#         init_cond_dict_Avi['Rotor Speed'] = rpm2perc(float(init_cond_dict['Rotor Speed']))
#         init_cond_dict_Avi['Engine 1 Torque'] = round(float(init_cond_dict['Engine 1 Torque']),2)
#         init_cond_dict_Avi['Engine 2 Torque'] = round(float(init_cond_dict['Engine 2 Torque']),2)
#         init_cond_dict_Avi['Pitch Angle'] = round(np.rad2deg(float(init_cond_dict['Pitch Angle'])),2)
#         init_cond_dict_Avi['Bank Angle']  = round(np.rad2deg(float(init_cond_dict['Bank Angle'])),2)
#         init_cond_dict_Avi['Heading'] = map360(np.rad2deg(float(init_cond_dict['Heading'])))
#         init_cond_dict_Avi['Pitch Rate'] = round(np.rad2deg(float(init_cond_dict['Pitch Rate'])),2)
#         init_cond_dict_Avi['Roll Rate'] = round(np.rad2deg(float(init_cond_dict['Roll Rate'])),2)
#         init_cond_dict_Avi['Yaw Rate'] = round(np.rad2deg(float(init_cond_dict['Yaw Rate'])),2)
#         init_cond_dict_Avi['Longitudinal Cyclic Pos.'] = map_control(float(init_cond_dict['Longitudinal Cyclic Pos.']))
#         init_cond_dict_Avi['Lateral Cyclic Pos.'] = map_control(float(init_cond_dict['Lateral Cyclic Pos.']))
#         init_cond_dict_Avi['Pedals Pos.'] = map_control(float(init_cond_dict['Pedals Pos.']))
#         init_cond_dict_Avi['Collective Pos.'] = map_control(float(init_cond_dict['Collective Pos.']))
#         return init_cond_dict_Avi
        
    
def set_standard_cond():
    configuration_loading_empty_mass.write(7500)
    flightmodel_configuration_cg_x.write(-4.7)
    configuration_failure_engine_1_failed.write(False)
    configuration_failure_engine_2_failed.write(False)
    hardware_pilot_collective_position.write(-1)
    hardware_pilot_cyclic_lateral_position.write(0)
    hardware_pilot_cyclic_longitudinal_position.write(0)
    hardware_pilot_pedals_position.write(0)
    

def set_init_cond_flyout(init_cond_dict):
    ON = 5e-324 
    

    #Positions
    #coordiantes LOWL RW26:
    LOWL = [48.23380,14.20719]
    reference_frame_inertial_position_latitude.write(LOWL[0])
    reference_frame_inertial_position_longitude.write(LOWL[1])
        
    
    configuration_loading_empty_mass.write(float(init_cond_dict['Gross Weight']))
    flightmodel_configuration_cg_x.write(float(init_cond_dict['CG Longitudinal']))
    
    #x -> Pitch achse CG
    #y -> Rollachsen CG
    #z -> Hohe
    #cg -> Lateral rechts -> y+
    #cg -> Long vorne -> x+
    
    #Enviromental Parameter
    #reference_frame_inertial_position_altitude.write(float(init_cond_dict['Pressure Altitude']))
    environment_weather_temperature.write(float(init_cond_dict['OAT']))
    environment_weather_layer_1_wind_direction.write(float(init_cond_dict['Wind Direction']))
    environment_weather_layer_1_wind_speed.write(float(init_cond_dict['Wind Speed']))
    environment_weather_layer_1_top.write(ft2m(14000)) #Set weather layer up to 14000ft

    
    #Flight Parameters
    reference_frame_inertial_position_v_xy.write(float(init_cond_dict['Ground Speed']))
    reference_frame_inertial_attitude_psi.write(float(init_cond_dict['Heading']))

    configuration_failure_engine_1_failed.write(False) if init_cond_dict['Engine 1 Main Switch'] == 'FLIGHT' else configuration_failure_engine_1_failed.write(True)
    configuration_failure_engine_2_failed.write(False) if init_cond_dict['Engine 2 Main Switch'] == 'FLIGHT' else configuration_failure_engine_2_failed.write(True)
    
# =============================================================================
#     hardware_pilot_collective_position.write(float(init_cond_dict["Collective Pos."]))
#     hardware_pilot_cyclic_lateral_position.write(float(init_cond_dict["Lateral Cyclic Pos."]))
#     hardware_pilot_cyclic_longitudinal_position.write(float(init_cond_dict["Longitudinal Cyclic Pos."]))
#     hardware_pilot_pedals_position.write(float(init_cond_dict["Pedals Pos."]))
# =============================================================================

    hardware_panel_center_hydraulics_xmsn_nr_p10.write(False) if init_cond_dict['HINR Button'] == 'NORMAL' else hardware_panel_center_hydraulics_xmsn_nr_p10.write(False)
    if init_cond_dict['AFCS State'] == 'DSAS':
        flightmodel_module_simple_scas_input_scas_pitch_on.write(ON) 
        flightmodel_module_simple_scas_input_scas_roll_on.write(ON) 
        flightmodel_module_simple_scas_input_scas_yaw_on.write(ON) 
    else:
        flightmodel_module_simple_scas_input_scas_pitch_on.write(ON)
        flightmodel_module_simple_scas_input_scas_roll_on.write(ON)
        flightmodel_module_simple_scas_input_scas_yaw_on.write(ON)


def get_QTG_init_cond_ref(QTG_path):
    init_cond_ref_path = os.path.join(QTG_path, 'init_conditions.json')
    with open(init_cond_ref_path, 'r') as json_file:
        init_cond_ref_dict = json.load(json_file)
    return init_cond_ref_dict["Init_condition_MQTG"]


def get_QTG_path(QTG_name, Refernce_data_path):
    for subdir, _, files in os.walk(Refernce_data_path):
        if QTG_name in subdir:
            return subdir


def get_QTG_time(QTG_path):
    Time_path = os.path.join(QTG_path, 'Time.XY.qtgplot.sim')
    with open(Time_path, 'r') as json_file:
        time_dict = json.load(json_file)
        T = time_dict['Storage'][0]['x']
        T = np.array(T) 
    return T


def create_report(QTG_path, report_file):
    output_path = os.path.join(QTG_path, report_file)
    if os.path.exists(output_path):
        os.remove(output_path)
    
    pdf_merger = PdfMerger()
    # Gehe durch alle Dateien im Ordner
    for root, dirs, files in os.walk(QTG_path):
        for file in sorted(files):
            if file.endswith('.pdf'):
                # Voller Pfad der PDF-Datei
                file_path = os.path.join(root, file)
                pdf_merger.append(file_path)

    # Speichere die zusammengeführte PDF
    
    pdf_merger.write(output_path)
    pdf_merger.close()
    

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


# Function to get the test and the specific test part
def get_test_test_part_test_case(tests, test_id, part_id, case_id):
    # Find the test with the given id
    test = next((test for test in tests if test['id'] == test_id), None)
    if test:
        # Find the test part with the given id within the found test
        test_part = next((part for part in test['test_parts'] if part['id'] == part_id), None)
        if test_part:
            test_case = next((case for case in test_part['test_cases'] if case['id'] == case_id), None)
            return test, test_part, test_case
    return None, None, None



def create_plots(QTG_path, part):

    params = part['tolerances_recurrent_criteria']
    para_file_dict = {
        'Engine 1 Torque':'Engine1 TRQ Indicated',
        'Engine 2 Torque':'Engine2 TRQ Indicated',
        'Rotor Speed' : 'Rotor RPM',
        'Pitch Angle' : 'Pitch Angle',
        'Bank Angle' : 'Roll Angle',
        'Heading' : 'Yaw Angle Unwrapped',
        'Sideslip Angle' : 'Angle of Sideslip',
        'Airspeed' : 'Indicated Airspeed',
        'Radar Altitude' : 'RadarAltitude',
        'Vertical Velocity' : 'Vertical Speed',
        'Longitudinal Cyclic Pos.' : 'Control Position Pitch',
        'Lateral Cyclic Pos.' : 'Control Position Roll',
        'Pedals Pos.' : 'Control Position Yaw',
        'Collective Pos.' : 'Control Position Collective',
        'Pitch Rate' : 'Pitch Angle Rate',
        'Roll Rate' : 'Roll Angle Rate' ,
        'Yaw Rate' : 'Yaw Angle Rate',
        'Correct Trend on Bank' : 'Roll Angle',
        'Force' : 'Control QTG Force',
        'Breakout' : 'dummy'
         
    }
    
    
    for count,param in enumerate(params):
        count = count+1
        plot_title = param['parameter']
        tol = float(param['tolerance'][1:])
        for dirpath, dirnames, filenames in os.walk(QTG_path):     
            for file in filenames:
                #if file.split('.')[0] == para_file_dict[plot_title] and file.endswith('.sim'):
                if para_file_dict[plot_title] in file.split('.')[0]  and file.endswith('.sim'):
                    file_path = os.path.join(dirpath, file)
                    compare_name = file.split('.')[0]
                    break


        try:
            print(file_path)
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
        except:
            continue
        
        if 'FTD1' in data.keys():
            x_Ref = data['Storage'][0]['x']
            y_Ref = data['Storage'][0]['y']
            x = data['FTD1']['x']
            y = data['FTD1']['y']
            x_Rec = data['FTD1_Recurrent']['x']
            y_Rec = data['FTD1_Recurrent']['y']       
        
            y[-1] = y[-2]
            x[-1] = x[-2]
            y_Rec[-1] = y_Rec[-2]
            x_Rec[-1] = x_Rec[-2]
        
            x_label = 'Time(s)'     
            
            if 'Yaw Angle Unwrapped' in para_file_dict[plot_title]:
                y = [map360(i) for i in y]
                y_Rec = [map360(i) for i in y_Rec]
            elif 'Roll Angle' in para_file_dict[plot_title]:
                y=np.rad2deg(y)
                y_Rec=np.rad2deg(y_Rec)
            elif 'Pitch Angle' in para_file_dict[plot_title]:
                y=np.rad2deg(y)
                y_Rec=np.rad2deg(y_Rec)
            elif 'Angle of Sideslip' in para_file_dict[plot_title]:
                y=np.rad2deg(y)
                y_Rec=np.rad2deg(y_Rec)
            elif 'Angle Rate' in para_file_dict[plot_title]:
                y=np.rad2deg(y)
                y_Rec=np.rad2deg(y_Rec)
            elif 'Control Position Pitch' in para_file_dict[plot_title]: #Pitch position Signal ist bei der Referenz invertiert
                y=[map_control(-i) for i in y]
                y_Rec=[map_control(-i) for i in y_Rec]
            elif 'Control Position Collective' in para_file_dict[plot_title]:
                y=[map_control(i) for i in y]
                y_Rec=[map_control(i) for i in y_Rec]
            elif 'Control Position Roll' in para_file_dict[plot_title]:
                y=[map_control(i) for i in y]
                y_Rec=[map_control(i) for i in y_Rec]
            elif 'Control Position Yaw' in para_file_dict[plot_title]:
                y=[map_control(i) for i in y]
                y_Rec=[map_control(i) for i in y_Rec] 
            elif 'Control QTG Force Pitch' in compare_name:
                y = [pitch_brun2N(i) for i in y]
                x = [pitch_brun2angle(i) for i in x]
                y_Rec = [pitch_brun2N(i) for i in y_Rec]
                x_Rec = [pitch_brun2angle(i) for i in x_Rec]
                x_label = 'Position (deg)'
            elif 'Control QTG Force Roll' in compare_name:
                y = [roll_brun2N(i) for i in y]
                x = [roll_brun2angle(i) for i in x]
                y_Rec = [roll_brun2N(i) for i in y_Rec]
                x_Rec = [roll_brun2angle(i) for i in x_Rec]
                x_label = 'Position (deg)'
            elif 'Control QTG Force Collective' in compare_name:
                y = [coll_brun2N(i) for i in y]
                x = [coll_brun2angle(i) for i in x]
                y_Rec = [coll_brun2N(i) for i in y_Rec]
                x_Rec = [coll_brun2angle(i) for i in x_Rec]
                x_label = 'Position (deg)'
            elif 'Control QTG Force Yaw' in compare_name:
                x = [yaw_brun2angle(i) for i in x]
                y = [i*-1000 for i in y]
                x_Rec = [yaw_brun2angle(i) for i in x_Rec]
                y_Rec = [i*-1000 for i in y_Rec]
                x_label = 'Position (deg)'
            elif 'Control QTG Position Pitch Velocity' in para_file_dict[plot_title]:
                y = [pitch_brun2angle(i) for i in y]
                y,x = ATRIM_calc(x, y)
                y_Rec = [pitch_brun2angle(i) for i in y_Rec]
                y_Rec,x_Rec = ATRIM_calc(x_Rec, y_Rec)
            elif 'Control QTG Position Roll Velocity' in para_file_dict[plot_title]:
                y = [coll_brun2angle(i) for i in y]
                y,x = ATRIM_calc(x, y)
                y_Rec = [coll_brun2angle(i) for i in y_Rec]
                y_Rec,x_Rec = ATRIM_calc(x_Rec, y_Rec)
            elif 'Groundspeed' in para_file_dict[plot_title]:
                y=[mps2kt(i) for i in y]
                y_Rec=[mps2kt(i) for i in y_Rec]
            elif 'Airspeed' in para_file_dict[plot_title]:
                y=[mps2kt(i) for i in y]
                y_Rec=[mps2kt(i) for i in y_Rec]
            elif 'Barometric Altitude' in para_file_dict[plot_title]:
                y=[m2ft(i) for i in y]
                y_Rec=[m2ft(i) for i in y_Rec]
            elif 'Vertical' in para_file_dict[plot_title]:
                y=[mps2fpm(-i) for i in y]
                y_Rec=[mps2fpm(-i) for i in y_Rec]
            elif 'Rotor' in para_file_dict[plot_title]:
                y=[rpm2perc(i) for i in y]
                y_Rec=[rpm2perc(i) for i in y_Rec]
            else:
                y_label = plot_title +' (??)'
                pdfname = f"{plot_title}.svg"
            
            
            
            y_uptol = [i+tol for i in y]
            y_lotol = [i-tol for i in y]
            
            pdfname = f"{count}_{plot_title}.svg"
            y_label = plot_title +' '+ param['unit']
    
            plt.figure(figsize=(10, 6))
            plt.plot(x, y_uptol, linewidth=0.5, color='orange', linestyle='dashed')
            plt.plot(x, y_lotol, linewidth=0.5, color='orange', linestyle='dashed')
            
            
            plt.plot(x_Ref, y_Ref, label='Reference')
            plt.plot(x, y, label='FTD1_MQTG')
            plt.plot(x_Rec, y_Rec, label='Reccurent', color='green', linestyle='dashed')
    
            
            ##Section for scale
            sc_fac = 1.5
            plt.autoscale()
            y_min, y_max = plt.ylim()
            y_range = y_max - y_min
            plt.ylim(y_min - y_range*sc_fac, y_max + y_range*sc_fac)
    
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.title(plot_title)
            plt.legend()
            plt.grid(True)
            #plt.show() 
            save_path = os.path.join(dirpath, pdfname)
            
            plt.savefig(save_path, format='pdf')
            plt.close()



def create_comparison_table(QTG_path):

    for dirpath, dirnames, filenames in os.walk(QTG_path): 
        for file in filenames:
            if 'init_conditions' in file:
                file_path = os.path.join(dirpath, file)
                with open(file_path, 'r') as json_file:
                    data = json.load(json_file)
                    
                    

    Init_cond = data["Init_condition_Reccurent"]
    Ref_Init_cond = data["Init_condition_MQTG"]
    
    init_cond_di_avi = units_conversion(Init_cond,'Avi')
    Ref_Init_cond = units_conversion(Ref_Init_cond,'Avi')

    # Erstellen der Tabellendaten
    table_data = [
        ["Parameter [UoM]", "MQTG", "Recurrent"],
        ["Mass Properties", "", ""]
    ]
    
    # Werte aus dict1 und dict2 zusammenführen
    for key in Ref_Init_cond:
        table_data.append([key, Ref_Init_cond[key], init_cond_di_avi.get(key, "")])
        if key == "Moment of Inertia ZZ":
            table_data.append(["Environment Parameters", "", ""])
        if key == "Wind Speed":
            table_data.append(["Flight Parameters", "", ""])
    
    # DataFrame für die Tabelle erstellen
    df = pd.DataFrame(table_data)
    
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
    table_path = os.path.join(QTG_path,"0_Init_cond_table.pdf")
    with PdfPages(table_path) as pdf:
        pdf.savefig(fig, bbox_inches='tight')
    
    print(f"Tabelle erfolgreich als {table_path} gespeichert.")


def main(test_item, test_dir, gui_output, gui_input):
    pass


if __name__ == "__main__":
    
    brunner_task = DSim.Variable.Enum(DSim.Node(dsim_host,"host/sim1-model/entity/as532_1/task/io_brunner_cls/mode"))
    brunner_task.write(TASK_MODE.FORCE_RUN)
    
    #Refernce_data_path = r'D:\entity\rotorsky\as532\resources\MQTG_Comparison_with_MQTG_FTD3\Reference_data_Init_flyout_V2'
    save_data_path = r'D:\entity\rotorsky\as532\resources\MQTG_Comparison_with_MQTG_FTD3\RecurrentQTG_save_manu'
    #Gib den Testnamen an
    QTG_name = '2.a.1_B2'
    test_id, part_id, case_id = split_string(QTG_name)
    test, part, case = get_test_test_part_test_case(qtg_data_structure.data['tests'], test_id, part_id, case_id)

    #Pfad der Referenzdaten und der Speicherdaten, des jeweiligen QTGs
    QTG_path = get_QTG_path(QTG_name, save_data_path)
    #Zeitdauer des Tests
    T = get_QTG_time(QTG_path)
    dT = np.mean(np.diff(T))
    
    #Definiere selbst wie lange der Test dauern soll
    desired_time = 20
    
    
    T = np.arange(0,desired_time,dT)
    
    
    #Hole die Anfangsbedingungen des jeweiligen QTGs
    init_cond_ref_dict = get_QTG_init_cond_ref(QTG_path)
    
    #Schreibe die Anfangsbedingungen des jeweiligen QTGs
    set_init_cond_flyout(init_cond_ref_dict)
    simulation_mode.write(SIM_MODE.PAUSE)
    time.sleep(2)
    simulation_mode.write(SIM_MODE.RUN) 
    input("Hit Enter if Pilot is ready")
    
    
    logandsave_flyout_init_cond(QTG_path)
    
    input_matrix, output_matrix, force_matrix = log_flyout_input_output(T)

    save_io_files(QTG_path, input_matrix, output_matrix, force_matrix, T)
    create_comparison_table(QTG_path)
    create_plots(QTG_path,part)
    create_report(QTG_path, 'Report.pdf')

    
    
    set_standard_cond()
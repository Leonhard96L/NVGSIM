# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 08:16:26 2024

@author: simulator
"""
import os, sys, enum, ctypes
from enum import IntEnum
import time



dsim_root_directory = os.path.join(os.path.dirname(sys.path[0]), "D:/")
sys.path.append(os.path.join(dsim_root_directory, "entity/multisim/dsim/sdk/python/include"))
sys.path.append(os.path.join(dsim_root_directory, "entity/multisim/simulation/sdk/python/include"))

import DSim
import ctypes
import numpy as np

# get more accurate timer (using windows multimedia dll)
winmm = ctypes.WinDLL('winmm')
winmm.timeBeginPeriod(1)

# host definition
dsim_host = DSim.Entity("sim1")
# entity definition
dsim_entity   = DSim.Entity("ec135_1")

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
    


reference_frame_inertial_attitude_phi = DSim.Variable.Double(DSim.Node(dsim_entity,"reference_frame/inertial/attitude/phi"))
reference_frame_inertial_attitude_theta = DSim.Variable.Double(DSim.Node(dsim_entity,"reference_frame/inertial/attitude/theta"))
reference_frame_inertial_attitude_psi = DSim.Variable.Double(DSim.Node(dsim_entity,"reference_frame/inertial/attitude/psi"))
reference_frame_inertial_position_latitude = DSim.Variable.Double(DSim.Node(dsim_entity,"reference_frame/inertial/position/latitude"))
reference_frame_inertial_position_longitude = DSim.Variable.Double(DSim.Node(dsim_entity,"reference_frame/inertial/position/longitude"))
reference_frame_inertial_position_altitude = DSim.Variable.Double(DSim.Node(dsim_entity,"reference_frame/inertial/position/altitude"))
reference_frame_inertial_position_v_xy = DSim.Variable.Double(DSim.Node(dsim_entity,"reference_frame/inertial/position/v_xy")) #Forward speed
reference_frame_body_freestream_airspeed = DSim.Variable.Double(DSim.Node(dsim_entity,"reference_frame/body/freestream/v_x"))



hardware_pilot_collective_position = DSim.Variable.Double(DSim.Node(dsim_entity,"hardware/pilot/collective/position"))
hardware_pilot_collective_trim_position = DSim.Variable.Double(DSim.Node(dsim_entity,"hardware/pilot/collective/trim/position"))
hardware_pilot_cyclic_lateral_position = DSim.Variable.Double(DSim.Node(dsim_entity,"hardware/pilot/cyclic/lateral/position"))
hardware_pilot_cyclic_lateral_trim_position = DSim.Variable.Double(DSim.Node(dsim_entity,"hardware/pilot/cyclic/lateral/trim/position"))
hardware_pilot_cyclic_longitudinal_position = DSim.Variable.Double(DSim.Node(dsim_entity,"hardware/pilot/cyclic/longitudinal/position"))
hardware_pilot_cyclic_longitudinal_trim_position = DSim.Variable.Double(DSim.Node(dsim_entity,"hardware/pilot/cyclic/longitudinal/trim/position"))
hardware_pilot_pedals_position = DSim.Variable.Double(DSim.Node(dsim_entity,"hardware/pilot/pedals/position"))
hardware_pilot_pedals_trim_position = DSim.Variable.Double(DSim.Node(dsim_entity,"hardware/pilot/pedals/trim/position"))



LOWL = [48.23386,14.20719]
RW_26 = np.deg2rad(260)

reference_frame_inertial_position_altitude.write(295)
reference_frame_body_freestream_airspeed.write(0)
reference_frame_inertial_position_v_xy.write(0)


simulation_mode.write(SIM_MODE.TRIM)
time.sleep(2)
simulation_mode.write(SIM_MODE.RUN) 
time.sleep(3)
#simulation_mode.write(SIM_MODE.PAUSE) 
hardware_pilot_cyclic_lateral_trim_position.write(0)
hardware_pilot_cyclic_longitudinal_trim_position.write(0)
reference_frame_inertial_position_latitude.write(LOWL[0])
reference_frame_inertial_position_longitude.write(LOWL[1])
reference_frame_inertial_attitude_psi.write(RW_26)
time.sleep(5)

reference_frame_inertial_attitude_psi.write(RW_26)
cyclic_lat_init = hardware_pilot_cyclic_lateral_position.read()
cyclic_long_init = hardware_pilot_cyclic_longitudinal_position.read()
pedals_init = hardware_pilot_pedals_position.read()

pedals = pedals_init
cyclic_lat = cyclic_lat_init
cyclic_long = cyclic_long_init



print("Ready")


# =============================================================================
# #Transport delay  test fuer HMD
# while True:
# 
# # =============================================================================
# #     if cyclic_lat > abs(cyclic_lat_init) + 0.005: 
# #         reference_frame_inertial_attitude_phi.write(np.deg2rad(20))
# #         time.sleep(0.3)
# #         simulation_mode.write(SIM_MODE.PAUSE) 
# #     cyclic_lat = hardware_pilot_cyclic_lateral_position.read()
# # =============================================================================
#     
# # =============================================================================
# #     if cyclic_long > abs(cyclic_long_init) + 0.005: 
# #         reference_frame_inertial_attitude_theta.write(np.deg2rad(20))
# #         time.sleep(0.3)
# #         simulation_mode.write(SIM_MODE.PAUSE) 
# #     cyclic_long = hardware_pilot_cyclic_longitudinal_position.read()
# # =============================================================================
#     
# 
# 
#     if pedals > abs(pedals_init) + 0.0005: 
#         reference_frame_inertial_attitude_psi.write(np.deg2rad(RW_26+30))
#         time.sleep(0.3)
#         simulation_mode.write(SIM_MODE.PAUSE) 
#     pedals = hardware_pilot_pedals_position.read()
#     
# =============================================================================




#Transport delay test fuer instrumenten display
while True:

    if cyclic_lat > abs(cyclic_lat_init) + 0.0005: 
        reference_frame_inertial_attitude_phi.write(np.deg2rad(5))
        time.sleep(0.5)
        simulation_mode.write(SIM_MODE.PAUSE) 
    cyclic_lat = hardware_pilot_cyclic_lateral_position.read()
    
# =============================================================================
#     if cyclic_long > abs(cyclic_long_init) + 0.0005: 
#         reference_frame_inertial_attitude_theta.write(np.deg2rad(5))
#         time.sleep(0.5)
#         simulation_mode.write(SIM_MODE.PAUSE) 
#     cyclic_long = hardware_pilot_cyclic_longitudinal_position.read()
# =============================================================================
    


# =============================================================================
#     if pedals > abs(pedals_init) + 0.0005: 
#         reference_frame_inertial_attitude_psi.write(np.deg2rad(RW_26+5))
#         time.sleep(0.5)
#         simulation_mode.write(SIM_MODE.PAUSE) 
#         
#     pedals = hardware_pilot_pedals_position.read()
# =============================================================================
    
    
    



    
    
    
    
    
    
    
    














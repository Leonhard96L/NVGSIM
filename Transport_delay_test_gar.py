import ctypes
import enum
import sys
import time
from pathlib import Path

import numpy as np

# setup dsim -------------------------------------------------------

DSIM_ROOT = Path("D:/")

DSIM_PATHS = [
    DSIM_ROOT / "entity/multisim/dsim/sdk/python/include",
    DSIM_ROOT / "entity/multisim/simulation/sdk/python/include",
]

for path in DSIM_PATHS:
    sys.path.append(str(path))

import DSim

#-------------------------------------------------------------------

# definitions ------------------------------------------------------

ZERO = 0
LOWL_LATITUDE = 48.23386
LOWL_LONGITUDE = 14.20719
RUNWAY_26_HEADING = np.deg2rad(260)

INITIAL_ALTITUDE = 295
INITIAL_AIRSPEED = 0
INITIAL_FORWARD_SPEED = 0

class SimMode(enum.IntEnum):
    TRIM = 0
    RUN = 1
    PAUSE = 2
    REPLAY = 3

#-------------------------------------------------------------------

# define dsim controls ---------------------------------------------

# GAR could be like
#class Helicopter:
#    def __init__(self, entity):
#        self.phi = DSim.Variable.Double(
#            DSim.Node(entity, "reference_frame/inertial/attitude/phi")
#        )
#        self.theta = DSim.Variable.Double(
#            DSim.Node(entity, "reference_frame/inertial/attitude/theta")
#        )
#        self.psi = DSim.Variable.Double(
#            DSim.Node(entity, "reference_frame/inertial/attitude/psi")
#        )
#
#        self.latitude = DSim.Variable.Double(
#            DSim.Node(entity, "reference_frame/inertial/position/latitude")
#        )
#
#        self.longitude = DSim.Variable.Double(
#            DSim.Node(entity, "reference_frame/inertial/position/longitude")
#        )
#
#        self.altitude = DSim.Variable.Double(
#            DSim.Node(entity, "reference_frame/inertial/position/altitude")
#        )

#       def set_roll_deg(self, degrees):
#          """Set helicopter roll angle in degrees."""
#           self.roll.write(np.deg2rad(degrees))
#
# ...
#
#heli = Helicopter(dsim_entity)
#heli.phi.write(np.deg2rad(10))

# GAR is this needed?
# GAR do winmm.timeEndPeriod(1)
# GAR time.perf_counter() instead of sleep?
# get more accurate timer (using windows multimedia dll)
winmm = ctypes.WinDLL('winmm')
winmm.timeBeginPeriod(1)

# GAR are those needed?
# dsim_host = DSim.Entity("sim1")
dsim_entity = DSim.Entity("ec135_1")
# dworld_entity = DSim.Entity("world")

simulation_mode = DSim.Variable.Enum(DSim.Node(dsim_entity, "SIMULATION/mode"))

phi = DSim.Variable.Double(DSim.Node(dsim_entity, "reference_frame/inertial/attitude/phi"))
theta = DSim.Variable.Double(DSim.Node(dsim_entity, "reference_frame/inertial/attitude/theta"))
psi = DSim.Variable.Double(DSim.Node(dsim_entity, "reference_frame/inertial/attitude/psi"))
latitude = DSim.Variable.Double(DSim.Node(dsim_entity, "reference_frame/inertial/position/latitude"))
longitude = DSim.Variable.Double(DSim.Node(dsim_entity, "reference_frame/inertial/position/longitude"))
altitude = DSim.Variable.Double(DSim.Node(dsim_entity, "reference_frame/inertial/position/altitude"))
speed_xy = DSim.Variable.Double(DSim.Node(dsim_entity, "reference_frame/inertial/position/v_xy")) #Forward speed
airspeed_x = DSim.Variable.Double(DSim.Node(dsim_entity, "reference_frame/body/freestream/v_x"))

# GAR are those needed?
# hardware_pilot_collective_position = DSim.Variable.Double(DSim.Node(dsim_entity,"hardware/pilot/collective/position"))
# hardware_pilot_collective_trim_position = DSim.Variable.Double(DSim.Node(dsim_entity,"hardware/pilot/collective/trim/position"))
cyclic_lateral = DSim.Variable.Double(DSim.Node(dsim_entity, "hardware/pilot/cyclic/lateral/position"))
cyclic_lateral_trim = DSim.Variable.Double(DSim.Node(dsim_entity, "hardware/pilot/cyclic/lateral/trim/position"))
cyclic_longitudinal = DSim.Variable.Double(DSim.Node(dsim_entity, "hardware/pilot/cyclic/longitudinal/position"))
cyclic_longitudinal_trim = DSim.Variable.Double(DSim.Node(dsim_entity, "hardware/pilot/cyclic/longitudinal/trim/position"))
pedals = DSim.Variable.Double(DSim.Node(dsim_entity,"hardware/pilot/pedals/position"))
# GAR is this needed
# hardware_pilot_pedals_trim_position = DSim.Variable.Double(DSim.Node(dsim_entity,"hardware/pilot/pedals/trim/position"))

#-------------------------------------------------------------------

# init  ------------------------------------------------------------

altitude.write(INITIAL_ALTITUDE)
airspeed_x.write(INITIAL_AIRSPEED)
speed_xy.write(INITIAL_FORWARD_SPEED)

simulation_mode.write(SimMode.TRIM)
time.sleep(2)
simulation_mode.write(SimMode.RUN)
time.sleep(3)
#simulation_mode.write(SIM_MODE.PAUSE)
cyclic_lateral_trim.write(ZERO)
cyclic_longitudinal_trim.write(ZERO)
latitude.write(LOWL_LATITUDE)
longitude.write(LOWL_LONGITUDE)
psi.write(RUNWAY_26_HEADING)
time.sleep(5)

# GAR why set twice?
psi.write(RUNWAY_26_HEADING)
cyclic_latitude_init = cyclic_lateral.read()
cyclic_longitude_init = cyclic_longitudinal.read()
pedals_init = pedals.read()

pedals = pedals_init
cyclic_lat = cyclic_latitude_init
cyclic_long = cyclic_longitude_init

#-------------------------------------------------------------------

print("Ready")

# start test  ------------------------------------------------------

# Notes GAR

# error in threshold?
# use smth like
# if abs(cyclic_lat - cyclic_lat_init) > 0.0005:

# dont print in loops

# use time.sleep(0.01) for timing control on value.read()

# cleanup like
#try:
#    while True:
#        ...
#except KeyboardInterrupt:
#    print("Test stopped by user.")
#finally:
#    winmm.timeEndPeriod(1)
#    simulation_mode.write(SIM_MODE.PAUSE)

# structure like
#def main():
#    initialize_simulation()
#    initialize_test()
#    run_lateral_cyclic_test()
#    shutdown()

#if __name__ == "__main__":
#    main()

#-------------------------------------------------------------------
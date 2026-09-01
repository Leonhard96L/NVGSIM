# imports ----------------------------------------------------------

import ctypes
import enum
import sys
import time
from pathlib import Path

import numpy as np

# setup DSim -------------------------------------------------------

DSIM_ROOT = Path("D:/")

DSIM_PATHS = [
    DSIM_ROOT / "entity/multisim/dsim/sdk/python/include",
    DSIM_ROOT / "entity/multisim/simulation/sdk/python/include",
]

for path in DSIM_PATHS:
    sys.path.append(str(path))

import DSim

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

# init DSim variables ----------------------------------------------

dsim_entity = DSim.Entity("ec135_1")

simulation_mode = DSim.Variable.Enum(DSim.Node(dsim_entity, "SIMULATION/mode"))

# aircraft
phi = DSim.Variable.Double(DSim.Node(dsim_entity, "reference_frame/inertial/attitude/phi"))
theta = DSim.Variable.Double(DSim.Node(dsim_entity, "reference_frame/inertial/attitude/theta"))
psi = DSim.Variable.Double(DSim.Node(dsim_entity, "reference_frame/inertial/attitude/psi"))
latitude = DSim.Variable.Double(DSim.Node(dsim_entity, "reference_frame/inertial/position/latitude"))
longitude = DSim.Variable.Double(DSim.Node(dsim_entity, "reference_frame/inertial/position/longitude"))
altitude = DSim.Variable.Double(DSim.Node(dsim_entity, "reference_frame/inertial/position/altitude"))
speed_xy = DSim.Variable.Double(DSim.Node(dsim_entity, "reference_frame/inertial/position/v_xy")) #Forward speed
airspeed_x = DSim.Variable.Double(DSim.Node(dsim_entity, "reference_frame/body/freestream/v_x"))

# controls
cyclic_lateral = DSim.Variable.Double(DSim.Node(dsim_entity, "hardware/pilot/cyclic/lateral/position"))
cyclic_lateral_trim = DSim.Variable.Double(DSim.Node(dsim_entity, "hardware/pilot/cyclic/lateral/trim/position"))
cyclic_longitudinal = DSim.Variable.Double(DSim.Node(dsim_entity, "hardware/pilot/cyclic/longitudinal/position"))
cyclic_longitudinal_trim = DSim.Variable.Double(DSim.Node(dsim_entity, "hardware/pilot/cyclic/longitudinal/trim/position"))
pedals = DSim.Variable.Double(DSim.Node(dsim_entity,"hardware/pilot/pedals/position"))

def init_simulation():
    altitude.write(INITIAL_ALTITUDE)
    airspeed_x.write(INITIAL_AIRSPEED)
    speed_xy.write(INITIAL_FORWARD_SPEED)

    #GAR check sleeps here
    simulation_mode.write(SimMode.TRIM)
    time.sleep(2)

    simulation_mode.write(SimMode.RUN)
    time.sleep(3)

    cyclic_lateral_trim.write(ZERO)
    cyclic_longitudinal_trim.write(ZERO)
    latitude.write(LOWL_LATITUDE)
    longitude.write(LOWL_LONGITUDE)
    psi.write(RUNWAY_26_HEADING)

    time.sleep(5)

def test():
    print("Ready")

def main():
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1)

    try:
        init_simulation()
        test()

    except KeyboardInterrupt:
        print("\nTest stopped by user.")

    finally:
        try:
            simulation_mode.write(SimMode.PAUSE)

        finally:
            winmm.timeEndPeriod(1)

if __name__ == "__main__":
    main()
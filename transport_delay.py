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

INPUT_THRESHOLD = 0.0005
LOOP_PERIOD = 0.01

DISPLACEMENT_MAGNITUDE = np.deg2rad(20)

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

    # TODO GAR check sleeps here. is it necessary. fixed time for all sleeps
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

def run_lateral_cyclic_test():
    initial_cyclic = cyclic_lateral.read()

    print("Ready")
    print(f"Initial lateral cyclic: " f"{initial_cyclic:.6f}")

    while True:
        loop_start = time.perf_counter()

        current_cyclic = cyclic_lateral.read()

        if abs(current_cyclic - initial_cyclic) > INPUT_THRESHOLD:
            print(
                f"Cyclic movement detected: "
                f"{current_cyclic:.6f}"
            )
            # TODO GAR why write different angles. can i just use the same for every test?
            phi.write(DISPLACEMENT_MAGNITUDE)
            # TODO GAR can we do full test in pause?
            # TODO GAR should i break after first input?
            simulation_mode.write(SimMode.PAUSE)

        elapsed = time.perf_counter() - loop_start
        # fixed loop cycle time of 0.01s
        time.sleep(max(0.0, LOOP_PERIOD - elapsed))

def run_longitudinal_cyclic_test():
    initial_cyclic = cyclic_longitudinal.read()

    print("Ready")
    print(f"Initial longitudinal cyclic: " f"{initial_cyclic:.6f}")

    while True:
        loop_start = time.perf_counter()

        current_cyclic = cyclic_longitudinal.read()

        if abs(current_cyclic - initial_cyclic) > INPUT_THRESHOLD:
            print(
                f"Cyclic movement detected: "
                f"{current_cyclic:.6f}"
            )
            theta.write(DISPLACEMENT_MAGNITUDE)
            simulation_mode.write(SimMode.PAUSE)

        elapsed = time.perf_counter() - loop_start
        # fixed loop cycle time of 0.01s
        time.sleep(max(0.0, LOOP_PERIOD - elapsed))

def run_pedals_test():
    initial_cyclic = pedals.read()

    print("Ready")
    print(f"Initial pedals: " f"{initial_cyclic:.6f}")

    while True:
        loop_start = time.perf_counter()

        current_pedals = pedals.read()

        if abs(current_pedals - initial_cyclic) > INPUT_THRESHOLD:
            print(
                f"Cyclic movement detected: "
                f"{current_pedals:.6f}"
            )
            psi.write(np.deg2rad(RUNWAY_26_HEADING) + DISPLACEMENT_MAGNITUDE)
            simulation_mode.write(SimMode.PAUSE)

        elapsed = time.perf_counter() - loop_start
        # fixed loop cycle time of 0.01s
        time.sleep(max(0.0, LOOP_PERIOD - elapsed))

def main():
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1)

    try:
        init_simulation()
        run_lateral_cyclic_test()
        # run_longitudinal_cyclic_test()
        # run_pedals_test()

    except KeyboardInterrupt:
        print("\nTest stopped by user.")

    finally:
        try:
            simulation_mode.write(SimMode.PAUSE)

        finally:
            winmm.timeEndPeriod(1)

if __name__ == "__main__":
    main()
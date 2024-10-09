import copy
import numpy as np


def split_string(s):
    # Find the positions of the first and last dots
    first_dot = s.find('.')
    last_dot = s.rfind('_')

    # Split the string based on the dot positions
    test_id = s[:first_dot]
    part_id = s[first_dot + 1:last_dot]
    case_id = s[last_dot + 1:]
    return test_id, part_id, case_id


# Function to get the test and the specific test part
def get_test_test_part_test_case(tests_orig, test_id, part_id, case_id):
    tests = copy.deepcopy(tests_orig)
    # Find the test with the given id
    test = next((test for test in tests if test['id'] == test_id), None)

    if test:
        # Find the test part with the given id within the found test
        test_part = next((part for part in test.get('test_parts', []) if part['id'] == part_id), None)

        if test_part:
            # Find the test case with the given id within the found test part
            test_case = next((case for case in test_part.get('test_cases', []) if case['id'] == case_id), None)

            test['test_parts'] = [test_part]    # Clean up the test_parts list within the test
            test_part['test_cases'] = [test_case]   # Clean up the test_cases list within the test_part

            return test, test_part, test_case

    return None, None, None


#def map_control(x): return round(50 * (x + 1), 2)  



def map_control(x,axis): # Brunner2Moog
    if axis == 'pitch':
        min_val = -0.95
        max_val = 1
    elif axis == 'roll':
        min_val = -1
        max_val = 1
    elif axis == 'pedal':
        min_val = -1
        max_val = 1
    elif axis == 'collective':
        min_val = 0.02
        max_val = 1

    return round((x - min_val) / (max_val - min_val) * 100,2)
    



def inv_map_control(x, axis):  # Moog2Brunner
    if axis == 'pitch':
        min_val = -0.95
        max_val = 1
    elif axis == 'roll':
        min_val = -1
        max_val = 1
    elif axis == 'pedal':
        min_val = -1
        max_val = 1
    elif axis == 'collective':
        min_val = 0.018
        max_val = 1

    return round(min_val + (x / 100) * (max_val - min_val),2) 


def rpm2perc(x): return round((np.rad2deg(x) / 1590) * 100, 2)


def perc2rpm(x): return round(((np.deg2rad(x) / 100) * 1590), 2)


def m2ft(x): return x * 3.281


def ft2m(x): return x * (1 / 3.281)


def mps2fpm(x): return x * 196.9


def fpm2mps(x): return x * (1 / 196.9)


def mps2kt(x): return x * 1.944


def kt2mps(x): return x * (1 / 1.944)


def map360(x): return round(np.rad2deg(x),2)%360


def pitch_brun2angle(x):
    # Factors for the control angles
    pitchP_factor_pos = 12.5
    pitchP_factor_neg = 12.3
    x = x * pitchP_factor_pos if x > 0 else x * pitchP_factor_neg
    # x[x>0] *= pitchP_factor_pos
    # x[x<0] *= pitchP_factor_neg
    return x


def roll_brun2angle(x):
    # Factors for the control angles
    rollP_factor_pos = 10.2
    rollP_factor_neg = 10.1
    x = x * rollP_factor_pos if x > 0 else x * rollP_factor_neg
    # x[x>0] *= rollP_factor_pos
    # x[x<0] *= rollP_factor_neg
    return x


def yaw_brun2angle(x):
    yawP_factor_pos = 17.5
    yawP_factor_neg = 21.7
    x = x * yawP_factor_pos if x > 0 else x * yawP_factor_neg
    # x[x>0] *= yawP_factor_pos
    # x[x<0] *= yawP_factor_neg
    return x


def coll_brun2angle(x):
    collP_factor_pos = 28
    x = x * collP_factor_pos
    # x[x>0] *= collP_factor_pos
    return x


def pitch_brun2N(x):
    # Cyclic: Abstand Griff zu Drehpunkt_Longitudinal
    L_P = -0.7124
    x = x * 100 / L_P
    return x


def roll_brun2N(x):
    # Cyclic: Abstand Griff zu Drehpunkt_Lateral_Longitudinal
    L_R = 0.7806
    x = x * 100 / L_R
    return x


def coll_brun2N(x):
    # Collective: Abstand Griff zu Drehpunkt
    #LC = 0.61 Old
    LC = 0.5159
    x = x * 100 / LC
    return x


def ATRIM_calc(x, y):
    x = np.array(x)
    x = x[::60]
    y = np.array(y)
    y = y[::60]
    rate = np.diff(y) / np.diff(x)
    return rate, x[:-1]


# Gross Weight
# Linear interpolation of GW:
# EC135T2+ min. GW = 1700kg max.GW = 2980kg
# AS532 min. GW = 4500kg max.GW = 8600kg
def GW_map(x):
    return 4500 + (4100 / 1280) * (float(x) - 1700)


# CG_Long
# Linear interpolation of CG_x:
# EC135T2+ max.AFT = 4541mm max.FWD=4121mm
# AS532 max.AFT = -4.97m max.FWD=-4.47m
def CG_x_map(x):
    return -4.97 + (0.5 / -0.42) * (x - 4.541)


def units_conversion(init_cond_dict, unit):
    m2ft = 3.281
    ft2m = 1 / m2ft
    mps2fpm = 196.9
    fpm2mps = 1 / mps2fpm
    mps2kt = 1.944
    kt2mps = 1 / mps2kt
    m2mm = 1e3
    mm2m = 1 / m2mm

    if unit == 'SI':
        init_cond_dict_SI = init_cond_dict
        init_cond_dict_SI['Gross Weight'] = round(float(init_cond_dict['Gross Weight']), 2)
        init_cond_dict_SI['CG Longitudinal'] = round(float(init_cond_dict['CG Longitudinal']) * mm2m, 2)
        init_cond_dict_SI['CG Lateral'] = round(float(init_cond_dict['CG Lateral']) * mm2m, 2)
        init_cond_dict_SI['Pressure Altitude'] = round(float(init_cond_dict['Pressure Altitude']) * ft2m, 2)
        init_cond_dict_SI['Wind Direction'] = round(np.deg2rad(float(init_cond_dict['Wind Direction'])), 2)
        init_cond_dict_SI['Wind Speed'] = round(float(init_cond_dict['Wind Speed']) * kt2mps, 2)
        init_cond_dict_SI['Airspeed'] = round(float(init_cond_dict['Airspeed']) * kt2mps, 2)
        init_cond_dict_SI['Ground Speed'] = round(float(init_cond_dict['Ground Speed']) * kt2mps, 2)
        init_cond_dict_SI['Vertical Velocity'] = round(float(init_cond_dict['Vertical Velocity']) * fpm2mps, 2)
        if init_cond_dict['Radar Altitude'] == 'N/A':
            init_cond_dict_SI['Radar Altitude'] = 'N/A'
        else:
            init_cond_dict_SI['Radar Altitude'] = round(float(init_cond_dict['Radar Altitude']) * ft2m, 2)
        init_cond_dict_SI['Rotor Speed'] = perc2rpm(float(init_cond_dict['Rotor Speed']))
        init_cond_dict_SI['Engine 1 Torque'] = round(float(init_cond_dict['Engine 1 Torque']), 2)
        init_cond_dict_SI['Engine 2 Torque'] = round(float(init_cond_dict['Engine 2 Torque']), 2)
        init_cond_dict_SI['Pitch Angle'] = round(np.deg2rad(float(init_cond_dict['Pitch Angle'])), 2)
        init_cond_dict_SI['Bank Angle'] = round(np.deg2rad(float(init_cond_dict['Bank Angle'])), 2)
        init_cond_dict_SI['Heading'] = round(np.deg2rad(float(init_cond_dict['Heading'])), 2)
        init_cond_dict_SI['Pitch Rate'] = round(np.deg2rad(float(init_cond_dict['Pitch Rate'])), 2)
        init_cond_dict_SI['Roll Rate'] = round(np.deg2rad(float(init_cond_dict['Roll Rate'])), 2)
        init_cond_dict_SI['Yaw Rate'] = round(np.deg2rad(float(init_cond_dict['Yaw Rate'])), 2)
        init_cond_dict_SI['Longitudinal Cyclic Pos.'] = inv_map_control(
            float(init_cond_dict['Longitudinal Cyclic Pos.']), 'pitch')
        init_cond_dict_SI['Lateral Cyclic Pos.'] = inv_map_control(float(init_cond_dict['Lateral Cyclic Pos.']), 'roll')
        init_cond_dict_SI['Pedals Pos.'] = inv_map_control(float(init_cond_dict['Pedals Pos.']), 'pedal')
        init_cond_dict_SI['Collective Pos.'] = inv_map_control(float(init_cond_dict['Collective Pos.']), 'collective')
        return init_cond_dict_SI

    elif unit == 'Avi':
        init_cond_dict_Avi = init_cond_dict
        init_cond_dict_Avi['Gross Weight'] = round(float(init_cond_dict['Gross Weight']), 2)
        init_cond_dict_Avi['CG Longitudinal'] = round(float(init_cond_dict['CG Longitudinal']) * m2mm, 2)
        init_cond_dict_Avi['CG Lateral'] = round(float(init_cond_dict['CG Lateral']) * m2mm, 1)
        init_cond_dict_Avi['Pressure Altitude'] = round(float(init_cond_dict['Pressure Altitude']) * m2ft, 2)
        init_cond_dict_Avi['Wind Direction'] = round(np.rad2deg(float(init_cond_dict['Wind Direction'])), 2)
        init_cond_dict_Avi['Wind Speed'] = round(float(init_cond_dict['Wind Speed']) * mps2kt, 2)
        init_cond_dict_Avi['Airspeed'] = round(float(init_cond_dict['Airspeed']) * mps2kt, 2)
        init_cond_dict_Avi['Ground Speed'] = round(float(init_cond_dict['Ground Speed']) * mps2kt, 2)
        init_cond_dict_Avi['Vertical Velocity'] = round(-float(init_cond_dict['Vertical Velocity']) * mps2fpm, 2)
        init_cond_dict_Avi['Radar Altitude'] = round(float(init_cond_dict['Radar Altitude']), 2)
        init_cond_dict_Avi['Rotor Speed'] = rpm2perc(float(init_cond_dict['Rotor Speed']))
        init_cond_dict_Avi['Engine 1 Torque'] = round(float(init_cond_dict['Engine 1 Torque']), 2)
        init_cond_dict_Avi['Engine 2 Torque'] = round(float(init_cond_dict['Engine 2 Torque']), 2)
        init_cond_dict_Avi['Pitch Angle'] = round(np.rad2deg(float(init_cond_dict['Pitch Angle'])), 2)
        init_cond_dict_Avi['Bank Angle'] = round(np.rad2deg(float(init_cond_dict['Bank Angle'])), 2)
        init_cond_dict_Avi['Heading'] = map360(float(init_cond_dict['Heading']))
        init_cond_dict_Avi['Pitch Rate'] = round(np.rad2deg(float(init_cond_dict['Pitch Rate'])), 2)
        init_cond_dict_Avi['Roll Rate'] = round(np.rad2deg(float(init_cond_dict['Roll Rate'])), 2)
        init_cond_dict_Avi['Yaw Rate'] = round(np.rad2deg(float(init_cond_dict['Yaw Rate'])), 2)
        init_cond_dict_Avi['Longitudinal Cyclic Pos.'] = map_control(float(init_cond_dict['Longitudinal Cyclic Pos.']), 'pitch')
        init_cond_dict_Avi['Lateral Cyclic Pos.'] = map_control(float(init_cond_dict['Lateral Cyclic Pos.']), 'roll')
        init_cond_dict_Avi['Pedals Pos.'] = map_control(float(init_cond_dict['Pedals Pos.']), 'pedal')
        init_cond_dict_Avi['Collective Pos.'] = map_control(float(init_cond_dict['Collective Pos.']), 'collective')
        return init_cond_dict_Avi


# automatic_data_template = {
#     'tests': [
#         {
#             'id': '1',
#             'name': 'Performance',
#             'test_parts': [
#                 {
#                     'id': 'a.3',
#                     'main_title': 'Engine Assessment',
#                     'test_title': 'Engine & Rotor Speed Governing',
#                     'objective': 'The objective of this test is to demonstrate that the FSTD engine and rotor speed governing is compliant with the reference data.',
#                     'tolerances_evaluation_criteria': [
#                         {'parameter': 'Engine 1 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Engine 2 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Rotor Speed', 'unit': '[%]', 'tolerance': 'CT&M'}
#                     ],
#                     'test_cases': [
#                         {
#                             'id': 'A1',
#                             'name': 'Engine rotor & speed governing',
#                             'condition': '90 KIAS, -1000 fpm, up input',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(,‘manu’).Click RUN or press F5.',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.',
#                                 'When the test elapsed time is 3.4 seconds, apply a 30.0% Torque per engine increase in 4.0 seconds.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B1',
#                             'name': 'Engine rotor & speed governing',
#                             'condition': '60 KIAS, AEO MCP, down input',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.',
#                                 'When the test elapsed time is 3.6 seconds, apply a 40.0% Torque per engine decrease in 3.0 seconds.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         }
#                     ]
#                 },
#                 {
#                     'id': 'c.1',
#                     'main_title': 'Take-Off',
#                     'test_title': 'Take-off All engines',
#                     'objective': 'The objective of this test is to demonstrate that the FSTD all engines take-off is compliant with the reference data.',
#                     'tolerances_evaluation_criteria': [
#                         {'parameter': 'Airspeed', 'unit': '[kts]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Radar Altitude', 'unit': '[ft]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Engine 1 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Engine 2 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Rotor Speed', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Pitch Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Bank Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Heading', 'unit': '[deg]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Collective Pos.', 'unit': '[%]', 'tolerance': 'CT&M'}
#                     ],
#                     'test_cases': [
#                         {
#                             'id': 'A1',
#                             'name': 'Take-off All engines',
#                             'condition': 'CAT A',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Hover in 6ft AGL',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.',
#                                 'After 4s start to take-off. '
#                                 'Noch zu schreieben...'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         }
#                     ]
#                 },
#                 {
#                     'id': 'c.2',
#                     'main_title': 'Take-Off',
#                     'test_title': 'OEI continued take-off',
#                     'objective': 'The objective of this test is to demonstrate that the FSTD one engine inoperative continued take-off is compliant with the reference data.',
#                     'tolerances_evaluation_criteria': [
#                         {'parameter': 'Airspeed', 'unit': '[kts]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Radar Altitude', 'unit': '[ft]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Engine 1 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Engine 2 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Rotor Speed', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Pitch Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Bank Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Heading', 'unit': '[deg]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Collective Pos.', 'unit': '[%]', 'tolerance': 'CT&M'}
#                     ],
#                     'test_cases': [
#                         {
#                             'id': 'A1',
#                             'name': 'OEI continued take-off',
#                             'condition': 'OEI',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.',
#                                 'Noch zu schreieben...'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         }
#                     ]
#                 },
#                 {
#                     'id': 'd',
#                     'main_title': 'Hover Performance',
#                     'test_title': '',
#                     'objective': 'The objective of this test is to demonstrate that the FSTD hover performance is compliant with the reference data.',
#                     'tolerances_evaluation_criteria': [
#                         {'parameter': 'Engine 1 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Engine 2 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Pitch Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Bank Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Collective Pos.', 'unit': '[%]', 'tolerance': 'CT&M'}
#                     ],
#                     'test_cases': [
#                         {
#                             'id': 'A1',
#                             'name': 'Hover Performance',
#                             'condition': 'Light GW, Aft CG, 3ft AGL',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Pull Collective until hovering in 3ft AGL'
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.',
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'A2',
#                             'name': 'Hover Performance',
#                             'condition': 'Light GW, Aft CG, 10ft AGL',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Pull Collective until hovering in 10ft AGL'
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.',
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'A3',
#                             'name': 'Hover Performance',
#                             'condition': 'Light GW, Aft CG, 25ft AGL',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Pull Collective until hovering in 25ft AGL'
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.',
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'A4',
#                             'name': 'Hover Performance',
#                             'condition': 'Light GW, Aft CG, 70ft AGL',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Pull Collective until hovering in 70ft AGL'
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.',
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B1',
#                             'name': 'Hover Performance',
#                             'condition': 'Heavy GW, Forward CG, 3ft AGL',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Pull Collective until hovering in 3ft AGL'
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.',
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B2',
#                             'name': 'Hover Performance',
#                             'condition': 'Heavy GW, Forward CG, 10ft AGL',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Pull Collective until hovering in 10ft AGL'
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.',
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B3',
#                             'name': 'Hover Performance',
#                             'condition': 'Heavy GW, Forward CG, 25ft AGL',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Pull Collective until hovering in 25ft AGL'
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.',
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B4',
#                             'name': 'Hover Performance',
#                             'condition': 'Heavy GW, Forward CG, 70ft AGL',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Pull Collective until hovering in 70ft AGL'
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.',
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         }
#                     ]
#                 },
#                 {
#                     'id': 'e',
#                     'main_title': 'Vertical Climb Performance',
#                     'test_title': 'Vertical Climb Performance',
#                     'objective': 'The objective of this test is to demonstrate that the FSTD vertical climb performance is compliant with the reference data.',
#                     'tolerances_evaluation_criteria': [
#                         {'parameter': 'Vertical Velocity', 'unit': '[ft/min]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Collective Pos.', 'unit': '[%]', 'tolerance': 'CT&M'}
#                     ],
#                     'test_cases': [
#                         {
#                             'id': 'A1',
#                             'name': 'Vertical Climb Performance',
#                             'condition': 'Light GW, Aft CG - AEO TOP',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Pull collective until the FLI reaches TOP.',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B1',
#                             'name': 'Vertical Climb Performance',
#                             'condition': 'Heavy GW, Fwd CG - AEO MCP',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Pull collective until the FLI reaches MCP',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         }
#                     ]
#                 },
#                 {
#                     'id': 'f',
#                     'main_title': 'Level Flight Performance and Trimmed Flight Control Position',
#                     'test_title': 'Level Flight Performance and Trimmed Flight Control Position',
#                     'objective': 'The objective of this test is to demonstrate that the FSTD level flight performance is compliant with the reference data.',
#                     'tolerances_evaluation_criteria': [
#                         {'parameter': 'Engine 1 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Engine 2 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Pitch Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Sideslip Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Collective Pos.', 'unit': '[%]', 'tolerance': 'CT&M'}
#                     ],
#                     'test_cases': [
#                         {
#                             'id': 'A1',
#                             'name': 'Level Flight Performance and Trimmed Flight Control Position',
#                             'condition': 'Light GW, Aft CG - 64 KIAS',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.',
#                                 'Trim controls to reach and maintain 64 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'A2',
#                             'name': 'Level Flight Performance and Trimmed Flight Control Position',
#                             'condition': 'Light GW, Aft CG - 130 KIAS',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.',
#                                 'Trim controls to reach and maintain 130 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B1',
#                             'name': 'Level Flight Performance and Trimmed Flight Control Position',
#                             'condition': 'Heavy GW, Forward CG - 64 KIAS',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.',
#                                 'Trim controls to reach and maintain 64 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B2',
#                             'name': 'Level Flight Performance and Trimmed Flight Control Position',
#                             'condition': 'Heavy GW, Forward CG - 130 KIAS',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.',
#                                 'Trim controls to reach and maintain 130 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         }
#                     ]
#                 },
#                 {
#                     'id': 'g',
#                     'main_title': 'Climb Performance and Trimmed Flight Control Position',
#                     'test_title': 'Climb Performance and Trimmed Flight Control Position',
#                     'objective': 'The objective of this test is to demonstrate that the FSTD climb performance is compliant with the reference data.',
#                     'tolerances_evaluation_criteria': [
#                         {'parameter': 'Vertical Velocity', 'unit': '[ft/min]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Pitch Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Sideslip Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Collective Pos.', 'unit': '[%]', 'tolerance': 'CT&M'}
#                     ],
#                     'test_cases': [
#                         {
#                             'id': 'A1',
#                             'name': 'Climb Performance and Trimmed Flight Control Position',
#                             'condition': 'Light GW, Aft CG - AEO MCP, 63 KIAS',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Pull collective until the FLI reaches MCP.',
#                                 'Trim controls to reach and maintain 63 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'A2',
#                             'name': 'Climb Performance and Trimmed Flight Control Position',
#                             'condition': 'Light GW, Aft CG - AEO TOP, 63 KIAS',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Pull collective until the FLI reaches TOP.',
#                                 'Trim controls to reach and maintain 63 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'A3',
#                             'name': 'Climb Performance and Trimmed Flight Control Position',
#                             'condition': 'Light GW, Aft CG - OEI MCP, 64 KIAS',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Pull collective until the FLI reaches MCP.',
#                                 'Trim controls to reach and maintain 64 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'A4',
#                             'name': 'Climb Performance and Trimmed Flight Control Position',
#                             'condition': 'Light GW, Aft CG - OEI 2 min, 38 KIAS',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Pull collective until the FLI reaches 2 min.',
#                                 'Trim controls to reach and maintain 38 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'A5',
#                             'name': 'Climb Performance and Trimmed Flight Control Position',
#                             'condition': 'Light GW, Aft CG - OEI 30s, 37 KIAS',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Pull collective until the FLI reaches 30s.',
#                                 'Trim controls to reach and maintain 37 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B1',
#                             'name': 'Climb Performance and Trimmed Flight Control Position',
#                             'condition': 'Heavy GW, Forward CG - AEO MCP, 62 KIAS',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Pull collective until the FLI reaches MCP.',
#                                 'Trim controls to reach and maintain 62 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B2',
#                             'name': 'Climb Performance and Trimmed Flight Control Position',
#                             'condition': 'Heavy GW, Forward CG - AEO TOP, 62 KIAS',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Pull collective until the FLI reaches TOP.',
#                                 'Trim controls to reach and maintain 62 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B3',
#                             'name': 'Climb Performance and Trimmed Flight Control Position',
#                             'condition': 'Heavy GW, Forward CG - OEI MCP, 65 KIAS',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Pull collective until the FLI reaches MCP.',
#                                 'Trim controls to reach and maintain 65 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B4',
#                             'name': 'Climb Performance and Trimmed Flight Control Position',
#                             'condition': 'Heavy GW, Forward CG - OEI 2 min, 35 KIAS',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Pull collective until the FLI reaches 2 min.',
#                                 'Trim controls to reach and maintain 35 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B5',
#                             'name': 'Climb Performance and Trimmed Flight Control Position',
#                             'condition': 'Heavy GW, Forward CG - OEI 30 s, 42 KIAS',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Pull collective until the FLI reaches 30s.',
#                                 'Trim controls to reach and maintain 42 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         }
#                     ]
#                 },
#                 {
#                     'id': 'h.1',
#                     'main_title': 'Descent',
#                     'test_title': 'Descent Performance and Trimmed Flight Control Position',
#                     'objective': 'The objective of this test is to demonstrate that the FSTD descent performance is compliant with the reference data.',
#                     'tolerances_evaluation_criteria': [
#                         {'parameter': 'Engine 1 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Engine 2 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Pitch Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Sideslip Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Collective Pos.', 'unit': '[%]', 'tolerance': 'CT&M'}
#                     ],
#                     'test_cases': [
#                         {
#                             'id': 'A1',
#                             'name': 'Descent Performance and Trimmed Flight Control Position',
#                             'condition': 'Light GW, Aft CG - 90 KIAS, -1000 fpm',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(,‘manu’).Click RUN or press F5.',
#                                 'Push collective until reaching 1000 fpm of descent',
#                                 'Trim controls to reach and maintain 90 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B1',
#                             'name': 'Descent Performance and Trimmed Flight Control Position',
#                             'condition': 'Heavy GW, Fwd CG - 90 KIAS, -1000 fpm',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Push collective until reaching 1000 fpm of descent',
#                                 'Trim controls to reach and maintain 90 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         }
#                     ]
#                 },
#                 {
#                     'id': 'j.1',
#                     'main_title': 'Landing',
#                     'test_title': 'Landing - All Engines',
#                     'objective': 'The objective of this test is to demonstrate that the FSTD landing performance with all engines operative is compliant with the reference data.',
#                     'tolerances_evaluation_criteria': [
#                         {'parameter': 'Airspeed', 'unit': '[kts]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Radar Altitude', 'unit': '[ft]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Engine 1 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Engine 2 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Rotor Speed', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Pitch Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Bank Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Heading', 'unit': '[deg]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Collective Pos.', 'unit': '[%]', 'tolerance': 'CT&M'}
#                     ],
#                     'test_cases': [
#                         {
#                             'id': 'A1',
#                             'name': 'Landing - All Engines',
#                             'condition': 'CAT A',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(,‘manu’).Click RUN or press F5.',
#                                 'Climb up to 316ft AGL.',
#                                 'Trim controls to reach and maintain 70 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.',
#                                 'When the test elapsed time is 1.0 seconds, decrease collective to achieve 450 ft/min of rate of descent in approximately 20.0 seconds and maintain it. In the meantime move controls to reduce airspeed by 20.0 KIAS and maintain it.',
#                                 'When the test elapsed time is 36.0 seconds, increase collective to achieve level flight condition in approximately 13.0 seconds. In the meantime move controls to reach an hover condition in 23.0 seconds and maintain it.',
#                                 'Continue the maneuver touching the ground when the test elapsed time is 59.0 seconds.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         }
#                     ]
#                 },
#                 {
#                     'id': 'j.2',
#                     'main_title': 'Landing',
#                     'test_title': 'Landing - One Engine Inoperative',
#                     'objective': 'The objective of this test is to demonstrate that the FSTD one engine inoperative landing is compliant with the reference data.',
#                     'tolerances_evaluation_criteria': [
#                         {'parameter': 'Airspeed', 'unit': '[kts]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Radar Altitude', 'unit': '[ft]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Engine 1 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Engine 2 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Rotor Speed', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Pitch Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Bank Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Heading', 'unit': '[deg]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Collective Pos.', 'unit': '[%]', 'tolerance': 'CT&M'}
#                     ],
#                     'test_cases': [
#                         {
#                             'id': 'A1',
#                             'name': 'Landing - One Engine Inoperative',
#                             'condition': 'OEI - CAT A',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(,‘manu’).Click RUN or press F5.',
#                                 'Climb up to 305ft AGL.',
#                                 'Trim controls to reach and maintain 68 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.',
#                                 'Maintain pitch attitude to 5.0 deg nose up to reach 40 KIAS in 42.0 seconds, while maintaining a 300 ft/min rate of descent.',
#                                 'When the test elapsed time is 42.0 seconds, maintain 40 KIAS and continue the descent.',
#                                 'When the test elapsed time is 48.0 seconds, decrease the airspeed to 20.0 KIAS in 11.0 seconds and continue the descent.',
#                                 'When the test elapsed time is 52.0 seconds, Instructor press the Engine 1 Fail button on the IOS, continuing descent and increase pitch in order to reach an attitude of 16.0 deg in 10.0 seconds.',
#                                 'Continue decreasing ground speed to reach 5.0 kts when the test elapsed time is 70.0 seconds.',
#                                 'Start to pull the collective to cushion the landing and touch the ground when the test elapsed time is 72.0 seconds.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'A2',
#                             'name': 'Landing - One Engine Inoperative',
#                             'condition': 'OEI - CAT B',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(,‘manu’).Click RUN or press F5.',
#                                 'Climb up to 270ft AGL.',
#                                 'Trim controls to reach and maintain 77 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.',
#                                 'Increase pitch attitude to 6.0 deg nose up to reach 40 KIAS in 34.0 seconds, while maintaining a 300 ft/min rate of descent.',
#                                 'When the test elapsed time is 34.0 seconds, maintain 40 KIAS and continue the descent.',
#                                 'When the test elapsed time is 40.0 seconds, decrease the airspeed to 20.0 KIAS in 10.0 seconds and continue the descent.',
#                                 'When the test elapsed time is 47.0 seconds, increase pitch in order to reach an attitude of 13.0 deg in 8.0 seconds.',
#                                 'Continue decreasing ground speed to reach 5.0 kts when the test elapsed time is 60.0 seconds.',
#                                 'Start to pull the collective to cushion the landing and touch the ground when the test elapsed time is 74.0 seconds.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         }
#                     ]
#                 }
#             ]
#         },
#         {
#             'id': '2',
#             'name': 'Handling Qualities',
#             'test_parts': [
#                 {
#                     'id': 'a.1',
#                     'main_title': 'Control System Mechanical Characteristics',
#                     'test_title': 'Cyclic Force vs Position',
#                     'objective': 'The objective of this test is to demonstrate that the FSTD Cyclic Control System Mechanical Characteristics are compliant with the reference data.',
#                     'tolerances_evaluation_criteria': [
#                         {'parameter': 'Breakout', 'unit': '[daN]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Force', 'unit': '[daN]', 'tolerance': 'CT&M'}
#                     ],
#                     'test_cases': [
#                         {
#                             'id': 'A1',
#                             'name': 'Cyclic Force vs Position',
#                             'condition': 'Longitudinal cyclic - Trim ON',
#                             'automatic_testing_possible': False,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(,‘manu’).Click RUN or press F5.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.',
#                                 'Move the Cyclic stick to perform a complete sweep on the longitudinal axis.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'A2',
#                             'name': 'Cyclic Force vs Position',
#                             'condition': 'Longitudinal cyclic - Trim OFF',
#                             'automatic_testing_possible': False,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.',
#                                 'Move the Cyclic stick to perform a complete sweep on the longitudinal axis while pressing the FTR Release button.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B1',
#                             'name': 'Cyclic Force vs Position',
#                             'condition': 'Lateral cyclic - Trim ON',
#                             'automatic_testing_possible': False,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.',
#                                 'Move the Cyclic stick to perform a complete sweep on the lateral axis.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B2',
#                             'name': 'Cyclic Force vs Position',
#                             'condition': 'Lateral cyclic - Trim OFF',
#                             'automatic_testing_possible': False,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.',
#                                 'Move the Cyclic stick to perform a complete sweep on the lateral axis while pressing the FTR Release button.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         }
#                     ]
#                 },
#                 {
#                     'id': 'a.2',
#                     'main_title': 'Control System Mechanical Characteristics',
#                     'test_title': 'Collective/Pedals Force vs Position',
#                     'objective': 'The objective of this test is to demonstrate that the FSTD Collective/Pedals Control System Mechanical Characteristics are compliant with the reference data.',
#                     'tolerances_evaluation_criteria': [
#                         {'parameter': 'Breakout', 'unit': '[daN]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Force', 'unit': '[daN]', 'tolerance': 'CT&M'}
#                     ],
#                     'test_cases': [
#                         {
#                             'id': 'A1',
#                             'name': 'Collective/Pedals Force vs Position',
#                             'condition': 'Collective - Trim ON',
#                             'automatic_testing_possible': False,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(,‘manu’).Click RUN or press F5.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.',
#                                 'Move the Collective lever to perform a complete sweep.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B1',
#                             'name': 'Collective/Pedals Force vs Position',
#                             'condition': 'Pedals - Trim ON',
#                             'automatic_testing_possible': False,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.',
#                                 'Move the Pedals to perform a complete sweep.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         }
#                     ]
#                 },
#                 {
#                     'id': 'a.4',
#                     'main_title': 'Control System Mechanical Characteristics',
#                     'test_title': 'Trim System Rate',
#                     'objective': 'The objective of this test is to demonstrate that the FSTD Trim System Rate Characteristics are compliant with the reference data.',
#                     'tolerances_evaluation_criteria': [
#                         {'parameter': 'Trim Rate', 'unit': '[%]', 'tolerance': 'CT&M'}
#                     ],
#                     'test_cases': [
#                         {
#                             'id': 'A1',
#                             'name': 'Longitudinal Cyclic',
#                             'condition': 'Longitudinal Cyclic - ATRIM',
#                             'automatic_testing_possible': False,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(,‘manu’).Click RUN or press F5.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.',
#                                 'Press the Beep-Trim to move the Cyclic stick in the full aft position on the longitudinal axis.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B1',
#                             'name': 'Lateral Cyclic',
#                             'condition': 'Lateral Cyclic - ATRIM',
#                             'automatic_testing_possible': False,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.',
#                                 'Press the Beep-Trim to move the Cyclic stick in the full right position on the lateral axis.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         }
#                     ]
#                 },
#                 {
#                     'id': 'c.2',
#                     'main_title': 'Longitudinal Handling Qualities',
#                     'test_title': 'Longitudinal Static Stability',
#                     'objective': 'The objective of this test is to demonstrate that the FSTD longitudinal static stability is compliant with the reference data.',
#                     'tolerances_evaluation_criteria': [
#                         {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'}
#                     ],
#                     'test_cases': [
#                         {
#                             'id': 'A1',
#                             'name': 'Longitudinal Static Stability',
#                             'condition': 'Cruise, Trim Speed UP - 120 KIAS, Trim Speed',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Trim controls to reach and maintain 119 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'A2',
#                             'name': 'Longitudinal Static Stability',
#                             'condition': 'Cruise, Trim Speed UP - 125 KIAS',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Trim controls to reach and maintain 124 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'A3',
#                             'name': 'Longitudinal Static Stability',
#                             'condition': 'Cruise, Trim Speed UP - 130 KIAS',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Trim controls to reach and maintain 129 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B1',
#                             'name': 'Longitudinal Static Stability',
#                             'condition': 'Cruise, Trim Speed DOWN - 120 KIAS, Trim Speed',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Trim controls to reach and maintain 120 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B2',
#                             'name': 'Longitudinal Static Stability',
#                             'condition': 'Cruise, Trim Speed DOWN - 115 KIAS',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Trim controls to reach and maintain 115 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B3',
#                             'name': 'Longitudinal Static Stability',
#                             'condition': 'Cruise, Trim Speed DOWN - 110 KIAS',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Trim controls to reach and maintain 107 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'C1',
#                             'name': 'Longitudinal Static Stability',
#                             'condition': 'Autorotation, Trim Speed UP - 75 KIAS, Trim Speed',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Trim controls to reach and maintain 74 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'C2',
#                             'name': 'Longitudinal Static Stability',
#                             'condition': 'Autorotation, Trim Speed UP - 85 KIAS',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Trim controls to reach and maintain 84 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'C3',
#                             'name': 'Longitudinal Static Stability',
#                             'condition': 'Autorotation, Trim Speed UP - 90 KIAS',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Trim controls to reach and maintain 88 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'D1',
#                             'name': 'Longitudinal Static Stability',
#                             'condition': 'Autorotation, Trim Speed DOWN - 75 KIAS, Trim Speed',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Trim controls to reach and maintain 75 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'D2',
#                             'name': 'Longitudinal Static Stability',
#                             'condition': 'Autorotation, Trim Speed DOWN - 65 KIAS',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Trim controls to reach and maintain 65 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'D3',
#                             'name': 'Longitudinal Static Stability',
#                             'condition': 'Autorotation, Trim Speed DOWN - 55 KIAS',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Trim controls to reach and maintain 55 KIAS',
#                                 'Stabilize and maintain current flight condition.',
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         }
#                     ]
#                 },
#                 {
#                     'id': 'c.4',
#                     'main_title': 'Longitudinal Handling Qualities',
#                     'test_title': 'Manoeuvring Stability',
#                     'objective': 'The objective of this test is to demonstrate that the FSTD longitudinal manoeuvring stability is compliant with the reference data.',
#                     'tolerances_evaluation_criteria': [
#                         {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'}
#                     ],
#                     'test_cases': [
#                         {
#                             'id': 'A1',
#                             'name': 'Manoeuvring Stability',
#                             'condition': 'Right Turn, Mid Speed - 65 KIAS, 0 Bank',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.'
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'A2',
#                             'name': 'Manoeuvring Stability',
#                             'condition': 'Right Turn, Mid Speed - 65 KIAS, 30 Bank',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.'
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'A3',
#                             'name': 'Manoeuvring Stability',
#                             'condition': 'Right Turn, Mid Speed - 65 KIAS, 45 Bank',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.'
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B1',
#                             'name': 'Manoeuvring Stability',
#                             'condition': 'Left Turn, Mid Speed - 66 KIAS, 0 Bank',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.'
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B2',
#                             'name': 'Manoeuvring Stability',
#                             'condition': 'Left Turn, Mid Speed - 65 KIAS, 30 Bank',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.'
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B3',
#                             'name': 'Manoeuvring Stability',
#                             'condition': 'Left Turn, Mid Speed - 66 KIAS, 45 Bank',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.'
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'C1',
#                             'name': 'Manoeuvring Stability',
#                             'condition': 'Right Turn, High Speed - 120 KIAS, 0 Bank',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.'
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'C2',
#                             'name': 'Manoeuvring Stability',
#                             'condition': 'Right Turn, High Speed - 120 KIAS, 30 Bank',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.'
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'C3',
#                             'name': 'Manoeuvring Stability',
#                             'condition': 'Right Turn, High Speed - 120 KIAS, 45 Bank',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.'
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'D1',
#                             'name': 'Manoeuvring Stability',
#                             'condition': 'Left Turn, High Speed - 120 KIAS, 0 Bank',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.'
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'D2',
#                             'name': 'Manoeuvring Stability',
#                             'condition': 'Left Turn, High Speed - 120 KIAS, 30 Bank',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.'
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'D3',
#                             'name': 'Manoeuvring Stability',
#                             'condition': 'Left Turn, High Speed - 120 KIAS, 45 Bank',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.'
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         }
#                     ]
#                 },
#                 {
#                     'id': 'd.2',
#                     'main_title': 'Lateral & Directional Handling Qualities',
#                     'test_title': 'Directional Static Stability',
#                     'objective': 'The objective of this test is to demonstrate that the FSTD directional static stability is compliant with the reference data.',
#                     'tolerances_evaluation_criteria': [
#                         {'parameter': 'Bank Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': 'CT&M'}
#                     ],
#                     'test_cases': [
#                         {
#                             'id': 'A1',
#                             'name': 'Directional Static Stability',
#                             'condition': 'Mid Speed - 100 KIAS, Trim',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.'
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'A2',
#                             'name': 'Directional Static Stability',
#                             'condition': 'Mid Speed - 100 KIAS, Right Sideslip 1',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.'
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'A3',
#                             'name': 'Directional Static Stability',
#                             'condition': 'Mid Speed - 100 KIAS, Right Sideslip 2',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.'
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B1',
#                             'name': 'Directional Static Stability',
#                             'condition': 'Mid Speed - 100 KIAS, Trim',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.'
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B2',
#                             'name': 'Directional Static Stability',
#                             'condition': 'Mid Speed - 100 KIAS, Left Sideslip 1',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.'
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B3',
#                             'name': 'Directional Static Stability',
#                             'condition': 'Mid Speed - 100 KIAS, Left Sideslip 2',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.'
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         }
#                     ]
#                 },
#                 {
#                     'id': 'd.3.i',
#                     'main_title': 'Dynamic Lateral and Directional Stability',
#                     'test_title': 'Lateral-Directional Oscillations',
#                     'objective': 'The objective of this test is to demonstrate that the FSTD dynamic lateral-directional stability (oscillations) is compliant with the reference data.',
#                     'tolerances_evaluation_criteria': [
#                         {'parameter': 'Calculated period', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Time to 1/2 amplitude', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'or Time to Double amplitude', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'or Damping Ratio', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Time difference between peaks of Bank and Sideslip', 'unit': '[s]',
#                          'tolerance': 'CT&M'},
#                         {'parameter': 'Non-periodic response', 'unit': '[-]', 'tolerance': 'Time history'}
#                     ],
#                     'test_cases': [
#                         {
#                             'id': 'A1',
#                             'name': 'Lateral-Directional Oscillations',
#                             'condition': 'Mid Speed - 66 KIAS, Left Pedal input',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.'
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'A2',
#                             'name': 'Lateral-Directional Oscillations',
#                             'condition': 'Mid Speed - 66 KIAS, Left Pedal input',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.'
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B1',
#                             'name': 'Lateral-Directional Oscillations',
#                             'condition': 'High Speed - 90 KIAS, Left Pedal input',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.'
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B2',
#                             'name': 'Lateral-Directional Oscillations',
#                             'condition': 'High Speed - 90 KIAS, Left Pedal input',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.'
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         }
#                     ]
#                 },
#                 {
#                     'id': 'd.3.ii',
#                     'main_title': 'Dynamic Lateral and Directional Stability',
#                     'test_title': 'Spiral Stability',
#                     'objective': 'The objective of this test is to demonstrate that the FSTD spiral stability is compliant with the reference data.',
#                     'tolerances_evaluation_criteria': [
#                         {'parameter': 'Correct Trend on Bank', 'unit': '[deg]', 'tolerance': 'CT&M'}
#                     ],
#                     'test_cases': [
#                         {
#                             'id': 'A1',
#                             'name': 'Spiral Stability',
#                             'condition': 'Right Input - 64 KIAS',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.'
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'A2',
#                             'name': 'Spiral Stability',
#                             'condition': 'Right Input - 64 KIAS',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.'
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B1',
#                             'name': 'Spiral Stability',
#                             'condition': 'Left Input - 63 KIAS',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.'
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         },
#                         {
#                             'id': 'B2',
#                             'name': 'Spiral Stability',
#                             'condition': 'Left Input - 64 KIAS',
#                             'automatic_testing_possible': True,
#                             'generic_flight_controls': [
#                                 {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
#                                 {'fc': 'Lateral', 'status': 'MATH PILOT'},
#                                 {'fc': 'Collective', 'status': 'MATH PILOT'},
#                                 {'fc': 'Pedals', 'status': 'MATH PILOT'}
#                             ],
#                             'automatic_testing': [
#                                 'Write the name of the test into the brackets of the function (, ‘auto’). Click RUN or press F5.',
#                                 'The generic flight controls will be internally controlled according to the following table:'
#                             ],
#                             'manual_testing': [
#                                 'Write the name of the test into the brackets of the function(, ‘manu’).Click RUN or press F5.',
#                                 'Set controls to reach target values.'
#                                 'On the IOS keyboard press ‘Enter’ to start recording.'
#                             ],
#                             'notes_rationales': {
#                                 'notes': ['No Notes related to the Test are present'],
#                                 'rationales_validation_data': ['No Rationales related to the Test are present'],
#                                 'rationales_results': ['No Rationales related to the Test are present']
#                             }
#                         }
#                     ]
#                 }
#             ]
#         }
#     ]
# }

#             '1.a.2.A1': 'HI NR - OFF to ON',
#             '1.a.2.A2': 'HI NR - ON to OFF',
#             '1.a.3': 'Engine & Rotor Speed Governing',
#             '1.a.3.A1': '90 KIAS - Up Input, -1000 fpm',
#             '1.a.3.B1': '60 KIAS - Down Input, AEO MCP',
# ]}
#
#
#     '1.c': 'Take-Off',
#     '1.c.1': 'Take-off All engines',
#     '1.c.1.A1': 'CAT A - Clear Helipad',
#     '1.c.2': 'OEI continued take-off',
#     '1.c.2.A1': 'OEI',
#     '1.d': 'Hover Performance',
#     '1.d.A1': 'Light GW, Aft CG - 3 ft AGL',
#     '1.d.A2': 'Light GW, Aft CG - 10 ft AGL',
#     '1.d.A3': 'Light GW, Aft CG - 25 ft AGL',
#     '1.d.A4': 'Light GW, Aft CG - 70 ft AGL',
#     '1.d.B1': 'Heavy GW, Aft CG - 3 ft AGL',
#     '1.d.B2': 'Heavy GW, Aft CG - 10 ft AGL',
#     '1.d.B3': 'Heavy GW, Aft CG - 25 ft AGL',
#     '1.d.B4': 'Heavy GW, Aft CG - 70 ft AGL',
#     '1.e': 'Vertical Climb Performance',
#     '1.e.A1': 'Light GW, Aft CG - AEO TOP',
#     '1.e.B1': 'Heavy GW, Fwd CG - AEO MCP',
#     '1.f': 'Level Flight Performance and Trimmed Flight Control Position',
#     '1.f.A1': 'Light GW, Aft CG - 64 KIAS',
#     '1.f.A2': 'Light GW, Aft CG - 130 KIAS',
#     '1.f.B1': 'Heavy GW, Aft CG - 64 KIAS',
#     '1.f.B2': 'Heavy GW, Aft CG - 130 KIAS',
#     '1.g': 'Climb Performance and Trimmed Flight Control Position',
#     '1.g.A1': 'Light GW, Aft CG - AEO MCP, VY',
#     '1.g.A2': 'Light GW, Aft CG - AEO TOP, VY',
#     '1.g.A3': 'Light GW, Aft CG - OEI MCP, VY',
#     '1.g.A4': 'Light GW, Aft CG - OEI 2 min, VTOSS',
#     '1.g.A5': 'Light GW, Aft CG - OEI 30 s, VTOSS',
#     '1.g.B1': 'Heavy GW, Fwd CG - AEO MCP, VY',
#     '1.g.B2': 'Heavy GW, Fwd CG - AEO TOP, VY',
#     '1.g.B3': 'Heavy GW, Fwd CG - OEI MCP, VY',
#     '1.g.B4': 'Heavy GW, Fwd CG - OEI 2 min, VTOSS',
#     '1.g.B5': 'Heavy GW, Fwd CG - OEI 30 s, VTOSS',
#     '1.h': 'Descent',
#     '1.h.1': 'Descent Performance and Trimmed Flight Control Position',
#     '1.h.1.A1': 'Light GW, Aft CG - 90 KIAS, -1000 fpm',
#     '1.h.1.B1': 'Heavy GW, Fwd CG - 90 KIAS, -1000 fpm',
#     '1.j': 'Landing',
#     '1.j.1': 'Landing - All Engines',
#     '1.j.1.A1': 'CAT A - Clear Helipad',
#     '1.j.2': 'Landing - One Engine Inoperative',
#     '1.j.2.A1': 'OEI - CAT A Clear Helipad',
#     '1.j.2.A2': 'OEI - CAT B',
#     '2.a': 'Control System Mechanical Characteristics',
#     '2.a.1': 'Cyclic Force vs Position',
#     '2.a.1.A1': 'Longitudinal - Trim ON',
#     '2.a.1.A2': 'Longitudinal - Trim OFF',
#     '2.a.1.B1': 'Lateral - Trim ON',
#     '2.a.1.B2': 'Lateral - Trim OFF',
#     '2.a.2': 'Collective/Pedals Force vs Position',
#     '2.a.2.A1': 'Collective - Trim ON',
#     '2.a.2.B1': 'Pedals - Trim ON',
#     '2.a.4': 'Trim System Rate',
#     '2.a.4.A1': 'Longitudinal Cyclic - ATRIM',
#     '2.a.4.B1': 'Lateral Cyclic - ATRIM',
#     '2.c': 'Longitudinal Handling Qualities',
#     '2.c.2': 'Longitudinal Static Stability',
#     '2.c.2.A1': 'Cruise, Trim Speed UP - 120 KIAS, Trim Speed',
#     '2.c.2.A2': 'Cruise, Trim Speed UP - 125 KIAS',
#     '2.c.2.A3': 'Cruise, Trim Speed UP - 130 KIAS',
#     '2.c.2.B1': 'Cruise, Trim Speed DOWN - 120 KIAS, Trim Speed',
#     '2.c.2.B2': 'Cruise, Trim Speed DOWN - 115 KIAS',
#     '2.c.2.B3': 'Cruise, Trim Speed DOWN - 110 KIAS',
#     '2.c.2.C1': 'Autorotation, Trim Speed UP - 75 KIAS, Trim Speed',
#     '2.c.2.C2': 'Autorotation, Trim Speed UP - 85 KIAS',
#     '2.c.2.C3': 'Autorotation, Trim Speed UP - 90 KIAS',
#     '2.c.2.D1': 'Autorotation, Trim Speed DOWN - 75 KIAS, Trim Speed',
#     '2.c.2.D2': 'Autorotation, Trim Speed DOWN - 65 KIAS',
#     '2.c.2.D3': 'Autorotation, Trim Speed DOWN - 55 KIAS',
#     '2.c.4': 'Manoeuvring Stability',
#     '2.c.4.A1': 'Right Turn, Mid Speed - Vy, 0 Bank',
#     '2.c.4.A2': 'Right Turn, Mid Speed - Vy, 30 Bank',
#     '2.c.4.A3': 'Right Turn, Mid Speed - Vy, 45 Bank',
#     '2.c.4.B1': 'Left Turn, Mid Speed - Vy, 0 Bank',
#     '2.c.4.B2': 'Left Turn, Mid Speed - Vy, 30 Bank',
#     '2.c.4.B3': 'Left Turn, Mid Speed - Vy, 45 Bank',
#     '2.c.4.C1': 'Right Turn, High Speed - 120 KIAS, 0 Bank',
#     '2.c.4.C2': 'Right Turn, High Speed - 120 KIAS, 30 Bank',
#     '2.c.4.C3': 'Right Turn, High Speed - 120 KIAS, 45 Bank',
#     '2.c.4.D1': 'Left Turn, High Speed - 120 KIAS, 0 Bank',
#     '2.c.4.D2': 'Left Turn, High Speed - 120 KIAS, 30 Bank',
#     '2.c.4.D3': 'Left Turn, High Speed - 120 KIAS, 45 Bank',
#     '2.d': 'Lateral & Directional Handling Qualities',
#     '2.d.2': 'Directional Static Stability',
#     '2.d.2.A1': 'Mid Speed, DSAS - 100 KIAS, Trim',
#     '2.d.2.A2': 'Mid Speed, DSAS - 100 KIAS, Right Sideslip 1',
#     '2.d.2.A3': 'Mid Speed, DSAS - 100 KIAS, Right Sideslip 2',
#     '2.d.2.B1': 'Mid Speed, AFCS OFF - 100 KIAS, Trim',
#     '2.d.2.B2': 'Mid Speed, AFCS OFF - 100 KIAS, Left Sideslip 1',
#     '2.d.2.B3': 'Mid Speed, AFCS OFF - 100 KIAS, Left Sideslip 2',
#     '2.d.3': 'Dynamic Lateral and Directional Stability',
#     '2.d.3.i': 'Lateral-Directional Oscillations',
#     '2.d.3.i.A1': 'Mid Speed - Vy, DSAS, Left Pedal input ',
#     '2.d.3.i.A2': 'Mid Speed - Vy, AFCS OFF, Left Pedal input ',
#     '2.d.3.i.B1': 'High Speed - 90 KIAS, DSAS, Left Pedal input',
#     '2.d.3.i.B2': 'High Speed - 90 KIAS, AFCS OFF, Left Pedal input',
#     '2.d.3.ii': 'Spiral Stability',
#     '2.d.3.ii.A1': 'Right Input - Vy, DSAS',
#     '2.d.3.ii.A2': 'Right Input - Vy, AFCS OFF',
#     '2.d.3.ii.B1': 'Left Input - Vy, DSAS',
#     '2.d.3.ii.B2': 'Left Input - Vy, AFCS OFF'
# }
#
# # Take-off
# d1c1A1 = " Take Off-All Engines-CAT A on Runway"  # 1
# d1c2A1 = " Take Off-OEI CAT A on Runway"  # 2
#
# # Hover Performance
# sec1d = " Hover Performance"
# d1d1A1 = " Light GW, Aft CG - 3 ft AGL"
# d1d1A2 = " Light GW, Aft CG - 10 ft AGLL"
# d1d1A3 = " Light GW, Aft CG - 25 ft AGL"
# d1d1A4 = " Light GW, Aft CG - 70 ft AGL"
# d1d1B1 = " Heavy GW - 3ft AGL"
# d1d1B2 = " Heavy GW - 10ft AGL"
# d1d1B3 = " Heavy GW - 25ft AGL"
# d1d1B4 = " Heavy GW - 70ft AGL"
#
# # Vertical climb Performance
# d1e1A1 = " Light GW - AEO TOP"
# d1e1B1 = " Heavy GW - AEO MCP"
#
# # Level flight  Performance and Trimmed Flight Condition
# # Info:
# # VH Maximum speed in level flight at maximum continuous power.
# d1f1A1 = " Light GW - VY"
# d1f1A2 = " Light GW - VH"
# d1f1B1 = " Heavy GW - VY"
# d1f1B2 = " Heavy GW - VH"
#
# # Climb Performance and Trimmed Flight Control Position
# # Info:
# # MCP = Maximum continuous power
# # TOP = Take off Power
# d1g1A1 = " Light GW - AEO MCP VY"
# d1g1A2 = " Light GW - AEO TOP VY"
# d1g1A3 = " Light GW - OEI MCP VY"
# d1g1A4 = " Light GW - OEI 2MIN VTOSS"
# d1g1B1 = " Heavy GW - AEO MCP VY"
# d1g1B2 = " Heavy GW - AEO TOP VY"
# d1g1B3 = " Heavy GW - OEI MCP VY"
# d1g1B4 = " Heavy GW - OEI 2MIN VTOSS"
#
# # Descent Performance and Trimmed Flight Control Position
# d1h1A1 = " Light GW - 90KIAS -1000fpm"
# d1h1B1 = " Heavy GW - 90KIAS -1000fpm"
#
# # Landing
# d1j1A1 = " Landing - All Enignes CAT A"
#
# d1j2A1 = " OEI TM - CAT A"
# d1j2A2 = " OEI TM - CAT B"
#
# ##Handling Qualities
#
# # Cycliv Force vs Position
# d2a1A1 = " Cyclic Longitudinal - Trim ON"
# d2a1A2 = " Cyclic Longitudinal - Trim OFF"
# d2a1B1 = " Cyclic Lateral - Trim ON"
# d2a1B2 = " Cyclic Lateral - Trim OFF"
#
# # Collective/Pedals Force vs Position
# d2a2A1 = " Collective - Trim ON"
# d2a2B1 = " Pedals - Trim ON"
#
# # Trim System Rate
# d2a4A1 = " Longitudinal Cyclic - ATRIM"
# d2a4B1 = " Lateral Cyclic - ATRIM"
#
# # Longitudinal Static Stability
# d2c2A1 = " Cruise Trim Speed Up - 120 KIAS, Trim Speed"
# d2c2A2 = " Cruise Trim Speed Up - 125 KIAS"
# d2c2A3 = " Cruise Trim Speed Up - 130 KIAS"
# d2c2B1 = " Cruise Trim Speed Down - 120 KIAS, Trim Speed"
# d2c2B2 = " Cruise Trim Speed Down - 115 KIAS"
# d2c2B3 = " Cruise Trim Speed Down - 110 KIAS"
# d2c2C1 = " Autorotation Trim Speed Up - 75 KIAS, Trim Speed"
# d2c2C2 = " Autorotation Trim Speed Up - 85 KIAS"
# d2c2C3 = " Autorotation Trim Speed Up - 90 KIAS"
# d2c2D1 = " Autorotation Trim Speed Up - 75 KIAS, Trim Speed"
# d2c2D2 = " Autorotation Trim Speed Up - 65 KIAS"
# d2c2D3 = " Autorotation Trim Speed Up - 55 KIAS"
#
# # Manoeuvring Stability
# d2c4A1 = " Right Turn, Vy, 0 Bank"
# d2c4A2 = " Right Turn, Vy, 30 Bank"
# d2c4A3 = " Right Turn, Vy, 45 Bank"
# d2c4B1 = " Left Turn, Vy, 0 Bank"
# d2c4B2 = " Left Turn, Vy, 30 Bank"
# d2c4B3 = " Left Turn, Vy, 45 Bank"
# d2c4C1 = " Right Turn, 120 KIAS, 0 Bank"
# d2c4C2 = " Right Turn, 120 KIAS, 30 Bank"
# d2c4C3 = " Right Turn, 120 KIAS, 45 Bank"
# d2c4D1 = " Left Turn, 120 KIAS, 0 Bank"
# d2c4D2 = " Left Turn, 120 KIAS, 30 Bank"
# d2c4D3 = " Left Turn, 120 KIAS, 45 Bank"
#
# # Diractional static stability
# d2d2A1 = " Mid Speed, 100 KIAS"
# d2d2A2 = " Mid Speed, 100 KIAS Right Sideslip 1"
# d2d2A3 = " Mid Speed, 100 KIAS Right Sideslip 2"
# d2d2B1 = " Mid Speed, 100 KIAS"
# d2d2B2 = " Mid Speed, 100 KIAS Left Sideslip 1"
# d2d2B3 = " Mid Speed, 100 KIAS Left Sideslip 2"
#
# # Lateral directional oscillations
# d2d3iA1 = " Mid Speed Vy, DSAS, Left Pedal input"
# d2d3iA2 = " Mid Speed Vy, AFCS OFF, Left Pedal input"
# d2d3iB1 = " High Speed 90 KIAS, DSAS, Left Pedal input"
# d2d3iB2 = " High Speed 90, AFCS OFF, Left Pedal input"
#
# # Spiral Stability
# d2d3iiA1 = " Right Input, Vy, DSAS"
# d2d3iiA2 = " Right Input, Vy, AFCS OFF"
# d2d3iiB1 = " Left Input, Vy, DSAS"
# d2d3iiB2 = " Left Input, Vy, AFCS OFF"

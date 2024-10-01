# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 15:00:36 2024

@author: simulator
"""

data = {
    'tests': [
        {
            'id': '1',
            'name': 'Performance',
            'test_parts': [
                {
                    'id': 'a.3',
                    'snapshot' : False,
                    'main_title': 'Engine Assessment',
                    'test_title': 'Engine & Rotor Speed Governing',
                    'objective': 'The objective of this test is to demonstrate that the FSTD engine and rotor speed governing is compliant with the reference data.',
                    'tolerances_evaluation_criteria': [
                        {'parameter': 'Engine 1 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Engine 2 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Rotor Speed', 'unit': '[%]', 'tolerance': 'CT&M'}
                    ],
                    'tolerances_recurrent_criteria': [
                        {'parameter': 'Engine 1 Torque', 'unit': '[%]', 'tolerance': '±5'},
                        {'parameter': 'Engine 2 Torque', 'unit': '[%]', 'tolerance': '±5'},
                        {'parameter': 'Rotor Speed', 'unit': '[%]', 'tolerance': '±1.5'}
                    ],
                    'add_plots' : [
                        {'parameter': 'Airspeed', 'unit': '[kts]'},
                        {'parameter': 'Vertical Velocity', 'unit': '[ft/min]'},
                        {'parameter': 'Pitch Angle', 'unit': '[deg]'},
                        {'parameter': 'Bank Angle', 'unit': '[deg]'},
                        {'parameter': 'Heading', 'unit': '[deg]'},
                        {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]'},
                        {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]'},
                        {'parameter': 'Pedals Pos.', 'unit': '[%]'},
                        {'parameter': 'Collective Pos.', 'unit': '[%]'}
                    ],
                    'test_cases': [
                        {
                            'id': 'A1',
                            'name': 'Engine rotor & speed governing',
                            'condition': '90 KIAS, -1000 fpm, up input',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Trim controls to reach 90 KIAS and descent with 1000ft/min',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.',
                                'When the test elapsed time is 3.4 seconds, pull collective to reach a vertival velocity of 800ft/min in 3.5 seconds.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B1',
                            'name': 'Engine rotor & speed governing',
                            'condition': '60 KIAS, AEO MCP, down input',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Trim controls to reach 60 KIAS and climb with 1500ft/min',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.',
                                'When the test elapsed time is 3.6 seconds, push collective to reach descent of 500ft/min in 4.5 seconds'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        }
                    ]
                },
                {
                    'id': 'c.1',
                    'snapshot' : False,
                    'main_title': 'Take-Off',
                    'test_title': 'Take-off All engines',
                    'objective': 'The objective of this test is to demonstrate that the FSTD all engines take-off is compliant with the reference data.',
                    'tolerances_evaluation_criteria': [
                        {'parameter': 'Airspeed', 'unit': '[kts]', 'tolerance': 'CT&M'},
                        {'parameter': 'Radar Altitude', 'unit': '[ft]', 'tolerance': 'CT&M'},
                        {'parameter': 'Engine 1 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Engine 2 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Rotor Speed', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Pitch Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
                        {'parameter': 'Bank Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
                        {'parameter': 'Heading', 'unit': '[deg]', 'tolerance': 'CT&M'},
                        {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Collective Pos.', 'unit': '[%]', 'tolerance': 'CT&M'}
                    ],
                    'tolerances_recurrent_criteria': [
                        {'parameter': 'Airspeed', 'unit': '[kts]', 'tolerance': '±3'},
                        {'parameter': 'Radar Altitude', 'unit': '[ft]', 'tolerance': '±20'},
                        {'parameter': 'Engine 1 Torque', 'unit': '[%]', 'tolerance': '±3'},
                        {'parameter': 'Engine 2 Torque', 'unit': '[%]', 'tolerance': '±3'},
                        {'parameter': 'Rotor Speed', 'unit': '[%]', 'tolerance': '±1.5'},
                        {'parameter': 'Pitch Angle', 'unit': '[deg]', 'tolerance': '±1.5'},
                        {'parameter': 'Bank Angle', 'unit': '[deg]', 'tolerance': '±2'},
                        {'parameter': 'Heading', 'unit': '[deg]', 'tolerance': '±2'},
                        {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': '±10'},
                        {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]', 'tolerance': '±10'},
                        {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': '±10'},
                        {'parameter': 'Collective Pos.', 'unit': '[%]', 'tolerance': '±10'}
                    ],
                    'add_plots' : [
                        {'parameter': 'Sideslip Angle', 'unit': '[deg]'}
                    ],
                    'test_cases': [
                        {
                            'id': 'A1',
                            'name': 'Take-off All engines',
                            'condition': 'CAT A',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Hover in 3ft AGL.',
                                'Press "Enter" to start recording.',
                                'After 2s start take-off run. ',
                                'After 20s an IAS of 40kts and height of 50ft AGL should be reached.',
                                'After 24s an IAS of 60kts and height of 100ft AGL should be reached.',
                                'Maintain 60kts.',
                                'After 35s a height of 280ft AGL should be reached.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        }
                    ]
                },
                {
                    'id': 'c.2',
                    'snapshot' : False,
                    'main_title': 'Take-Off',
                    'test_title': 'OEI continued take-off',
                    'objective': 'The objective of this test is to demonstrate that the FSTD one engine inoperative continued take-off is compliant with the reference data.',
                    'tolerances_evaluation_criteria': [
                        {'parameter': 'Airspeed', 'unit': '[kts]', 'tolerance': 'CT&M'},
                        {'parameter': 'Radar Altitude', 'unit': '[ft]', 'tolerance': 'CT&M'},
                        {'parameter': 'Engine 1 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Engine 2 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Rotor Speed', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Pitch Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
                        {'parameter': 'Bank Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
                        {'parameter': 'Heading', 'unit': '[deg]', 'tolerance': 'CT&M'},
                        {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Collective Pos.', 'unit': '[%]', 'tolerance': 'CT&M'}
                    ],
                    'tolerances_recurrent_criteria': [
                        {'parameter': 'Airspeed', 'unit': '[kts]', 'tolerance': '±3'},
                        {'parameter': 'Radar Altitude', 'unit': '[ft]', 'tolerance': '±20'},
                        {'parameter': 'Engine 1 Torque', 'unit': '[%]', 'tolerance': '±3'},
                        {'parameter': 'Engine 2 Torque', 'unit': '[%]', 'tolerance': '±3'},
                        {'parameter': 'Rotor Speed', 'unit': '[%]', 'tolerance': '±1.5'},
                        {'parameter': 'Pitch Angle', 'unit': '[deg]', 'tolerance': '±1.5'},
                        {'parameter': 'Bank Angle', 'unit': '[deg]', 'tolerance': '±2'},
                        {'parameter': 'Heading', 'unit': '[deg]', 'tolerance': '±2'},
                        {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': '±10'},
                        {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]', 'tolerance': '±10'},
                        {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': '±10'},
                        {'parameter': 'Collective Pos.', 'unit': '[%]', 'tolerance': '±10'}
                    ],
                    'add_plots' : [
                        {'parameter': 'Sideslip Angle', 'unit': '[deg]'}
                    ],
                    'test_cases': [
                        {
                            'id': 'A1',
                            'name': 'OEI continued take-off',
                            'condition': 'OEI',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Hover in 3ft AGL.',
                                'Press "Enter" to start recording.',
                                'After 5s start take-off run. ',
                                'After 25s an IAS of 45kts and height of 100ft AGL should be reached.',
                                'After 35s an IAS of 40kts and height of 320ft AGL should be reached.',
                                'After 35s an IAS of 55kts and height of 400ft AGL should be reached.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        }
                    ]
                },
                {
                    'id': 'd',
                    'snapshot' : True,
                    'main_title': 'Hover Performance',
                    'test_title': '',
                    'objective': 'The objective of this test is to demonstrate that the FSTD hover performance is compliant with the reference data.',
                    'tolerances_evaluation_criteria': [
                        {'parameter': 'Engine 1 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Engine 2 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Pitch Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
                        {'parameter': 'Bank Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
                        {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Collective Pos.', 'unit': '[%]', 'tolerance': 'CT&M'}
                    ],
                    'tolerances_recurrent_criteria': [
                        {'parameter': 'Engine 1 Torque', 'unit': '[%]', 'tolerance': '±3'},
                        {'parameter': 'Engine 2 Torque', 'unit': '[%]', 'tolerance': '±3'},
                        {'parameter': 'Pitch Angle', 'unit': '[deg]', 'tolerance': '±1.5'},
                        {'parameter': 'Bank Angle', 'unit': '[deg]', 'tolerance': '±1.5'},
                        {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': '±5'},
                        {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]', 'tolerance': '±5'},
                        {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': '±5'},
                        {'parameter': 'Collective Pos.', 'unit': '[%]', 'tolerance': '±5'}
                    ],
                    'add_plots' : [
                        {'parameter': 'Radar Altitude', 'unit': '[ft]'}
                    ],
                    'test_cases': [
                        {
                            'id': 'A1',
                            'name': 'Hover Performance',
                            'condition': 'Light GW, Aft CG, 3ft AGL',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Pull Collective until hovering in 3ft AGL'
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'A2',
                            'name': 'Hover Performance',
                            'condition': 'Light GW, Aft CG, 10ft AGL',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Pull Collective until hovering in 10ft AGL'
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'A3',
                            'name': 'Hover Performance',
                            'condition': 'Light GW, Aft CG, 25ft AGL',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Pull Collective until hovering in 25ft AGL'
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'A4',
                            'name': 'Hover Performance',
                            'condition': 'Light GW, Aft CG, 70ft AGL',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Pull Collective until hovering in 70ft AGL'
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B1',
                            'name': 'Hover Performance',
                            'condition': 'Heavy GW, Forward CG, 3ft AGL',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Pull Collective until hovering in 3ft AGL'
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B2',
                            'name': 'Hover Performance',
                            'condition': 'Heavy GW, Forward CG, 10ft AGL',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Pull Collective until hovering in 10ft AGL'
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B3',
                            'name': 'Hover Performance',
                            'condition': 'Heavy GW, Forward CG, 25ft AGL',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Pull Collective until hovering in 25ft AGL'
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B4',
                            'name': 'Hover Performance',
                            'condition': 'Heavy GW, Forward CG, 70ft AGL',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Pull Collective until hovering in 70ft AGL'
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        }
                    ]
                },
                {
                    'id': 'e',
                    'snapshot' : True,
                    'main_title': 'Vertical Climb Performance',
                    'test_title': 'Vertical Climb Performance',
                    'objective': 'The objective of this test is to demonstrate that the FSTD vertical climb performance is compliant with the reference data.',
                    'tolerances_evaluation_criteria': [
                        {'parameter': 'Vertical Velocity', 'unit': '[ft/min]', 'tolerance': 'CT&M'},
                        {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Collective Pos.', 'unit': '[%]', 'tolerance': 'CT&M'}
                    ],
                    'tolerances_recurrent_criteria': [
                        {'parameter': 'Vertical Velocity', 'unit': '[ft/min]', 'tolerance': '±100'},
                        {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': '±5'},
                        {'parameter': 'Collective Pos.', 'unit': '[%]', 'tolerance': '±5'}
                    ],
                    'add_plots' : [
                        {'parameter': 'Engine 1 Torque', 'unit': '[%]'},
                        {'parameter': 'Engine 2 Torque', 'unit': '[%]'},
                        {'parameter': 'Pitch Angle', 'unit': '[deg]'},
                        {'parameter': 'Bank Angle', 'unit': '[deg]'},
                        {'parameter': 'Heading', 'unit': '[deg]'},
                        {'parameter': 'Groundspeed', 'unit': '[kts]'},
                        {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]'},
                        {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]'}
                    ],
                    'test_cases': [
                        {
                            'id': 'A1',
                            'name': 'Vertical Climb Performance',
                            'condition': 'Light GW, Aft CG - AEO TOP',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Pull collective until the FLI reaches TOP.',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B1',
                            'name': 'Vertical Climb Performance',
                            'condition': 'Heavy GW, Fwd CG - AEO MCP',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Pull collective until the FLI reaches MCP',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        }
                    ]
                },
                {
                    'id': 'f',
                    'snapshot' : True,
                    'main_title': 'Level Flight Performance and Trimmed Flight Control Position',
                    'test_title': 'Level Flight Performance and Trimmed Flight Control Position',
                    'objective': 'The objective of this test is to demonstrate that the FSTD level flight performance is compliant with the reference data.',
                    'tolerances_evaluation_criteria': [
                        {'parameter': 'Engine 1 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Engine 2 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Pitch Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
                        {'parameter': 'Sideslip Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
                        {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Collective Pos.', 'unit': '[%]', 'tolerance': 'CT&M'}
                    ],
                    'tolerances_recurrent_criteria': [
                        {'parameter': 'Engine 1 Torque', 'unit': '[%]', 'tolerance': '±3'},
                        {'parameter': 'Engine 2 Torque', 'unit': '[%]', 'tolerance': '±3'},
                        {'parameter': 'Pitch Angle', 'unit': '[deg]', 'tolerance': '±1.5'},
                        {'parameter': 'Sideslip Angle', 'unit': '[deg]', 'tolerance': '±2'},
                        {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': '±5'},
                        {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]', 'tolerance': '±5'},
                        {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': '±5'},
                        {'parameter': 'Collective Pos.', 'unit': '[%]', 'tolerance': '±5'}
                    ],
                    'add_plots' : [
                        {'parameter': 'Airspeed', 'unit': '[kts]'},
                        {'parameter': 'Rotor Speed', 'unit': '[%]'}
                    ],
                    'test_cases': [
                        {
                            'id': 'A1',
                            'name': 'Level Flight Performance and Trimmed Flight Control Position',
                            'condition': 'Light GW, Aft CG - 64 KIAS',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Set controls to reach target values.',
                                'Trim controls to reach 64 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'A2',
                            'name': 'Level Flight Performance and Trimmed Flight Control Position',
                            'condition': 'Light GW, Aft CG - 130 KIAS',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Set controls to reach target values.',
                                'Trim controls to reach 130 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B1',
                            'name': 'Level Flight Performance and Trimmed Flight Control Position',
                            'condition': 'Heavy GW, Forward CG - 64 KIAS',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Set controls to reach target values.',
                                'Trim controls to reach 64 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B2',
                            'name': 'Level Flight Performance and Trimmed Flight Control Position',
                            'condition': 'Heavy GW, Forward CG - 130 KIAS',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Set controls to reach target values.',
                                'Trim controls to reach 130 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        }
                    ]
                },
                {
                    'id': 'g',
                    'snapshot' : True,
                    'main_title': 'Climb Performance and Trimmed Flight Control Position',
                    'test_title': 'Climb Performance and Trimmed Flight Control Position',
                    'objective': 'The objective of this test is to demonstrate that the FSTD climb performance is compliant with the reference data.',
                    'tolerances_evaluation_criteria': [
                        {'parameter': 'Vertical Velocity', 'unit': '[ft/min]', 'tolerance': 'CT&M'},
                        {'parameter': 'Pitch Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
                        {'parameter': 'Sideslip Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
                        {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Collective Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Airspeed', 'unit': '[kts]', 'tolerance': 'CT&M'}
                    ],
                    'tolerances_recurrent_criteria': [
                        {'parameter': 'Vertical Velocity', 'unit': '[ft/min]', 'tolerance': '±100'},
                        {'parameter': 'Pitch Angle', 'unit': '[deg]', 'tolerance': '±1.5'},
                        {'parameter': 'Sideslip Angle', 'unit': '[deg]', 'tolerance': '±2'},
                        {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': '±5'},
                        {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]', 'tolerance': '±5'},
                        {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': '±5'},
                        {'parameter': 'Collective Pos.', 'unit': '[%]', 'tolerance': '±5'},
                        {'parameter': 'Airspeed', 'unit': '[kts]', 'tolerance': '±3'}
                    ],
                    'add_plots' : [
                        {'parameter': 'Engine 1 Torque', 'unit': '[%]'},
                        {'parameter': 'Engine 2 Torque', 'unit': '[%]'},
                        {'parameter': 'Heading', 'unit': '[deg]'},
                        {'parameter': 'Bank Angle', 'unit': '[deg]'}
                    ],
                    'test_cases': [
                        {
                            'id': 'A1',
                            'name': 'Climb Performance and Trimmed Flight Control Position',
                            'condition': 'Light GW, Aft CG - AEO MCP, 63 KIAS',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Pull collective until the FLI reaches MCP.',
                                'Trim controls to reach 63 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'A2',
                            'name': 'Climb Performance and Trimmed Flight Control Position',
                            'condition': 'Light GW, Aft CG - AEO TOP, 63 KIAS',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Pull collective until the FLI reaches TOP.',
                                'Trim controls to reach 63 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'A3',
                            'name': 'Climb Performance and Trimmed Flight Control Position',
                            'condition': 'Light GW, Aft CG - OEI MCP, 64 KIAS',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Pull collective until the FLI reaches MCP.',
                                'Trim controls to reach 64 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'A4',
                            'name': 'Climb Performance and Trimmed Flight Control Position',
                            'condition': 'Light GW, Aft CG - OEI 2 min, 38 KIAS',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Pull collective until the FLI reaches 2 min.',
                                'Trim controls to reach 38 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'A5',
                            'name': 'Climb Performance and Trimmed Flight Control Position',
                            'condition': 'Light GW, Aft CG - OEI 30s, 37 KIAS',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Pull collective until the FLI reaches 30s.',
                                'Trim controls to reach 37 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B1',
                            'name': 'Climb Performance and Trimmed Flight Control Position',
                            'condition': 'Heavy GW, Forward CG - AEO MCP, 62 KIAS',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Pull collective until the FLI reaches MCP.',
                                'Trim controls to reach 62 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B2',
                            'name': 'Climb Performance and Trimmed Flight Control Position',
                            'condition': 'Heavy GW, Forward CG - AEO TOP, 62 KIAS',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Pull collective until the FLI reaches TOP.',
                                'Trim controls to reach 62 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B3',
                            'name': 'Climb Performance and Trimmed Flight Control Position',
                            'condition': 'Heavy GW, Forward CG - OEI MCP, 65 KIAS',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Pull collective until the FLI reaches MCP.',
                                'Trim controls to reach 65 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B4',
                            'name': 'Climb Performance and Trimmed Flight Control Position',
                            'condition': 'Heavy GW, Forward CG - OEI 2 min, 35 KIAS',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Pull collective until the FLI reaches 2 min.',
                                'Trim controls to reach 35 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B5',
                            'name': 'Climb Performance and Trimmed Flight Control Position',
                            'condition': 'Heavy GW, Forward CG - OEI 30 s, 42 KIAS',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Pull collective until the FLI reaches 30s.',
                                'Trim controls to reach 42 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        }
                    ]
                },
                {
                    'id': 'h.1',
                    'snapshot' : True,
                    'main_title': 'Descent',
                    'test_title': 'Descent Performance and Trimmed Flight Control Position',
                    'objective': 'The objective of this test is to demonstrate that the FSTD descent performance is compliant with the reference data.',
                    'tolerances_evaluation_criteria': [
                        {'parameter': 'Engine 1 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Engine 2 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Pitch Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
                        {'parameter': 'Sideslip Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
                        {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Collective Pos.', 'unit': '[%]', 'tolerance': 'CT&M'}
                    ],
                    'tolerances_recurrent_criteria': [
                        {'parameter': 'Engine 1 Torque', 'unit': '[%]', 'tolerance': '±3'},
                        {'parameter': 'Engine 2 Torque', 'unit': '[%]', 'tolerance': '±3'},
                        {'parameter': 'Pitch Angle', 'unit': '[deg]', 'tolerance': '±1.5'},
                        {'parameter': 'Sideslip Angle', 'unit': '[deg]', 'tolerance': '±2'},
                        {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': '±5'},
                        {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]', 'tolerance': '±5'},
                        {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': '±5'},
                        {'parameter': 'Collective Pos.', 'unit': '[%]', 'tolerance': '±5'}
                    ],
                    'add_plots' : [
                        {'parameter': 'Airspeed', 'unit': '[kts]'},
                        {'parameter': 'Pitch Angle', 'unit': '[deg]'},
                        {'parameter': 'Bank Angle', 'unit': '[deg]'},
                        {'parameter': 'Heading', 'unit': '[deg]'},
                        {'parameter': 'Vertical Velocity', 'unit': '[ft/min]'}
                    ],
                    'test_cases': [
                        {
                            'id': 'A1',
                            'name': 'Descent Performance and Trimmed Flight Control Position',
                            'condition': 'Light GW, Aft CG - 90 KIAS, -1000 fpm',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Push collective until reaching 1000 fpm of descent',
                                'Trim controls to reach 90 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B1',
                            'name': 'Descent Performance and Trimmed Flight Control Position',
                            'condition': 'Heavy GW, Fwd CG - 90 KIAS, -1000 fpm',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Push collective until reaching 1000 fpm of descent',
                                'Trim controls to reach 90 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        }
                    ]
                },
                {
                    'id': 'j.1',
                    'snapshot' : False,
                    'main_title': 'Landing',
                    'test_title': 'Landing - All Engines',
                    'objective': 'The objective of this test is to demonstrate that the FSTD landing performance with all engines operative is compliant with the reference data.',
                    'tolerances_evaluation_criteria': [
                        {'parameter': 'Airspeed', 'unit': '[kts]', 'tolerance': 'CT&M'},
                        {'parameter': 'Radar Altitude', 'unit': '[ft]', 'tolerance': 'CT&M'},
                        {'parameter': 'Engine 1 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Engine 2 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Rotor Speed', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Pitch Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
                        {'parameter': 'Bank Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
                        {'parameter': 'Heading', 'unit': '[deg]', 'tolerance': 'CT&M'},
                        {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Collective Pos.', 'unit': '[%]', 'tolerance': 'CT&M'}
                    ],
                    'tolerances_recurrent_criteria': [
                        {'parameter': 'Airspeed', 'unit': '[kts]', 'tolerance': '±3'},
                        {'parameter': 'Radar Altitude', 'unit': '[ft]', 'tolerance': '±20'},
                        {'parameter': 'Engine 1 Torque', 'unit': '[%]', 'tolerance': '±3'},
                        {'parameter': 'Engine 2 Torque', 'unit': '[%]', 'tolerance': '±3'},
                        {'parameter': 'Rotor Speed', 'unit': '[%]', 'tolerance': '±1.5'},
                        {'parameter': 'Pitch Angle', 'unit': '[deg]', 'tolerance': '±1.5'},
                        {'parameter': 'Bank Angle', 'unit': '[deg]', 'tolerance': '±1.5'},
                        {'parameter': 'Heading', 'unit': '[deg]', 'tolerance': '±2'},
                        {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': '±10'},
                        {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]', 'tolerance': '±10'},
                        {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': '±10'},
                        {'parameter': 'Collective Pos.', 'unit': '[%]', 'tolerance': '±10'}
                    ],
                    'add_plots' : [
                        {'parameter': 'Sideslip Angle', 'unit': '[deg]'},
                        {'parameter': 'Vertical Velocity', 'unit': '[ft/min]'}
                    ],
                    'test_cases': [
                        {
                            'id': 'A1',
                            'name': 'Landing - All Engines',
                            'condition': 'CAT A',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Start from position: '
                                'Climb up to 316ft AGL.',
                                'Trim controls to reach and maintain 70 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.',
                                'When the test elapsed time is 1.0 seconds, decrease collective to achieve 450 ft/min of rate of descent in approximately 20.0 seconds and maintain it. In the meantime move controls to reduce airspeed by 20.0 KIAS and maintain it.',
                                'When the test elapsed time is 36.0 seconds, increase collective to achieve level flight condition in approximately 13.0 seconds. In the meantime move controls to reach an hover condition in 23.0 seconds and maintain it.',
                                'Continue the maneuver touching the ground when the test elapsed time is 59.0 seconds.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        }
                    ]
                },
                {
                    'id': 'j.2',
                    'snapshot' : False,
                    'main_title': 'Landing',
                    'test_title': 'Landing - One Engine Inoperative',
                    'objective': 'The objective of this test is to demonstrate that the FSTD one engine inoperative landing is compliant with the reference data.',
                    'tolerances_evaluation_criteria': [
                        {'parameter': 'Airspeed', 'unit': '[kts]', 'tolerance': 'CT&M'},
                        {'parameter': 'Radar Altitude', 'unit': '[ft]', 'tolerance': 'CT&M'},
                        {'parameter': 'Engine 1 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Engine 2 Torque', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Rotor Speed', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Pitch Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
                        {'parameter': 'Bank Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
                        {'parameter': 'Heading', 'unit': '[deg]', 'tolerance': 'CT&M'},
                        {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Collective Pos.', 'unit': '[%]', 'tolerance': 'CT&M'}
                    ],
		            'tolerances_recurrent_criteria': [
                        {'parameter': 'Airspeed', 'unit': '[kts]', 'tolerance': '±3'},
                        {'parameter': 'Radar Altitude', 'unit': '[ft]', 'tolerance': '±20'},
                        {'parameter': 'Engine 1 Torque', 'unit': '[%]', 'tolerance': '±3'},
                        {'parameter': 'Engine 2 Torque', 'unit': '[%]', 'tolerance': '±3'},
                        {'parameter': 'Rotor Speed', 'unit': '[%]', 'tolerance': '±1.5'},
                        {'parameter': 'Pitch Angle', 'unit': '[deg]', 'tolerance': '±1.5'},
                        {'parameter': 'Bank Angle', 'unit': '[deg]', 'tolerance': '±1.5'},
                        {'parameter': 'Heading', 'unit': '[deg]', 'tolerance': '±2'},
                        {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': '±10'},
                        {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]', 'tolerance': '±10'},
                        {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': '±10'},
                        {'parameter': 'Collective Pos.', 'unit': '[%]', 'tolerance': '±10'}
                    ],
                    'add_plots' : [
                        {'parameter': 'Sideslip Angle', 'unit': '[deg]'},
                        {'parameter': 'Vertical Velocity', 'unit': '[ft/min]'}
                    ],
                    'test_cases': [
                        {
                            'id': 'A1',
                            'name': 'Landing - One Engine Inoperative',
                            'condition': 'OEI - CAT A',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Start from position: '
                                'Climb up to 305ft AGL.',
                                'Trim controls to reach and maintain 68 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.',
                                'Maintain pitch attitude to 5.0 deg nose up to reach 40 KIAS in 42.0 seconds, while maintaining a 300 ft/min rate of descent.',
                                'When the test elapsed time is 42.0 seconds, maintain 40 KIAS and continue the descent.',
                                'When the test elapsed time is 48.0 seconds, decrease the airspeed to 20.0 KIAS in 11.0 seconds and continue the descent.',
                                'When the test elapsed time is 52.0 seconds, Instructor press the Engine 1 Fail button on the IOS, continuing descent and increase pitch in order to reach an attitude of 16.0 deg in 10.0 seconds.',
                                'Continue decreasing ground speed to reach 5.0 kts when the test elapsed time is 70.0 seconds.',
                                'Start to pull the collective to cushion the landing and touch the ground when the test elapsed time is 72.0 seconds.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'A2',
                            'name': 'Landing - One Engine Inoperative',
                            'condition': 'OEI - CAT B',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Start from position: '
                                'Climb up to 270ft AGL.',
                                'Trim controls to reach and maintain 77 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.',
                                'Increase pitch attitude to 6.0 deg nose up to reach 40 KIAS in 34.0 seconds, while maintaining a 300 ft/min rate of descent.',
                                'When the test elapsed time is 34.0 seconds, maintain 40 KIAS and continue the descent.',
                                'When the test elapsed time is 40.0 seconds, decrease the airspeed to 20.0 KIAS in 10.0 seconds and continue the descent.',
                                'When the test elapsed time is 47.0 seconds, increase pitch in order to reach an attitude of 13.0 deg in 8.0 seconds.',
                                'Continue decreasing ground speed to reach 5.0 kts when the test elapsed time is 60.0 seconds.',
                                'Start to pull the collective to cushion the landing and touch the ground when the test elapsed time is 74.0 seconds.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        }
                    ]
                }
            ]
        },
        {
            'id': '2',
            'name': 'Handling Qualities',
            'test_parts': [
                {
                    'id': 'a.1',
                    'snapshot' : False,
                    'main_title': 'Control System Mechanical Characteristics',
                    'test_title': 'Cyclic Force vs Position',
                    'objective': 'The objective of this test is to demonstrate that the FSTD Cyclic Control System Mechanical Characteristics are compliant with the reference data.',
                    'tolerances_evaluation_criteria': [
                        {'parameter': 'Breakout', 'unit': '[daN]', 'tolerance': 'CT&M'},
                        {'parameter': 'Force', 'unit': '[daN]', 'tolerance': 'CT&M'}
                    ],
                    'tolerances_recurrent_criteria': [
                        {'parameter': 'Breakout', 'unit': '[daN]', 'tolerance': '±0.112'},
                        {'parameter': 'Force', 'unit': '[daN]', 'tolerance': '±0.224'}
                    ],
                    'add_plots' : [
                        {'parameter': 'Dummy'}
                    ],
                    'test_cases': [
                        {
                            'id': 'A1',
                            'name': 'Cyclic Force vs Position',
                            'condition': 'Longitudinal cyclic - Trim ON',
                            'automatic_testing_possible': False,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                           'manual_testing': [
                               'On the left column double click on the corresponding test. The test will displayed in the right column.',
                               'Right click on the corresponding test in the right column to change in manual mode.',
                               'Press "Start QTG" to start the test.',
                               'In the text field below, enter the desired time for the test to run. Press "Enter".',
                               'Press "Enter" to start recording.',
                               'Move the Cyclic stick to perform a complete sweep on the longitudinal axis.'
                           ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'A2',
                            'name': 'Cyclic Force vs Position',
                            'condition': 'Longitudinal cyclic - Trim OFF',
                            'automatic_testing_possible': False,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Press "Enter" to start recording.',
                                'Move the Cyclic stick to perform a complete sweep on the longitudinal axis while pressing the FTR Release button.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B1',
                            'name': 'Cyclic Force vs Position',
                            'condition': 'Lateral cyclic - Trim ON',
                            'automatic_testing_possible': False,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Press "Enter" to start recording.',
                                'Move the Cyclic stick to perform a complete sweep on the lateral axis.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B2',
                            'name': 'Cyclic Force vs Position',
                            'condition': 'Lateral cyclic - Trim OFF',
                            'automatic_testing_possible': False,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Press "Enter" to start recording.',
                                'Move the Cyclic stick to perform a complete sweep on the lateral axis while pressing the FTR Release button.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        }
                    ]
                },
                {
                    'id': 'a.2',
                    'snapshot' : False,
                    'main_title': 'Control System Mechanical Characteristics',
                    'test_title': 'Collective/Pedals Force vs Position',
                    'objective': 'The objective of this test is to demonstrate that the FSTD Collective/Pedals Control System Mechanical Characteristics are compliant with the reference data.',
                    'tolerances_evaluation_criteria': [
                        {'parameter': 'Breakout', 'unit': '[daN]', 'tolerance': 'CT&M'},
                        {'parameter': 'Force', 'unit': '[daN]', 'tolerance': 'CT&M'}
                    ],
            		    'tolerances_recurrent_criteria': [
                        {'parameter': 'Breakout', 'unit': '[daN]', 'tolerance': '±0.224'},
                        {'parameter': 'Force', 'unit': '[daN]', 'tolerance': '±0.448'}
                    ],
                    'add_plots' : [
                        {'parameter': 'Dummy'}
                    ],
                    'test_cases': [
                        {
                            'id': 'A1',
                            'name': 'Collective/Pedals Force vs Position',
                            'condition': 'Collective - Trim ON',
                            'automatic_testing_possible': False,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Press "Enter" to start recording.',
                                'Move the Collective lever to perform a complete sweep.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B1',
                            'name': 'Collective/Pedals Force vs Position',
                            'condition': 'Pedals - Trim ON',
                            'automatic_testing_possible': False,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Press "Enter" to start recording.',
                                'Move the Pedals to perform a complete sweep.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        }
                    ]
                },
                {
                    'id': 'a.4',
                    'snapshot' : False,
                    'main_title': 'Control System Mechanical Characteristics',
                    'test_title': 'Trim System Rate',
                    'objective': 'The objective of this test is to demonstrate that the FSTD Trim System Rate Characteristics are compliant with the reference data.',
                    'tolerances_evaluation_criteria': [
                        {'parameter': 'Trim Rate', 'unit': '[%]', 'tolerance': 'CT&M'}
                    ],
    		          'tolerances_recurrent_criteria': [
                        {'parameter': 'Trim Rate', 'unit': '[%]', 'tolerance': '±10'}
                    ],
                    'add_plots' : [
                        {'parameter': 'Dummy'}
                    ],
                    'test_cases': [
                        {
                            'id': 'A1',
                            'name': 'Longitudinal Cyclic',
                            'condition': 'Longitudinal Cyclic - ATRIM',
                            'automatic_testing_possible': False,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Press "Enter" to start recording.',
                                'Press the Beep-Trim to move the Cyclic stick in the full aft position on the longitudinal axis.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B1',
                            'name': 'Lateral Cyclic',
                            'condition': 'Lateral Cyclic - ATRIM',
                            'automatic_testing_possible': False,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Press "Enter" to start recording.',
                                'Press the Beep-Trim to move the Cyclic stick in the full right position on the lateral axis.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        }
                    ]
                },
                {
                    'id': 'c.2',
                    'snapshot' : True,
                    'main_title': 'Longitudinal Handling Qualities',
                    'test_title': 'Longitudinal Static Stability',
                    'objective': 'The objective of this test is to demonstrate that the FSTD longitudinal static stability is compliant with the reference data.',
                    'tolerances_evaluation_criteria': [
                        {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'}
                    ],
        		    'tolerances_recurrent_criteria': [
                        {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': '±10'}
                    ],
                    'add_plots' : [
                        {'parameter': 'Airspeed', 'unit': '[kts]'},
                        {'parameter': 'Pitch Angle', 'unit': '[deg]'},
                        {'parameter': 'Bank Angle', 'unit': '[deg]'},
                        {'parameter': 'Heading', 'unit': '[deg]'},
                        {'parameter': 'Engine 1 Torque', 'unit': '[%]'},
                        {'parameter': 'Engine 2 Torque', 'unit': '[%]'},
                        {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]'},
                        {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]'},
                        {'parameter': 'Pedals Pos.', 'unit': '[%]'},
                        {'parameter': 'Collective Pos.', 'unit': '[%]'},
                        {'parameter': 'Rotor Speed', 'unit': '[%]'}
                    ],
                    'test_cases': [
                        {
                            'id': 'A1',
                            'name': 'Longitudinal Static Stability',
                            'condition': 'Cruise, Trim Speed UP - 120 KIAS, Trim Speed',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Trim controls to reach 119 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Leave the collective fixed at its initial value and maintain the target IAS.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'A2',
                            'name': 'Longitudinal Static Stability',
                            'condition': 'Cruise, Trim Speed UP - 125 KIAS',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Trim controls to reach and maintain 124 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Leave the collective fixed at its initial value and maintain the target IAS.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'A3',
                            'name': 'Longitudinal Static Stability',
                            'condition': 'Cruise, Trim Speed UP - 130 KIAS',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Trim controls to reach and maintain 129 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Leave the collective fixed at its initial value and maintain the target IAS.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B1',
                            'name': 'Longitudinal Static Stability',
                            'condition': 'Cruise, Trim Speed DOWN - 120 KIAS, Trim Speed',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Trim controls to reach and maintain 120 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Leave the collective fixed at its initial value and maintain the target IAS.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B2',
                            'name': 'Longitudinal Static Stability',
                            'condition': 'Cruise, Trim Speed DOWN - 115 KIAS',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Trim controls to reach and maintain 115 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Leave the collective fixed at its initial value and maintain the target IAS.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B3',
                            'name': 'Longitudinal Static Stability',
                            'condition': 'Cruise, Trim Speed DOWN - 110 KIAS',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Trim controls to reach and maintain 107 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Leave the collective fixed at its initial value and maintain the target IAS.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'C1',
                            'name': 'Longitudinal Static Stability',
                            'condition': 'Autorotation, Trim Speed UP - 75 KIAS, Trim Speed',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Trim controls to reach and maintain 74 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Leave the collective fixed at its initial value and maintain the target IAS.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'C2',
                            'name': 'Longitudinal Static Stability',
                            'condition': 'Autorotation, Trim Speed UP - 85 KIAS',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Trim controls to reach and maintain 84 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Leave the collective fixed at its initial value and maintain the target IAS.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'C3',
                            'name': 'Longitudinal Static Stability',
                            'condition': 'Autorotation, Trim Speed UP - 90 KIAS',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Trim controls to reach and maintain 88 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Leave the collective fixed at its initial value and maintain the target IAS.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'D1',
                            'name': 'Longitudinal Static Stability',
                            'condition': 'Autorotation, Trim Speed DOWN - 75 KIAS, Trim Speed',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Trim controls to reach and maintain 75 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Leave the collective fixed at its initial value and maintain the target IAS.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'D2',
                            'name': 'Longitudinal Static Stability',
                            'condition': 'Autorotation, Trim Speed DOWN - 65 KIAS',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Trim controls to reach and maintain 65 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Leave the collective fixed at its initial value and maintain the target IAS.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'D3',
                            'name': 'Longitudinal Static Stability',
                            'condition': 'Autorotation, Trim Speed DOWN - 55 KIAS',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Trim controls to reach and maintain 55 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Leave the collective fixed at its initial value and maintain the target IAS.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        }
                    ]
                },
                {
                    'id': 'c.4',
                    'snapshot' : True,
                    'main_title': 'Longitudinal Handling Qualities',
                    'test_title': 'Manoeuvring Stability',
                    'objective': 'The objective of this test is to demonstrate that the FSTD longitudinal manoeuvring stability is compliant with the reference data.',
                    'tolerances_evaluation_criteria': [
                        {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'}
                    ],
        		    'tolerances_recurrent_criteria': [
                            {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': '±10'}
                    ],
                    'add_plots' : [
                        {'parameter': 'Airspeed', 'unit': '[kts]'},
                        {'parameter': 'Pitch Angle', 'unit': '[deg]'},
                        {'parameter': 'Bank Angle', 'unit': '[deg]'},
                        {'parameter': 'Heading', 'unit': '[deg]'},
                        {'parameter': 'Engine 1 Torque', 'unit': '[%]'},
                        {'parameter': 'Engine 2 Torque', 'unit': '[%]'},
                        {'parameter': 'Rotor Speed', 'unit': '[%]'},
                        {'parameter': 'Sideslip Angle', 'unit': '[deg]'},
                        {'parameter': 'Vertical Velocity', 'unit': '[ft/min]'},
                        {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]'},
                        {'parameter': 'Pedals Pos.', 'unit': '[%]'},
                        {'parameter': 'Collective Pos.', 'unit': '[%]'}
                    ],
                    'test_cases': [
                        {
                            'id': 'A1',
                            'name': 'Manoeuvring Stability',
                            'condition': 'Right Turn, Mid Speed - 65 KIAS, 0 Bank',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Set controls to reach target values.',
                                'Maintain level flight or turn at the initialisation speed, leaving the collective set at its initial value.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'A2',
                            'name': 'Manoeuvring Stability',
                            'condition': 'Right Turn, Mid Speed - 65 KIAS, 30 Bank',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Set controls to reach target values.',
                                'Maintain level flight or turn at the initialisation speed, leaving the collective set at its initial value.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'A3',
                            'name': 'Manoeuvring Stability',
                            'condition': 'Right Turn, Mid Speed - 65 KIAS, 45 Bank',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Set controls to reach target values.',
                                'Maintain level flight or turn at the initialisation speed, leaving the collective set at its initial value.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B1',
                            'name': 'Manoeuvring Stability',
                            'condition': 'Left Turn, Mid Speed - 66 KIAS, 0 Bank',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Set controls to reach target values.',
                                'Maintain level flight or turn at the initialisation speed, leaving the collective set at its initial value.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B2',
                            'name': 'Manoeuvring Stability',
                            'condition': 'Left Turn, Mid Speed - 65 KIAS, 30 Bank',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Set controls to reach target values.',
                                'Maintain level flight or turn at the initialisation speed, leaving the collective set at its initial value.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B3',
                            'name': 'Manoeuvring Stability',
                            'condition': 'Left Turn, Mid Speed - 66 KIAS, 45 Bank',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Set controls to reach target values.',
                                'Maintain level flight or turn at the initialisation speed, leaving the collective set at its initial value.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'C1',
                            'name': 'Manoeuvring Stability',
                            'condition': 'Right Turn, High Speed - 120 KIAS, 0 Bank',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Set controls to reach target values.',
                                'Maintain level flight or turn at the initialisation speed, leaving the collective set at its initial value.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'C2',
                            'name': 'Manoeuvring Stability',
                            'condition': 'Right Turn, High Speed - 120 KIAS, 30 Bank',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Set controls to reach target values.',
                                'Maintain level flight or turn at the initialisation speed, leaving the collective set at its initial value.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'C3',
                            'name': 'Manoeuvring Stability',
                            'condition': 'Right Turn, High Speed - 120 KIAS, 45 Bank',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Set controls to reach target values.',
                                'Maintain level flight or turn at the initialisation speed, leaving the collective set at its initial value.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'D1',
                            'name': 'Manoeuvring Stability',
                            'condition': 'Left Turn, High Speed - 120 KIAS, 0 Bank',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Set controls to reach target values.',
                                'Maintain level flight or turn at the initialisation speed, leaving the collective set at its initial value.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'D2',
                            'name': 'Manoeuvring Stability',
                            'condition': 'Left Turn, High Speed - 120 KIAS, 30 Bank',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Set controls to reach target values.',
                                'Maintain level flight or turn at the initialisation speed, leaving the collective set at its initial value.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'D3',
                            'name': 'Manoeuvring Stability',
                            'condition': 'Left Turn, High Speed - 120 KIAS, 45 Bank',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Set controls to reach target values.',
                                'Maintain level flight or turn at the initialisation speed, leaving the collective set at its initial value.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        }
                    ]
                },
                {
                    'id': 'd.2',
                    'snapshot' : True,
                    'main_title': 'Lateral & Directional Handling Qualities',
                    'test_title': 'Directional Static Stability',
                    'objective': 'The objective of this test is to demonstrate that the FSTD directional static stability is compliant with the reference data.',
                    'tolerances_evaluation_criteria': [
                        {'parameter': 'Bank Angle', 'unit': '[deg]', 'tolerance': 'CT&M'},
                        {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]', 'tolerance': 'CT&M'},
                        {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': 'CT&M'}
                    ],
        		    'tolerances_recurrent_criteria': [
                        {'parameter': 'Bank Angle', 'unit': '[deg]', 'tolerance': '±1.5'},
                        {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]', 'tolerance': '±10'},
                        {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]', 'tolerance': '±10'},
                        {'parameter': 'Pedals Pos.', 'unit': '[%]', 'tolerance': '±10'}
                    ],
                    'add_plots' : [
                        {'parameter': 'Airspeed', 'unit': '[kts]'},
                        {'parameter': 'Pitch Angle', 'unit': '[deg]'},
                        {'parameter': 'Heading', 'unit': '[deg]'},
                        {'parameter': 'Engine 1 Torque', 'unit': '[%]'},
                        {'parameter': 'Engine 2 Torque', 'unit': '[%]'},
                        {'parameter': 'Sideslip Angle', 'unit': '[deg]'},
                        {'parameter': 'Pedals Pos.', 'unit': '[%]'},
                        {'parameter': 'Collective Pos.', 'unit': '[%]'}
                    ],
                    'test_cases': [
                        {
                            'id': 'A1',
                            'name': 'Directional Static Stability',
                            'condition': 'Mid Speed - 100 KIAS, Trim',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Set controls to reach target values.',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'A2',
                            'name': 'Directional Static Stability',
                            'condition': 'Mid Speed - 100 KIAS, Right Sideslip 1',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Set controls to reach target values.',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'A3',
                            'name': 'Directional Static Stability',
                            'condition': 'Mid Speed - 100 KIAS, Right Sideslip 2',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Set controls to reach target values.',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B1',
                            'name': 'Directional Static Stability',
                            'condition': 'Mid Speed - 100 KIAS, Trim',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Set controls to reach target values.',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B2',
                            'name': 'Directional Static Stability',
                            'condition': 'Mid Speed - 100 KIAS, Left Sideslip 1',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Set controls to reach target values.',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B3',
                            'name': 'Directional Static Stability',
                            'condition': 'Mid Speed - 100 KIAS, Left Sideslip 2',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Set controls to reach target values.',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        }
                    ]
                },
                {
                    'id': 'd.3.i',
                    'snapshot' : False,
                    'main_title': 'Dynamic Lateral and Directional Stability',
                    'test_title': 'Lateral-Directional Oscillations',
                    'objective': 'The objective of this test is to demonstrate that the FSTD dynamic lateral-directional stability (oscillations) is compliant with the reference data.',
# =============================================================================
#                     'tolerances_evaluation_criteria': [
#                         {'parameter': 'Calculated period', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Time to 1/2 amplitude', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'or Time to Double amplitude', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'or Damping Ratio', 'unit': '[%]', 'tolerance': 'CT&M'},
#                         {'parameter': 'Time difference between peaks of Bank and Sideslip', 'unit': '[s]',
#                          'tolerance': 'CT&M'},
#                         {'parameter': 'Non-periodic response', 'unit': '[-]', 'tolerance': 'Time history'}
#                     ],
#         		    'tolerances_recurrent_criteria': [
#                         {'parameter': 'Calculated period', 'unit': '[%]', 'tolerance': '±10'},
#                         {'parameter': 'Time to 1/2 amplitude', 'unit': '[%]', 'tolerance': '±10'},
#                         {'parameter': 'or Time to Double amplitude', 'unit': '[%]', 'tolerance': '±10'},
#                         {'parameter': 'or Damping Ratio', 'unit': '[%]', 'tolerance': '±10'},
#                         {'parameter': 'Time difference between peaks of Bank and Sideslip', 'unit': '[s]',
#                          'tolerance': '±1'},
#                         {'parameter': 'Non-periodic response', 'unit': '[-]', 'tolerance': 'Time history'}
#                     ],
# =============================================================================
                    'tolerances_evaluation_criteria': [
                        {'parameter': 'Airspeed', 'unit': '[kts]', 'tolerance': 'CT&M'},
                        {'parameter': 'Roll Rate', 'unit': '[deg/s]', 'tolerance': 'CT&M'},
                        {'parameter': 'Yaw Rate', 'unit': '[deg/s]', 'tolerance': 'CT&M'}
                    ],
		            'tolerances_recurrent_criteria': [
                        {'parameter': 'Airspeed', 'unit': '[kts]', 'tolerance': '±10'},
                        {'parameter': 'Roll Rate', 'unit': '[deg/s]', 'tolerance': '±5'},
                        {'parameter': 'Yaw Rate', 'unit': '[deg/s]', 'tolerance': '±4'}
                    ],
                    'add_plots' : [
                        {'parameter': 'Pitch Angle', 'unit': '[deg]'},
                        {'parameter': 'Bank Angle', 'unit': '[deg]'},
                        {'parameter': 'Heading', 'unit': '[deg]'},
                        {'parameter': 'Pitch Rate', 'unit': '[deg/s]'},
                        {'parameter': 'Engine 1 Torque', 'unit': '[%]'},
                        {'parameter': 'Engine 2 Torque', 'unit': '[%]'},
                        {'parameter': 'Sideslip Angle', 'unit': '[deg]'},
                        {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]'},
                        {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]'},
                        {'parameter': 'Pedals Pos.', 'unit': '[%]'},
                        {'parameter': 'Collective Pos.', 'unit': '[%]'}
                    ],
                    'test_cases': [
                        {
                            'id': 'A1',
                            'name': 'Lateral-Directional Oscillations',
                            'condition': 'Mid Speed - 66 KIAS, Left Pedal input',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Trim controls to reach 66 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.',
                                'When the test elapsed time is 3.0 seconds, perform a pedal control doublet. Return pedal controls position to initial position, and then keep hands-off controls.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'A2',
                            'name': 'Lateral-Directional Oscillations',
                            'condition': 'Mid Speed - 66 KIAS, Left Pedal input',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Trim controls to reach 67 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.',
                                'When the test elapsed time is 3.5 seconds, perform a pedal control doublet. Return pedal controls position to initial position, and then keep hands-off controls.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B1',
                            'name': 'Lateral-Directional Oscillations',
                            'condition': 'High Speed - 90 KIAS, Left Pedal input',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Trim controls to reach 90 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.',
                                'When the test elapsed time is 3.6 seconds, perform a pedal control doublet. Return pedal controls position to initial position, and then keep hands-off controls.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B2',
                            'name': 'Lateral-Directional Oscillations',
                            'condition': 'High Speed - 90 KIAS, Left Pedal input',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Trim controls to reach 90 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.',
                                'When the test elapsed time is 2.5 seconds, perform a pedal control doublet. Return pedal controls position to initial position, and then keep hands-off controls.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        }
                    ]
                },
                {
                    'id': 'd.3.ii',
                    'snapshot' : False,
                    'main_title': 'Dynamic Lateral and Directional Stability',
                    'test_title': 'Spiral Stability',
                    'objective': 'The objective of this test is to demonstrate that the FSTD spiral stability is compliant with the reference data.',
                    'tolerances_evaluation_criteria': [
                        {'parameter': 'Correct Trend on Bank', 'unit': '[deg]', 'tolerance': 'CT&M'}
                    ],
                    'tolerances_recurrent_criteria': [
                        {'parameter': 'Correct Trend on Bank', 'unit': '[deg]', 'tolerance': '±2'}
                    ],
                    'add_plots' : [
                        {'parameter': 'Airspeed', 'unit': '[kts]'},
                        {'parameter': 'Heading', 'unit': '[deg]'},
                        {'parameter': 'Sideslip Angle', 'unit': '[deg]'},
                        {'parameter': 'Pitch Angle', 'unit': '[deg]'},
                        {'parameter': 'Pitch Rate', 'unit': '[deg/s]'},
                        {'parameter': 'Roll Rate', 'unit': '[deg/s]'},
                        {'parameter': 'Yaw Rate', 'unit': '[deg/s]'},
                        {'parameter': 'Engine 1 Torque', 'unit': '[%]'},
                        {'parameter': 'Engine 2 Torque', 'unit': '[%]'},
                        {'parameter': 'Vertical Velocity', 'unit': '[ft/min]'},                      
                        {'parameter': 'Longitudinal Cyclic Pos.', 'unit': '[%]'},
                        {'parameter': 'Lateral Cyclic Pos.', 'unit': '[%]'},
                        {'parameter': 'Pedals Pos.', 'unit': '[%]'},
                        {'parameter': 'Collective Pos.', 'unit': '[%]'}
                    ],
                    'test_cases': [
                        {
                            'id': 'A1',
                            'name': 'Spiral Stability',
                            'condition': 'Right Input - 64 KIAS',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Trim controls to reach 64 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.',
                                'When the test elapsed time is 7.0 seconds, move lateral cyclic to reach 30.0 deg of positive bank angle in 18.0 seconds and maintain it, leaving collective control and pedals free.',
                                'When the test elapsed time is 36.0 seconds, release lateral cyclic.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'A2',
                            'name': 'Spiral Stability',
                            'condition': 'Right Input - 64 KIAS',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Set controls to reach target values.'
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B1',
                            'name': 'Spiral Stability',
                            'condition': 'Left Input - 63 KIAS',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Trim controls to reach 63 KIAS',
                                'Stabilize and maintain current flight condition.',
                                'Press "Enter" to start recording.',
                                'When the test elapsed time is 12.0 seconds, move lateral cyclic to reach 20.0 deg of negative bank angle in 10.0 seconds and maintain it, leaving collective control and pedals free.',
                                'When the test elapsed time is 44.0 seconds, release lateral cyclic.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        },
                        {
                            'id': 'B2',
                            'name': 'Spiral Stability',
                            'condition': 'Left Input - 64 KIAS',
                            'automatic_testing_possible': True,
                            'generic_flight_controls': [
                                {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                                {'fc': 'Lateral', 'status': 'MATH PILOT'},
                                {'fc': 'Collective', 'status': 'MATH PILOT'},
                                {'fc': 'Pedals', 'status': 'MATH PILOT'}
                            ],
                            'automatic_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Press "Start QTG" to start the test.',
                                'The generic flight controls will be internally controlled according to the following table:'
                            ],
                            'manual_testing': [
                                'On the left column double click on the corresponding test. The test will displayed in the right column.',
                                'Right click on the corresponding test in the right column to change in manual mode.',
                                'Press "Start QTG" to start the test.',
                                'In the text field below, enter the desired time for the test to run. Press "Enter".',
                                'Set controls to reach target values.'
                                'Press "Enter" to start recording.'
                            ],
                            'notes_rationales': {
                                'notes': ['No Notes related to the Test are present'],
                                'rationales_validation_data': ['No Rationales related to the Test are present'],
                                'rationales_results': ['No Rationales related to the Test are present']
                            }
                        }
                    ]
                }
            ]
        }
    ]
}

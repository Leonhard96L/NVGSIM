import json
import os
from datetime import datetime

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS


if __name__ == "__main__":
    from collections import defaultdict

    # Example data with detailed test cases
    data = [
        {
            "test": "1",
            "part": "a.3",
            "case": {
                'id': 'A1',
                'name': 'OEI continued take-off',
                'condition': 'OEI',
                'automatic_testing_possible': True,
                'generic_flight_controls': [
                    {'fc': 'Longitudinal', 'status': 'MATH PILOT'},
                    {'fc': 'Lateral', 'status': 'MATH PILOT'},
                    {'fc': 'Collective', 'status': 'MATH PILOT'}
                ]
            },
            "is_mqtg": True,
            "curr_date": "2024-09-01",
            "curr_time": "14:00",
            "plots_base64": "base64string1"
        },
        {
            "test": "1",
            "part": "a.3",
            "case": {
                'id': 'A2',
                'name': 'Autorotation descent',
                'condition': 'Power-off',
                'automatic_testing_possible': False,
                'generic_flight_controls': [
                    {'fc': 'Longitudinal', 'status': 'MANUAL PILOT'},
                    {'fc': 'Lateral', 'status': 'MANUAL PILOT'}
                ]
            },
            "is_mqtg": False,
            "curr_date": "2024-09-01",
            "curr_time": "14:30",
            "plots_base64": "base64string2"
        },
        {
            "test": "1",
            "part": "b.5",
            "case": {
                'id': 'B1',
                'name': 'Hover check',
                'condition': 'Hover',
                'automatic_testing_possible': True,
                'generic_flight_controls': [
                    {'fc': 'Yaw', 'status': 'MATH PILOT'}
                ]
            },
            "is_mqtg": True,
            "curr_date": "2024-09-02",
            "curr_time": "09:00",
            "plots_base64": "base64string3"
        }
    ]

    # Step 1: Create the structure to hold the grouped data
    grouped_data = {"tests": []}
    test_dict = defaultdict(lambda: {"test_parts": defaultdict(lambda: {"test_cases": []})})

    # Step 2: Populate the structure
    for item in data:
        test_id = item["test"]
        part_id = item["part"]
        test_case = item["case"]

        # Add additional metadata to the test case
        test_case.update({
            "is_mqtg": item["is_mqtg"],
            "curr_date": item["curr_date"],
            "curr_time": item["curr_time"],
            "plots_base64": item["plots_base64"]
        })

        # Organize test cases under their respective parts and tests
        test_dict[test_id]["test_parts"][part_id]["test_cases"].append(test_case)

    # Step 3: Convert defaultdict to normal dict and populate the grouped_data
    for test_id, test_content in test_dict.items():
        test_entry = {
            "id": test_id,
            "name": f"Test {test_id}",  # You can customize the name here if needed
            "test_parts": []
        }

        for part_id, part_content in test_content["test_parts"].items():
            test_part = {
                "id": part_id,
                "main_title": f"Main Title {part_id}",  # You can customize the title here if needed
                "test_title": f"Test Title {part_id}",  # You can customize the test title here if needed
                "test_cases": part_content["test_cases"]
            }
            test_entry["test_parts"].append(test_part)

        grouped_data["tests"].append(test_entry)

    # Now grouped_data holds the restructured data
    import pprint

    pprint.pprint(grouped_data)

    """
        -Ziel ist es  eine Funktion, bei welcher ich die Sektion eingebe und die Test-ID und es wird ein Report erstellt.
        -QTG_report(1.d, 1.d.A1) und es wird pro test ein eigener Report erstellt. Also ein Report Pro test.
        -Der erstellte Report muss manuell verändert werden können. Weil man da manchmal Sachen dazuschreiben muss, welche nicht automatisiert werden können
        -Automatic testing: N.A. Somit kann die Tabelle: Fligth Controls und Status auch weck. 
        -Manual testing, werde ich manuell schreiben:
        -Die Tabelle Tolerances and Evaluation Criteria FTD Level 3 and FNPT Level III: Kann man anlegen, kann aber Leer sein. Diese ist dann abhängig vom Test
        unterschiedlich lang. Somit ist es besser, wenn man diese Manuell macht. Aber statt FTD Level 3 and FNPT Level III kommt halt nur FTD Level 1 hin.
        -Die Tabelle Test Results brauchen wir zur Zeit nicht, diese kann also weck.
        -Lass mal die Tabelle (Test Results) weck.
        -Notes and Rationales kann man nur die Überschrift stehen lassen die Tabelle kann auch weck. Ich werde dann die Rationales unten Manuell dazuschreiben.
        -Wäre auch super wenn die Plots angehängt werden können.
        -Bitte bei der Tabelle "Initial Conditions" eine Spalte hinzufügen, wo die Einheiten drin stehen. Die selben Einheiten wie bei Reiser
        
        -Im untenstehenden dict, stehen alle Tests drinnen, also Test ID und Beschreibung. Diese sind 1 zu 1 aus dem MQTG von Reiser
    """

    test_ID_dict = {'1.a': 'Engine Assessment',
                    '1.a.2' : 'Power Turbine Speed Trim',
                    '1.a.2.A1': 'HI NR - OFF to ON',
                    '1.a.2.A2': 'HI NR - ON to OFF',
                    '1.a.3': 'Engine & Rotor Speed Governing',
                    '1.a.3.A1': '90 KIAS - Up Input, -1000 fpm',
                    '1.a.3.B1' : '60 KIAS - Down Input, AEO MCP',
                    '1.c' : 'Take-Off',
                    '1.c.1' : 'Take-off All engines',
                    '1.c.1.A1' : 'CAT A - Clear Helipad',
                    '1.c.2' : 'OEI continued take-off',
                    '1.c.2.A1' : 'OEI',
                    '1.d': 'Hover Performance',
                    '1.d.A1':'Light GW, Aft CG - 3 ft AGL',
                    '1.d.A2':'Light GW, Aft CG - 10 ft AGL',
                    '1.d.A3':'Light GW, Aft CG - 25 ft AGL',
                    '1.d.A4':'Light GW, Aft CG - 70 ft AGL',
                    '1.d.B1':'Heavy GW, Aft CG - 3 ft AGL',
                    '1.d.B2':'Heavy GW, Aft CG - 10 ft AGL',
                    '1.d.B3':'Heavy GW, Aft CG - 25 ft AGL',
                    '1.d.B4':'Heavy GW, Aft CG - 70 ft AGL',
                    '1.e':'Vertical Climb Performance',
                    '1.e.A1':'Light GW, Aft CG - AEO TOP',
                    '1.e.B1':'Heavy GW, Fwd CG - AEO MCP',
                    '1.f': 'Level Flight Performance and Trimmed Flight Control Position',
                    '1.f.A1' : 'Light GW, Aft CG - 64 KIAS',
                    '1.f.A2': 'Light GW, Aft CG - 130 KIAS',
                    '1.f.B1' : 'Heavy GW, Aft CG - 64 KIAS',
                    '1.f.B2': 'Heavy GW, Aft CG - 130 KIAS',
                    '1.g' : 'Climb Performance and Trimmed Flight Control Position',
                    '1.g.A1' : 'Light GW, Aft CG - AEO MCP, VY',
                    '1.g.A2' : 'Light GW, Aft CG - AEO TOP, VY',
                    '1.g.A3' : 'Light GW, Aft CG - OEI MCP, VY',
                    '1.g.A4' : 'Light GW, Aft CG - OEI 2 min, VTOSS',
                    '1.g.A5' : 'Light GW, Aft CG - OEI 30 s, VTOSS',
                    '1.g.B1' : 'Heavy GW, Fwd CG - AEO MCP, VY',
                    '1.g.B2' : 'Heavy GW, Fwd CG - AEO TOP, VY',
                    '1.g.B3' : 'Heavy GW, Fwd CG - OEI MCP, VY',
                    '1.g.B4' : 'Heavy GW, Fwd CG - OEI 2 min, VTOSS',
                    '1.g.B5' : 'Heavy GW, Fwd CG - OEI 30 s, VTOSS',
                    '1.h' : 'Descent',
                    '1.h.1' : 'Descent Performance and Trimmed Flight Control Position',
                    '1.h.1.A1' : 'Light GW, Aft CG - 90 KIAS, -1000 fpm',
                    '1.h.1.B1' : 'Heavy GW, Fwd CG - 90 KIAS, -1000 fpm',
                    '1.j' : 'Landing',
                    '1.j.1' : 'Landing - All Engines',
                    '1.j.1.A1' : 'CAT A - Clear Helipad',
                    '1.j.2' : 'Landing - One Engine Inoperative',
                    '1.j.2.A1' : 'OEI - CAT A Clear Helipad',
                    '1.j.2.A2' : 'OEI - CAT B',
                    '2.a' : 'Control System Mechanical Characteristics',
                    '2.a.1' : 'Cyclic Force vs Position',
                    '2.a.1.A1' : 'Longitudinal - Trim ON',
                    '2.a.1.A2' : 'Longitudinal - Trim OFF',
                    '2.a.1.B1' : 'Lateral - Trim ON',
                    '2.a.1.B2' : 'Lateral - Trim OFF',
                    '2.a.2' : 'Collective/Pedals Force vs Position',
                    '2.a.2.A1' : 'Collective - Trim ON',
                    '2.a.2.B1' : 'Pedals - Trim ON',    
                    '2.a.4' : 'Trim System Rate',
                    '2.a.4.A1' : 'Longitudinal Cyclic - ATRIM',
                    '2.a.4.B1' : 'Lateral Cyclic - ATRIM',
                    '2.c' : 'Longitudinal Handling Qualities',
                    '2.c.2' : 'Longitudinal Static Stability',
                    '2.c.2.A1' : 'Cruise, Trim Speed UP - 120 KIAS, Trim Speed',
                    '2.c.2.A2' : 'Cruise, Trim Speed UP - 125 KIAS',
                    '2.c.2.A3' : 'Cruise, Trim Speed UP - 130 KIAS',
                    '2.c.2.B1' : 'Cruise, Trim Speed DOWN - 120 KIAS, Trim Speed',
                    '2.c.2.B2' : 'Cruise, Trim Speed DOWN - 115 KIAS',
                    '2.c.2.B3' : 'Cruise, Trim Speed DOWN - 110 KIAS',
                    '2.c.2.C1' : 'Autorotation, Trim Speed UP - 75 KIAS, Trim Speed',
                    '2.c.2.C2' : 'Autorotation, Trim Speed UP - 85 KIAS',
                    '2.c.2.C3' : 'Autorotation, Trim Speed UP - 90 KIAS',
                    '2.c.2.D1' : 'Autorotation, Trim Speed DOWN - 75 KIAS, Trim Speed',
                    '2.c.2.D2' : 'Autorotation, Trim Speed DOWN - 65 KIAS',
                    '2.c.2.D3' : 'Autorotation, Trim Speed DOWN - 55 KIAS',
                    '2.c.4' : 'Manoeuvring Stability',
                    '2.c.4.A1' : 'Right Turn, Mid Speed - Vy, 0 Bank',
                    '2.c.4.A2' : 'Right Turn, Mid Speed - Vy, 30 Bank',
                    '2.c.4.A3' : 'Right Turn, Mid Speed - Vy, 45 Bank',
                    '2.c.4.B1' : 'Left Turn, Mid Speed - Vy, 0 Bank',
                    '2.c.4.B2' : 'Left Turn, Mid Speed - Vy, 30 Bank',
                    '2.c.4.B3' : 'Left Turn, Mid Speed - Vy, 45 Bank',
                    '2.c.4.C1' : 'Right Turn, High Speed - 120 KIAS, 0 Bank',
                    '2.c.4.C2' : 'Right Turn, High Speed - 120 KIAS, 30 Bank',
                    '2.c.4.C3' : 'Right Turn, High Speed - 120 KIAS, 45 Bank',
                    '2.c.4.D1' : 'Left Turn, High Speed - 120 KIAS, 0 Bank',
                    '2.c.4.D2' : 'Left Turn, High Speed - 120 KIAS, 30 Bank',
                    '2.c.4.D3' : 'Left Turn, High Speed - 120 KIAS, 45 Bank',
                    '2.d' : 'Lateral & Directional Handling Qualities',
                    '2.d.2' : 'Directional Static Stability',
                    '2.d.2.A1' : 'Mid Speed, DSAS - 100 KIAS, Trim',
                    '2.d.2.A2' : 'Mid Speed, DSAS - 100 KIAS, Right Sideslip 1',
                    '2.d.2.A3' : 'Mid Speed, DSAS - 100 KIAS, Right Sideslip 2',
                    '2.d.2.B1' : 'Mid Speed, AFCS OFF - 100 KIAS, Trim',
                    '2.d.2.B2' : 'Mid Speed, AFCS OFF - 100 KIAS, Left Sideslip 1',
                    '2.d.2.B3' : 'Mid Speed, AFCS OFF - 100 KIAS, Left Sideslip 2',
                    '2.d.3' : 'Dynamic Lateral and Directional Stability',
                    '2.d.3.i' : 'Lateral-Directional Oscillations',
                    '2.d.3.i.A1' : 'Mid Speed - Vy, DSAS, Left Pedal input ',
                    '2.d.3.i.A2' : 'Mid Speed - Vy, AFCS OFF, Left Pedal input ',
                    '2.d.3.i.B1' : 'High Speed - 90 KIAS, DSAS, Left Pedal input',
                    '2.d.3.i.B2' : 'High Speed - 90 KIAS, AFCS OFF, Left Pedal input',
                    '2.d.3.ii' : 'Spiral Stability',
                    '2.d.3.ii.A1' : 'Right Input - Vy, DSAS',
                    '2.d.3.ii.A2' : 'Right Input - Vy, AFCS OFF',
                    '2.d.3.ii.B1' : 'Left Input - Vy, DSAS',
                    '2.d.3.ii.B2' : 'Left Input - Vy, AFCS OFF'
                    }




    #Take-off
    d1c1A1 = " Take Off-All Engines-CAT A on Runway"                        #1
    d1c2A1 = " Take Off-OEI CAT A on Runway"                                #2
    
    #Hover Performance
    sec1d = " Hover Performance" 
    d1d1A1 = " Light GW, Aft CG - 3 ft AGL"                                            
    d1d1A2 = " Light GW, Aft CG - 10 ft AGLL"
    d1d1A3 = " Light GW, Aft CG - 25 ft AGL" 
    d1d1A4 = " Light GW, Aft CG - 70 ft AGL" 
    d1d1B1 = " Heavy GW - 3ft AGL"
    d1d1B2 = " Heavy GW - 10ft AGL"
    d1d1B3 = " Heavy GW - 25ft AGL" 
    d1d1B4 = " Heavy GW - 70ft AGL" 
    
    #Vertical climb Performance
    d1e1A1 = " Light GW - AEO TOP"
    d1e1B1 = " Heavy GW - AEO MCP"
    
    #Level flight  Performance and Trimmed Flight Condition
    #Info:
    #VH Maximum speed in level flight at maximum continuous power.
    d1f1A1 = " Light GW - VY"
    d1f1A2 = " Light GW - VH"
    d1f1B1 = " Heavy GW - VY"
    d1f1B2 = " Heavy GW - VH"
    
    
    #Climb Performance and Trimmed Flight Control Position 
    #Info:
    #MCP = Maximum continuous power
    #TOP = Take off Power
    d1g1A1 =  " Light GW - AEO MCP VY"
    d1g1A2 =  " Light GW - AEO TOP VY"
    d1g1A3 =  " Light GW - OEI MCP VY"
    d1g1A4 =  " Light GW - OEI 2MIN VTOSS"
    d1g1B1 =  " Heavy GW - AEO MCP VY"
    d1g1B2 =  " Heavy GW - AEO TOP VY"
    d1g1B3 =  " Heavy GW - OEI MCP VY"
    d1g1B4 =  " Heavy GW - OEI 2MIN VTOSS"
    
    #Descent Performance and Trimmed Flight Control Position
    d1h1A1 = " Light GW - 90KIAS -1000fpm"
    d1h1B1 = " Heavy GW - 90KIAS -1000fpm"
    
    #Landing
    d1j1A1 = " Landing - All Enignes CAT A"
    
    d1j2A1 = " OEI TM - CAT A"
    d1j2A2 = " OEI TM - CAT B"
    
    ##Handling Qualities
    
    #Cycliv Force vs Position
    d2a1A1 = " Cyclic Longitudinal - Trim ON"
    d2a1A2 = " Cyclic Longitudinal - Trim OFF"
    d2a1B1 = " Cyclic Lateral - Trim ON"
    d2a1B2 = " Cyclic Lateral - Trim OFF"
    
    #Collective/Pedals Force vs Position
    d2a2A1 = " Collective - Trim ON"
    d2a2B1 = " Pedals - Trim ON"
    
    #Trim System Rate
    d2a4A1 = " Longitudinal Cyclic - ATRIM"
    d2a4B1 = " Lateral Cyclic - ATRIM"
    
    #Longitudinal Static Stability
    d2c2A1 = " Cruise Trim Speed Up - 120 KIAS, Trim Speed"
    d2c2A2 = " Cruise Trim Speed Up - 125 KIAS"
    d2c2A3 = " Cruise Trim Speed Up - 130 KIAS"
    d2c2B1 = " Cruise Trim Speed Down - 120 KIAS, Trim Speed"
    d2c2B2 = " Cruise Trim Speed Down - 115 KIAS"
    d2c2B3 = " Cruise Trim Speed Down - 110 KIAS"
    d2c2C1 = " Autorotation Trim Speed Up - 75 KIAS, Trim Speed"
    d2c2C2 = " Autorotation Trim Speed Up - 85 KIAS"
    d2c2C3 = " Autorotation Trim Speed Up - 90 KIAS"   
    d2c2D1 = " Autorotation Trim Speed Up - 75 KIAS, Trim Speed"
    d2c2D2 = " Autorotation Trim Speed Up - 65 KIAS"
    d2c2D3 = " Autorotation Trim Speed Up - 55 KIAS"    
    
    #Manoeuvring Stability
    d2c4A1 = " Right Turn, Vy, 0 Bank"
    d2c4A2 = " Right Turn, Vy, 30 Bank"
    d2c4A3 = " Right Turn, Vy, 45 Bank"
    d2c4B1 = " Left Turn, Vy, 0 Bank"
    d2c4B2 = " Left Turn, Vy, 30 Bank"
    d2c4B3 = " Left Turn, Vy, 45 Bank"
    d2c4C1 = " Right Turn, 120 KIAS, 0 Bank"
    d2c4C2 = " Right Turn, 120 KIAS, 30 Bank"
    d2c4C3 = " Right Turn, 120 KIAS, 45 Bank"   
    d2c4D1 = " Left Turn, 120 KIAS, 0 Bank"
    d2c4D2 = " Left Turn, 120 KIAS, 30 Bank"
    d2c4D3 = " Left Turn, 120 KIAS, 45 Bank"   
    
    #Diractional static stability
    d2d2A1 = " Mid Speed, 100 KIAS"
    d2d2A2 = " Mid Speed, 100 KIAS Right Sideslip 1"
    d2d2A3 = " Mid Speed, 100 KIAS Right Sideslip 2"
    d2d2B1 = " Mid Speed, 100 KIAS"
    d2d2B2 = " Mid Speed, 100 KIAS Left Sideslip 1"
    d2d2B3 = " Mid Speed, 100 KIAS Left Sideslip 2"
    
    #Lateral directional oscillations
    d2d3iA1 = " Mid Speed Vy, DSAS, Left Pedal input"
    d2d3iA2 = " Mid Speed Vy, AFCS OFF, Left Pedal input"
    d2d3iB1 = " High Speed 90 KIAS, DSAS, Left Pedal input"
    d2d3iB2 = " High Speed 90, AFCS OFF, Left Pedal input"
    
    #Spiral Stability
    d2d3iiA1 = " Right Input, Vy, DSAS"
    d2d3iiA2 = " Right Input, Vy, AFCS OFF"
    d2d3iiB1 = " Left Input, Vy, DSAS"
    d2d3iiB2 = " Left Input, Vy, AFCS OFF"   







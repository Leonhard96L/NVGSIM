import json
import os
from datetime import datetime

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS


def load_json_data(qtg_path):
    for dirpath, dirnames, filenames in os.walk(qtg_path):
        init_cond = None
        ref_init_cond = None

        for file in filenames:
            if 'FTD1_log_init_cond' in file:
                file_path = os.path.join(dirpath, file)
                with open(file_path, 'r') as json_file:
                    init_cond = json.load(json_file)
            if 'Reference_init_cond' in file:
                print(file)
                file_path = os.path.join(dirpath, file)
                with open(file_path, 'r') as json_file:
                    ref_init_cond = json.load(json_file)

    # print(init_cond)
    # print(ref_init_cond)
    return init_cond, ref_init_cond


def process_data(ref_init_cond, init_cond):
    # Get the current date and time
    now = datetime.now()

    # Format the date as mm.dd.yyyy
    formatted_date = now.strftime("%m.%d.%Y")

    # Format the time as hh:mm:ss
    formatted_time = now.strftime("%H:%M:%S")

    data = {
        "test": "hi leo",
        "title": "QTG Document",
        "curr_date": formatted_date,
        "curr_time": formatted_time,
        "headers": ["Parameter [UoM]", "Reference*", "FSTD"],
        "subsections": []
    }

    # Initialize subsection titles
    mass_properties = {"title": "Mass Properties", "rows": []}
    environment_parameters = {"title": "Environment Parameters", "rows": []}
    flight_parameters = {"title": "Flight Parameters", "rows": []}

    current_subsection = mass_properties

    for key in ref_init_cond:
        current_row = [key, ref_init_cond[key], init_cond.get(key, ""), ""]
        current_subsection["rows"].append(current_row)

        if key == "Moment of Inertia ZZ":
            data["subsections"].append(current_subsection)
            current_subsection = environment_parameters
        elif key == "Wind Speed":
            data["subsections"].append(current_subsection)
            current_subsection = flight_parameters

    # Append the last category
    data["subsections"].append(current_subsection)

    return data


def create_pdf(data, output_file):
    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('./templates'))
    template = env.get_template('test.html')

    # Render the HTML template with data
    html_out = template.render(data)
    css_path = './templates/style.css'
    # Convert the rendered HTML to PDF
    HTML(string=html_out).write_pdf(output_file, stylesheets=[CSS(css_path)])


# Generate the PDF
if __name__ == "__main__":
    init_cond, ref_init_cond = load_json_data("./data")
    data = process_data(ref_init_cond, init_cond)
    create_pdf(data, "output.pdf")

    
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







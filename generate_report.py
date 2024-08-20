import base64
import io
import json
import os
from datetime import datetime

import numpy as np
from jinja2 import Environment, FileSystemLoader
from matplotlib import pyplot as plt
from weasyprint import HTML, CSS
# from PyPDF2 import PdfMerger
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

from function_lib import *


# import matplotlib.pyplot as plt

# from Init_flyout import *


# from html2docx import html2docx
# from docx import Document


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


def process_data(ref_init_cond, init_cond, plot_base64):
    # Get the current date and time
    now = datetime.now()

    # Format the date as mm.dd.yyyy
    formatted_date = now.strftime("%m.%d.%Y")

    # Format the time as hh:mm:ss
    formatted_time = now.strftime("%H:%M:%S")

    # CHANGE FOR EACH TEST HERE:
    test_id = "1.d"

    sub_case_ids = [key for key in test_ID_dict.keys() if test_id in key]

    data = {
        "title": test_id + " " + test_ID_dict.get(test_id),
        "test_objective": "The objective of this test is to demonstrate that the FSTD hover performance is compliant with the helicopter reference data.",
        "headers": ["Parameter [UoM]", "Reference*", "FSTD"],
        # everything below is automatically generated!
        "test_id": test_id,
        "test_name": test_ID_dict.get(test_id),
        "sub_cases": [{"id": key, "name": test_ID_dict.get(key), "short_id": key[len(test_id)+1:]} for key in sub_case_ids],
        "subsections": [],
        "curr_date": formatted_date,
        "curr_time": formatted_time,
        "plots_base64": plot_base64
    }

    print(plot_base64[0])

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
    # with open("my.html") as fp:
    #     html = fp.read()
    #
    # # html2docx() returns an io.BytesIO() object. The HTML must be valid.
    # buf = html2docx(html_out, title="My Document", )
    #
    # with open("output.docx", "wb") as fp:
    #     fp.write(buf.getvalue())


def create_plots(QTG_path):
    plot_paths = []
    for dirpath, dirnames, filenames in os.walk(QTG_path):
        for file in filenames:
            if not file.endswith('.sim'):
                continue

            file_path = os.path.join(dirpath, file)

            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
            if 'FTD1' in data.keys():
                plot_title = file.split('.')[0]

                x_Ref = data['Storage'][0]['x']
                y_Ref = data['Storage'][0]['y']
                x = data['FTD1']['x']
                y = data['FTD1']['y']

                y[-1] = y[-2]

                x_label = 'Time(s)'

                # Korrektur mit richitgen Einheiten
                plt.figure(figsize=(10, 6))
                if 'Angle' in plot_title:
                    img_name = f"7_{plot_title}.png"
                    y = np.rad2deg(y)
                    y_label = plot_title + ' (deg)'
                    if 'Angle Rate' in plot_title:
                        img_name = f"9_{plot_title}.png"
                        y_label = plot_title + ' (deg/s)'
                    if 'Yaw Angle Unwrapped' in plot_title:
                        y = [map360(i) for i in y]
                        plot_title = 'Heading'
                        img_name = f"7_{plot_title}.png"
                        y_label = plot_title + ' (deg)'
                elif 'Control Position' in plot_title:
                    if 'Control Position Pitch' in plot_title:  # Pitch position Signal ist bei der Referenz invertiert
                        y = [i * -1 for i in y]
                    img_name = f"8_{plot_title}.png"
                    y = [map_control(i) for i in y]
                    y_label = plot_title + ' (%)'
                elif 'TRQ' in plot_title:
                    img_name = f"5_{plot_title}.png"
                    y_label = plot_title + ' (%)'
                elif 'Control QTG Force Pitch' in plot_title:
                    y = pitch_roll_brun2N(y)
                    x = pitch_brun2angle(x)
                    img_name = f"10_{plot_title}.png"
                    y_label = 'Force Pitch (N)'
                    x_label = 'Position (deg)'
                elif 'Control QTG Force Roll' in plot_title:
                    y = pitch_roll_brun2N(y)
                    x = roll_brun2angle(x)
                    img_name = f"10_{plot_title}.png"
                    y_label = 'Force Roll (N)'
                    x_label = 'Position (deg)'
                elif 'Control QTG Force Collective' in plot_title:
                    y = coll_brun2N(y)
                    x = coll_brun2angle(x)
                    img_name = f"10_{plot_title}.png"
                    y_label = 'Force Collective (N)'
                    x_label = 'Position (deg)'
                elif 'Control QTG Force Yaw' in plot_title:
                    x = yaw_brun2angle(x)
                    img_name = f"10_{plot_title}.png"
                    y_label = 'Force Yaw (N)'
                    x_label = 'Position (deg)'
                elif 'Groundspeed' in plot_title:
                    img_name = f"2_{plot_title}.png"
                    y = [mps2kt(i) for i in y]
                    y_label = plot_title + ' (kt)'
                elif 'Airspeed' in plot_title:
                    img_name = f"1_{plot_title}.png"
                    y = [mps2kt(i) for i in y]
                    y_label = plot_title + ' (kt)'
                elif 'RadarAltitude' in plot_title:
                    img_name = f"3_{plot_title}.png"
                    y_label = plot_title + ' (ft)'
                elif 'Barometric Altitude' in plot_title:
                    img_name = f"3_{plot_title}.png"
                    y = [m2ft(i) for i in y]
                    y_label = plot_title + ' (ft)'
                elif 'Vertical' in plot_title:
                    img_name = f"4_{plot_title}.png"
                    y = [mps2fpm(-i) for i in y]
                    y_label = plot_title + ' (ft/min)'
                elif 'Rotor' in plot_title:
                    img_name = f"6_{plot_title}.png"
                    y = [rpm2perc(i) for i in y]
                    y_label = plot_title + ' (%)'
                else:
                    y_label = plot_title + ' (??)'
                    img_name = f"{plot_title}.png"

                plt.plot(x_Ref, y_Ref, label='Reference')
                plt.plot(x, y, label='FTD1')

                # Section for scale
                sc_fac = 1.5
                plt.autoscale()
                y_min, y_max = plt.ylim()
                y_range = y_max - y_min
                plt.ylim(y_min - y_range * sc_fac, y_max + y_range * sc_fac)

                plt.xlabel(x_label)
                plt.ylabel(y_label)
                plt.title(plot_title)
                plt.legend()
                plt.grid(True)
                # plt.show()
                save_path = os.path.join(dirpath, img_name)

                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                plt.savefig(save_path, format='png')
                plt.close()
                print(plot_title + '.png created')

                img_data = buffer.getvalue()
                plot_paths.append(base64.b64encode(img_data).decode('utf-8'))

    return plot_paths


# Generate the PDF
if __name__ == "__main__":
    # 1. einen, mehrerer oder alle tests
    # 2. einen oder mehrere test cases
    print("MQTG Automatic Creator")
    create_init_cond = input("Create Initial QTG? (y/n): ").strip().lower() == 'y'
    test_name = input("Enter Test (leave empty to create all): ")
    test_case_name = ""
    if len(test_name) != 0: test_case_name = input("Enter Test Case (leave empty to create all test cases of a test): ")

    print(f"Create Initial QTG: {create_init_cond}")
    print(f"Test: {test_name}")
    print(f"Test Case: {test_case_name}")
    input()

    init_cond, ref_init_cond = load_json_data("./data")
    plots_base64 = create_plots("./data")
    # print(plots_base64)
    data = process_data(ref_init_cond, init_cond, plots_base64)
    create_pdf(data, "output.pdf")

import base64
import io
import json
import os
import re
from datetime import datetime

import numpy as np
from jinja2 import Environment, FileSystemLoader
from matplotlib import pyplot as plt
from weasyprint import HTML, CSS
# from PyPDF2 import PdfMerger
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

from function_lib import *
from qtg_data_structure import data as qtg_structure


# import matplotlib.pyplot as plt

# from Init_flyout import *


# from html2docx import html2docx
# from docx import Document


def load_json_data(qtg_path):
    file_path = os.path.join(qtg_path, 'init_conditions.json')
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

        init_cond_rec = data.get("Init_condition_Reccurent"),
        init_cond_ref = data.get("Init_condition_Reference"),
        init_cond_mqtg = data.get("Init_condition_MQTG"),

        print(init_cond_rec)
        print(init_cond_ref)
        print(init_cond_mqtg)
        return init_cond_rec, init_cond_ref, init_cond_mqtg


def process_test_case_data(test_item, init_cond_ref, init_cond_rec, init_cond_mqtg, plot_base64, date_time):
    def split_string(s):
        # Find the positions of the first and last dots
        first_dot = s.find('.')
        last_dot = s.rfind('_')

        # Split the string based on the dot positions
        test_id = s[:first_dot]
        part_id = s[first_dot + 1:last_dot]
        case_id = s[last_dot + 1:]
        return test_id, part_id, case_id

    test_id, part_id, case_id = split_string(test_item['id'])
    # 1.c.1_A1
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

    test, part, case = get_test_test_part_test_case(qtg_structure['tests'], test_id, part_id, case_id)

    print(test['tolerances_recurrent_criteria'])

    # Format the date as mm.dd.yyyy
    formatted_date = date_time.strftime("%m.%d.%Y")

    # Format the time as hh:mm:ss
    formatted_time = date_time.strftime("%H:%M:%S")

    # CHANGE FOR EACH TEST HERE:
    # test_id = "1.d"

    # sub_case_ids = [key for key in test_ID_dict.keys() if test_id in key]

    data = {
        "test": test,
        "part": part,
        "case": case,
        # "title": test_item['full_name'],
        # "test_objective": "The objective of this test is to demonstrate that the FSTD hover performance is compliant with the helicopter reference data.",
        # "headers": ["Parameter [UoM]", "Reference*", "FSTD"],
        # # everything below is automatically generated!
        # "test_id": test_item['id'],
        # "test_name": test_ID_dict.get(test_id),
        # "sub_cases": [{"id": key, "name": test_ID_dict.get(key), "short_id": key[len(test_id)+1:]} for key in sub_case_ids],
        # "subsections": [],
        "curr_date": formatted_date,
        "curr_time": formatted_time,
        "plots_base64": plot_base64
    }

    # print(plot_base64[0])

    # Initialize subsection titles
    mass_properties = {"title": "Mass Properties", "rows": []}
    environment_parameters = {"title": "Environment Parameters", "rows": []}
    flight_parameters = {"title": "Flight Parameters", "rows": []}

    # current_subsection = mass_properties
    #
    # for key in init_cond_ref:
    #     current_row = [key, init_cond_ref[key], init_cond_rec.get(key, ""), ""]
    #     current_subsection["rows"].append(current_row)
    #
    #     if key == "Moment of Inertia ZZ":
    #         data["subsections"].append(current_subsection)
    #         current_subsection = environment_parameters
    #     elif key == "Wind Speed":
    #         data["subsections"].append(current_subsection)
    #         current_subsection = flight_parameters
    #
    # # Append the last category
    # data["subsections"].append(current_subsection)

    return data


def create_test_case_pdf(data, output_file):
    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('./templates'))
    template = env.get_template('test_case.html')

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


# load plots instead of creating them.
def load_plots(qtg_path):
    plot_paths = []

    # Get a sorted list of all .png files in the directory
    image_files = sorted([f for f in os.listdir(qtg_path) if f.endswith('.png')])

    # Loop through all files in the directory
    for file_name in image_files:
        file_path = os.path.join(qtg_path, file_name)

        # Open the image file in binary mode
        with open(file_path, 'rb') as img_file:
            print(file_path)
            img_data = img_file.read()
            # Convert the image to Base64 and add it to the list
            base64_image = base64.b64encode(img_data).decode('utf-8')
            plot_paths.append(base64_image)
            # print(base64_image)

    return plot_paths


# deprecated
# def create_plots(QTG_path):
#     plot_paths = []
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
#
#                 y[-1] = y[-2]
#
#                 x_label = 'Time(s)'
#
#                 # Korrektur mit richitgen Einheiten
#                 plt.figure(figsize=(10, 6))
#                 if 'Angle' in plot_title:
#                     img_name = f"7_{plot_title}.png"
#                     y = np.rad2deg(y)
#                     y_label = plot_title + ' (deg)'
#                     if 'Angle Rate' in plot_title:
#                         img_name = f"9_{plot_title}.png"
#                         y_label = plot_title + ' (deg/s)'
#                     if 'Yaw Angle Unwrapped' in plot_title:
#                         y = [map360(i) for i in y]
#                         plot_title = 'Heading'
#                         img_name = f"7_{plot_title}.png"
#                         y_label = plot_title + ' (deg)'
#                 elif 'Control Position' in plot_title:
#                     if 'Control Position Pitch' in plot_title:  # Pitch position Signal ist bei der Referenz invertiert
#                         y = [i * -1 for i in y]
#                     img_name = f"8_{plot_title}.png"
#                     y = [map_control(i) for i in y]
#                     y_label = plot_title + ' (%)'
#                 elif 'TRQ' in plot_title:
#                     img_name = f"5_{plot_title}.png"
#                     y_label = plot_title + ' (%)'
#                 elif 'Control QTG Force Pitch' in plot_title:
#                     y = pitch_roll_brun2N(y)
#                     x = pitch_brun2angle(x)
#                     img_name = f"10_{plot_title}.png"
#                     y_label = 'Force Pitch (N)'
#                     x_label = 'Position (deg)'
#                 elif 'Control QTG Force Roll' in plot_title:
#                     y = pitch_roll_brun2N(y)
#                     x = roll_brun2angle(x)
#                     img_name = f"10_{plot_title}.png"
#                     y_label = 'Force Roll (N)'
#                     x_label = 'Position (deg)'
#                 elif 'Control QTG Force Collective' in plot_title:
#                     y = coll_brun2N(y)
#                     x = coll_brun2angle(x)
#                     img_name = f"10_{plot_title}.png"
#                     y_label = 'Force Collective (N)'
#                     x_label = 'Position (deg)'
#                 elif 'Control QTG Force Yaw' in plot_title:
#                     x = yaw_brun2angle(x)
#                     img_name = f"10_{plot_title}.png"
#                     y_label = 'Force Yaw (N)'
#                     x_label = 'Position (deg)'
#                 elif 'Groundspeed' in plot_title:
#                     img_name = f"2_{plot_title}.png"
#                     y = [mps2kt(i) for i in y]
#                     y_label = plot_title + ' (kt)'
#                 elif 'Airspeed' in plot_title:
#                     img_name = f"1_{plot_title}.png"
#                     y = [mps2kt(i) for i in y]
#                     y_label = plot_title + ' (kt)'
#                 elif 'RadarAltitude' in plot_title:
#                     img_name = f"3_{plot_title}.png"
#                     y_label = plot_title + ' (ft)'
#                 elif 'Barometric Altitude' in plot_title:
#                     img_name = f"3_{plot_title}.png"
#                     y = [m2ft(i) for i in y]
#                     y_label = plot_title + ' (ft)'
#                 elif 'Vertical' in plot_title:
#                     img_name = f"4_{plot_title}.png"
#                     y = [mps2fpm(-i) for i in y]
#                     y_label = plot_title + ' (ft/min)'
#                 elif 'Rotor' in plot_title:
#                     img_name = f"6_{plot_title}.png"
#                     y = [rpm2perc(i) for i in y]
#                     y_label = plot_title + ' (%)'
#                 else:
#                     y_label = plot_title + ' (??)'
#                     img_name = f"{plot_title}.png"
#
#                 plt.plot(x_Ref, y_Ref, label='Reference')
#                 plt.plot(x, y, label='FTD1')
#
#                 # Section for scale
#                 sc_fac = 1.5
#                 plt.autoscale()
#                 y_min, y_max = plt.ylim()
#                 y_range = y_max - y_min
#                 plt.ylim(y_min - y_range * sc_fac, y_max + y_range * sc_fac)
#
#                 plt.xlabel(x_label)
#                 plt.ylabel(y_label)
#                 plt.title(plot_title)
#                 plt.legend()
#                 plt.grid(True)
#                 # plt.show()
#                 save_path = os.path.join(dirpath, img_name)
#
#                 buffer = io.BytesIO()
#                 plt.savefig(buffer, format='png')
#                 plt.savefig(save_path, format='png')
#                 plt.close()
#                 print(plot_title + '.png created')
#
#                 img_data = buffer.getvalue()
#                 plot_paths.append(base64.b64encode(img_data).decode('utf-8'))
#
#     return plot_paths


def main(test_item, test_dir, date_time, gui_output, is_mqtg=False):
    # make pdf for each test, merge them into one document. check
    init_cond_rec, init_cond_ref, init_cond_mqtg = load_json_data(test_dir)

    # load existing images
    plots_base64 = load_plots(test_dir)
    data = process_test_case_data(test_item, init_cond_ref, init_cond_rec, init_cond_mqtg, plots_base64, date_time)
    gui_output("Creating Reports. This may take a second...")
    create_test_case_pdf(data, "output2.pdf")
    gui_output("Done creating Reports.")


# Generate the PDF
if __name__ == "__main__":
    # 1. einen, mehrerer oder alle tests
    # 2. einen oder mehrere test cases
    print("MQTG PDF Creator")
    create_init_cond = input("Create Initial QTG? (y/n): ").strip().lower() == 'y'
    test_name = input("Enter Test (leave empty to create all): ")
    test_case_name = ""
    if len(test_name) != 0:
        test_case_name = input("Enter Test Case (leave empty to create all test cases of a test): ")

    print(f"Create Initial QTG: {create_init_cond}")
    print(f"Test: {test_name}")
    print(f"Test Case: {test_case_name}")
    input()

    main("./data")



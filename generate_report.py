import base64
import copy
import json
import os

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
# from PyPDF2 import PdfMerger

from qtg_data_structure import data as qtg_structure


# import matplotlib.pyplot as plt

# from Init_flyout import *


# from html2docx import html2docx
# from docx import Document


def load_json_data(qtg_path):
    file_path = os.path.join(qtg_path, 'init_conditions.json')
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

        (init_cond_rec,) = data.get("Init_condition_Reccurent"),
        (init_cond_ref,) = data.get("Init_condition_Reference"),
        (init_cond_mqtg,) = data.get("Init_condition_MQTG"),

        print(init_cond_rec)
        print(init_cond_ref)
        print(init_cond_mqtg)
        return init_cond_rec, init_cond_ref, init_cond_mqtg


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
def get_test_test_part_test_case(tests, test_id, part_id, case_id):
    # Find the test with the given id
    test = next((test for test in tests if test['id'] == test_id), None)

    if test:
        # Find the test part with the given id within the found test
        test_part = next((part for part in test.get('test_parts', []) if part['id'] == part_id), None)

        if test_part:
            # Find the test case with the given id within the found test part
            test_case = next((case for case in test_part.get('test_cases', []) if case['id'] == case_id), None)

            # Clean up the test_parts list within the test
            test['test_parts'] = [test_part]
            # Clean up the test_cases list within the test_part
            test_part['test_cases'] = [test_case]

            return test, test_part, test_case

    # Return the cleaned list of tests with None values for test, test_part, and test_case if not found
    return None, None, None


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


def get_initial_conditions(case, init_cond_ref, init_cond_mqtg, init_cond_rec, is_mqtg):
    # Unit mappings
    units_map = {
        "Gross Weight": "kg",
        "Fuel Weigth": "kg",
        "CG Longitudinal": "mm",
        "CG Lateral": "mm",
        "Moment of Inertia XX": "kgm²",
        "Moment of Inertia XZ": "kgm²",
        "Moment of Inertia YY": "kgm²",
        "Moment of Inertia ZZ": "kgm²",
        "Pressure Altitude": "ft",
        "OAT": "degC",
        "Wind Direction": "deg",
        "Wind Speed": "kts",
        "Airspeed": "kts",
        "Ground Speed": "kts",
        "Vertical Velocity": "ft/min",
        "Radar Altitude": "ft",
        "Rotor Speed": "%",
        "Engine 1 Torque": "%",
        "Engine 2 Torque": "%",
        "Pitch Angle": "deg",
        "Bank Angle": "deg",
        "Heading": "deg",
        "Pitch Rate": "deg/s",
        "Roll Rate": "deg/s",
        "Yaw Rate": "deg/s",
        "X Body Acceleration": "m/s²",
        "Y Body Acceleration": "m/s²",
        "Z Body Acceleration": "m/s²",
        "Longitudinal Cyclic Pos.": "%",
        "Lateral Cyclic Pos.": "%",
        "Pedals Pos.": "%",
        "Collective Pos.": "%",
        "Engine 1 Main Switch": "−",
        "Engine 2 Main Switch": "−",
        "AFCS State": "−",
        "HINR Button": "−",
        "Training Mode": "−"
    }

    # Keys to categorize each section
    mass_properties_keys = [
        "Gross Weight", "Fuel Weigth", "CG Longitudinal", "CG Lateral", "Moment of Inertia XX", "Moment of Inertia XZ",
        "Moment of Inertia YY", "Moment of Inertia ZZ"
    ]
    environment_parameters_keys = [
        "Pressure Altitude", "OAT", "Wind Direction", "Wind Speed"
    ]
    flight_parameters_keys = [
        "Airspeed", "Ground Speed", "Vertical Velocity", "Radar Altitude", "Rotor Speed", "Engine 1 Torque",
        "Engine 2 Torque", "Pitch Angle", "Bank Angle", "Heading", "Pitch Rate", "Roll Rate", "Yaw Rate",
        "X Body Acceleration", "Y Body Acceleration", "Z Body Acceleration", "Longitudinal Cyclic Pos.",
        "Lateral Cyclic Pos.", "Pedals Pos.", "Collective Pos.", "Engine 1 Main Switch", "Engine 2 Main Switch",
        "AFCS State", "HINR Button", "Training Mode"
    ]

    # Define key mappings for each category
    def process_condition(ptr_dict, condition_data, keys_map, sub_category):
        # Process each key-value pair
        for key, value in condition_data.items():
            key_with_unit = f"{key} [{units_map.get(key, 'N/A')}]"

            # Update or initialize the dictionary entry for the key
            for category, keys in keys_map.items():
                if key in keys:
                    # Ensure that the category dictionary exists in the main dictionary
                    if key_with_unit not in ptr_dict[category]:
                        ptr_dict[category][key_with_unit] = {}

                    # Update the value for the sub-category
                    ptr_dict[category][key_with_unit][sub_category] = value

    # Example initialization
    case["init_conds"] = {
        "mass_properties": {},
        "environment_parameters": {},
        "flight_parameters": {}
    }

    # Define key mappings for each category
    keys_map = {
        'mass_properties': mass_properties_keys,
        'environment_parameters': environment_parameters_keys,
        'flight_parameters': flight_parameters_keys
    }

    # Process each condition and populate the corresponding sub-categories
    process_condition(case["init_conds"], init_cond_ref, keys_map, "ref")
    process_condition(case["init_conds"], init_cond_mqtg, keys_map, "mqtg")
    if not is_mqtg:
        process_condition(case["init_conds"], init_cond_rec, keys_map, "rec")


# returns structure data and plots for one test.
def process_test_case_data(test_item, init_cond_ref, init_cond_rec, init_cond_mqtg, plot_base64, date_time, is_mqtg):
    test_id, part_id, case_id = split_string(test_item['id'])
    test, part, case = get_test_test_part_test_case(copy.deepcopy(qtg_structure['tests']), test_id, part_id, case_id)

    # Format the date as mm.dd.yyyy
    formatted_date = date_time.strftime("%m.%d.%Y")

    # Format the time as hh:mm:ss
    formatted_time = date_time.strftime("%H:%M:%S")

    get_initial_conditions(case, init_cond_ref, init_cond_mqtg, init_cond_rec, is_mqtg)

    case.update({
        "is_mqtg": is_mqtg,
        "is_automatic": test_item['is_automatic'],
        "curr_date": formatted_date,
        "curr_time": formatted_time,
        "plots_base64": plot_base64
    })

    # print(case)

    data = {
        "test": test,
        "part": part,
        "case": case,
    }

    return data


# creates a test_case report for one test case with headers.
def create_test_case_pdf(data, output_file):
    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('./templates'))
    template = env.get_template('test_case.html')

    # Render the HTML template with data
    html_out = template.render(data)
    css_path = './templates/style.css'
    # Convert the rendered HTML to PDF
    HTML(string=html_out).write_pdf(output_file, stylesheets=[CSS(css_path)])


# PUBLIC FUNCTIONS

# create master test pdf in root directory for all executed tests.
def create_test_report(test_results, output_dir):
    def find_or_create(object, key, item):
        # Search for the test with the matching id
        for new_item in object[key]:
            if new_item["id"] == item["id"]:
                return new_item  # Return the existing test if found

        object[key].append(item)
        return item

    grouped_data = {"tests": []}

    # Step 2: Populate the structure
    for key, item in test_results.items():
        test = item["test"]
        test = find_or_create(grouped_data, "tests", test)

        part = item["part"]
        part = find_or_create(test, "test_parts", part)

        case = item["case"]
        case = find_or_create(part, "test_cases", case)

    env = Environment(loader=FileSystemLoader('./templates'))
    template = env.get_template('test.html')

    # Render the HTML template with data
    html_out = template.render(grouped_data)
    css_path = './templates/style.css'
    # Convert the rendered HTML to PDF
    HTML(string=html_out).write_pdf(os.path.join(output_dir, "Report.pdf"), stylesheets=[CSS(css_path)])


def generate_case_report(test_item, test_dir, date_time, is_mqtg=False):
    # make pdf for each test, merge them into one document. check
    init_cond_rec, init_cond_ref, init_cond_mqtg = load_json_data(test_dir)

    # load existing images
    plots_base64 = load_plots(test_dir)
    data = process_test_case_data(test_item, init_cond_ref, init_cond_rec, init_cond_mqtg, plots_base64, date_time, is_mqtg)

    create_test_case_pdf(data, os.path.join(test_dir, "Report.pdf"))

    return data


# Generate the PDF
# if __name__ == "__main__":
#     # 1. einen, mehrerer oder alle tests
#     # 2. einen oder mehrere test cases
#     print("MQTG PDF Creator")
#     create_init_cond = input("Create Initial QTG? (y/n): ").strip().lower() == 'y'
#     test_name = input("Enter Test (leave empty to create all): ")
#     test_case_name = ""
#     if len(test_name) != 0:
#         test_case_name = input("Enter Test Case (leave empty to create all test cases of a test): ")
#
#     print(f"Create Initial QTG: {create_init_cond}")
#     print(f"Test: {test_name}")
#     print(f"Test Case: {test_case_name}")
#     input()
#
#     generate_case_report("./data")

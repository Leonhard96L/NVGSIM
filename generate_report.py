import base64
import json
import os
import re

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS

from qtg_data_structure import data as qtg_structure
from function_lib import split_string, get_test_test_part_test_case, units_conversion
from test_mode import TestMode


def load_json_data(qtg_path, mode):
    file_path = os.path.join(qtg_path, 'init_conditions.json')
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

        # TODO: init cond für FTD3, FTD1...
        (init_cond_qtg,) = data.get("Init_condition_QTG"),
        (init_cond_mqtg,) = data.get("Init_condition_MQTG"),
        (init_cond_ref,) = data.get("Init_condition_Refer"),

        if mode == TestMode.REFERENCE:
            units_conversion(init_cond_ref, 'Avi')
        if mode == TestMode.MQTG:
            units_conversion(init_cond_mqtg, 'Avi')
        if mode == TestMode.QTG:
            units_conversion(init_cond_mqtg, 'Avi')
            units_conversion(init_cond_qtg, 'Avi')

        print(init_cond_ref)
        print(init_cond_mqtg)
        print(init_cond_qtg)

        return init_cond_ref, init_cond_mqtg, init_cond_qtg


def load_json_snapshots(test_item, qtg_path, mode):
    test_id, part_id, case_id = split_string(test_item['id'])
    test, part, case = get_test_test_part_test_case(qtg_structure['tests'], test_id, part_id, case_id)

    if not part['snapshot']:
        print("Not a snapshot test -> not reading json.")
        return {}

    file_path = ""
    if mode == TestMode.REFERENCE:
        file_path = os.path.join(qtg_path, 'output_table_refer.json')
    elif mode == TestMode.MQTG:
        file_path = os.path.join(qtg_path, 'output_table_mqtg.json')
    elif mode == TestMode.QTG:
        file_path = os.path.join(qtg_path, 'output_table_qtg.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    # Dynamically generate structured data with cleaned values
    structured_data = {}
    for key, values in data.items():
        # Filter out invalid data (e.g., " ")
        structured_data[key] = [value for value in values if value != " "]

    print(json.dumps(structured_data, indent=4))
    return structured_data


# load plots instead of creating them.
def load_plots(qtg_path, mode, only_refer=True):
    plot_paths = []

    # Get a sorted list of all .svg files in the directory
    # Function to extract the leading number from the filename
    def numerical_sort(value):
        # Extract the leading number (before any non-digit character)
        match = re.match(r'^(\d+)', value)
        return int(match.group(1)) if match else 0  # Use the number if found, else 0

    # Get the sorted list of .svg files in numerical order
    if mode == TestMode.REFERENCE:
        if only_refer:
            image_files = sorted([f for f in os.listdir(qtg_path) if f.endswith('refer.svg')], key=numerical_sort)
        else:
            image_files = sorted([f for f in os.listdir(qtg_path) if f.endswith('.svg')], key=numerical_sort)

    if mode == TestMode.MQTG:
        image_files = sorted([f for f in os.listdir(qtg_path) if f.endswith('mqtg.svg')], key=numerical_sort)

    if mode == TestMode.MQTG:
        image_files = sorted([f for f in os.listdir(qtg_path) if f.endswith('qtg.svg')], key=numerical_sort)

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


def get_initial_conditions(case, init_cond_ref, init_cond_mqtg, init_cond_qtg, mode):
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

    # Process each condition and populate the corresponding sub-categories
    if mode == TestMode.REFERENCE:
        process_condition(case["init_conds"], init_cond_ref, keys_map, "ref")
    elif mode == TestMode.MQTG:
        process_condition(case["init_conds"], init_cond_mqtg, keys_map, "mqtg")
    elif mode == TestMode.QTG:
        process_condition(case["init_conds"], init_cond_mqtg, keys_map, "mqtg")
        process_condition(case["init_conds"], init_cond_qtg, keys_map, "qtg")

# returns structure data and plots for one test.
def process_test_case_data(test_item, init_cond_ref, init_cond_mqtg, init_cond_qtg, plot_base64, date_time, mode):
    test_id, part_id, case_id = split_string(test_item['id'])
    test, part, case = get_test_test_part_test_case(qtg_structure['tests'], test_id, part_id, case_id)

    formatted_date = date_time.strftime("%d.%m.%Y")
    formatted_time = date_time.strftime("%H:%M:%S")

    get_initial_conditions(case, init_cond_ref, init_cond_mqtg, init_cond_qtg, mode)

    case.update({
        "is_snapshot": part['snapshot'],
        "is_mqtg": False,   # todo -> mode
        "is_automatic": test_item['is_automatic'],
        "software_version": '1_FTD_1.0',
        "curr_date": formatted_date,
        "curr_time": formatted_time,
        "plots_base64": plot_base64
    })

    data = {
        "test": test,
        "part": part,
        "case": case,
    }

    return data


def process_test_case_na(test_item, date_time, mode):
    test_id, part_id, case_id = split_string(test_item['id'])
    test, part, case = get_test_test_part_test_case(qtg_structure['tests'], test_id, part_id, case_id)

    formatted_date = date_time.strftime("%d.%m.%Y")
    formatted_time = date_time.strftime("%H:%M:%S")

    case.update({
        "curr_date": formatted_date,
        "curr_time": formatted_time,
    })

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
    template = env.get_template('test_case_wrapper.html')

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
        test = find_or_create(grouped_data, "tests", item["test"])
        part = find_or_create(test, "test_parts", item["part"])
        find_or_create(part, "test_cases", item["case"])

    env = Environment(loader=FileSystemLoader('./templates'))
    template = env.get_template('test.html')

    # Render the HTML template with data
    html_out = template.render(grouped_data)
    css_path = './templates/style.css'
    # Convert the rendered HTML to PDF
    HTML(string=html_out).write_pdf(os.path.join(output_dir, "Report.pdf"), stylesheets=[CSS(css_path)])


def generate_case_report(test_item, test_dir, date_time, mode: TestMode):
    if not test_item['is_applicable']:
        return process_test_case_na(test_item, date_time, mode)

    # make pdf for each test, merge them into one document. check
    init_cond_ref, init_cond_mqtg, init_cond_qtg, = load_json_data(test_dir, mode)

    # snapshot_data = load_json_snapshots(test_item, test_dir, mode)
    # load existing images
    plots_base64 = load_plots(test_dir, mode)
    data = process_test_case_data(test_item, init_cond_ref, init_cond_mqtg, init_cond_qtg, plots_base64, date_time, mode) # TODO: mode
    create_test_case_pdf(data, os.path.join(test_dir, "Report.pdf"))

    plots_base64 = load_plots(test_dir, mode, only_refer=False)
    data2 = process_test_case_data(test_item, init_cond_ref, init_cond_mqtg, init_cond_qtg, plots_base64, date_time, mode) # TODO: mode
    create_test_case_pdf(data2, os.path.join(test_dir, "Hidden_Report.pdf"))

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

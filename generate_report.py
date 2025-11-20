import base64
import json
import math
import os
import re
import tempfile
import win32com.client as win32
from premailer import transform

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS

from constants import TEMPLATE_NAME_CASE_WRAPPER, FILE_NAME_REPORT, TEMPLATE_PATH, TEMPLATE_PATH_STYLE, \
    TEMPLATE_NAME_TEST, TEMPLATE_NAME_CASE_FOOTER
from qtg_data_structure import data as qtg_structure
from function_lib import split_string, get_test_test_part_test_case, units_conversion
from qtg_generator import software_version
from test_mode import TestMode


def load_json_data(qtg_path, mode):
    file_path = os.path.join(qtg_path, 'init_conditions.json')
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

        # TODO: init cond für FTD3, FTD1...
        (init_cond_qtg,) = data.get("Init_condition_Recurrent"),
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
        file_path = os.path.join(qtg_path, 'output_table_recurrent.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    # Dynamically generate structured data with cleaned values
    structured_data = {}
    for key, values in data.items():
        # Filter out invalid data (e.g., " ")
        structured_data[key] = [value for value in values]

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

    image_files = []
    # Get the sorted list of .svg files in numerical order
    if only_refer:
        if mode == TestMode.REFERENCE:
            image_files = sorted([f for f in os.listdir(qtg_path) if f.endswith('refer.png')], key=numerical_sort)
        elif mode == TestMode.MQTG:
            image_files = sorted([f for f in os.listdir(qtg_path) if f.endswith('mqtg.png')], key=numerical_sort)
        elif mode == TestMode.QTG:
            image_files = sorted([f for f in os.listdir(qtg_path) if f.endswith('recurrent.png')], key=numerical_sort)
    else:
        image_files = sorted([f for f in os.listdir(qtg_path) if f.endswith('.png')], key=numerical_sort)

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
        process_condition(case["init_conds"], init_cond_qtg, keys_map, "rec")


# returns structure data and plots for one test.
def process_test_case_data(test_item, snapshot_data, init_cond_ref, init_cond_mqtg, init_cond_qtg, plot_base64,
                           date_time, mode):
    test_id, part_id, case_id = split_string(test_item['id'])
    test, part, case = get_test_test_part_test_case(qtg_structure['tests'], test_id, part_id, case_id)

    formatted_date = date_time.strftime("%d.%m.%Y")
    formatted_time = date_time.strftime("%H:%M:%S")

    get_initial_conditions(case, init_cond_ref, init_cond_mqtg, init_cond_qtg, mode)
    is_automatic = False if mode == mode.REFERENCE else test_item[
        'is_automatic']  # references cannot be automatic tests

    # use 1 page for part, 5 for static case, +1 for snapshot data, ceil(n/3) for plots
    count = 3 if mode != mode.REFERENCE else 2
    if part['snapshot']:
        count += 1
    count += int(math.ceil(len(plot_base64) / 3))

    case.update({
        "is_snapshot": part['snapshot'],
        "snapshot_data": snapshot_data,
        "is_automatic": is_automatic,
        "plots_base64": plot_base64,
        "calculated_page_number": count,
        "software_version": software_version,
        "curr_date": formatted_date,
        "curr_time": formatted_time,
    })

    data = {
        "test": test,
        "part": part,
        "case": case,
        "mode": mode,
        "testMode": TestMode,
    }

    return data


def process_test_case_na(test_item, date_time, mode):
    test_id, part_id, case_id = split_string(test_item['id'])
    test, part, case = get_test_test_part_test_case(qtg_structure['tests'], test_id, part_id, case_id)

    formatted_date = date_time.strftime("%d.%m.%Y")
    formatted_time = date_time.strftime("%H:%M:%S")

    case.update({
        "calculated_page_number": 1,
        "software_version": software_version,
        "curr_date": formatted_date,
        "curr_time": formatted_time,
    })

    data = {
        "test": test,
        "part": part,
        "case": case,
        "mode": mode,
        "testMode": TestMode,
    }
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

def create_graphs_pdf(data, output_file):
    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('./templates'))
    template = env.get_template('graphs.html')

    # Render the HTML template with data
    html_out = template.render(data)
    css_path = './templates/style.css'
    # Convert the rendered HTML to PDF
    HTML(string=html_out).write_pdf(output_file, stylesheets=[CSS(css_path)])


# creates a test_case report for one test case with headers.
def create_test_case_pdf(data, output_dir):
    html_out = populate_template(TEMPLATE_NAME_CASE_WRAPPER, data)
    tmp_file_path = create_temp_file(html_out)

    word = setup_word()

    doc = open_document(word, tmp_file_path)
    create_footer_single_test_case(word, doc, data)
    save_document(doc, output_dir)

    do_post_processing(doc, word, tmp_file_path)

# PUBLIC FUNCTIONS

def create_test_report(test_results, output_dir, mode: TestMode):
    def find_or_create(object, key, item):
        # Search for the test with the matching id
        for new_item in object[key]:
            if new_item["id"] == item["id"]:
                return new_item  # Return the existing test if found

        object[key].append(item)
        return item

    data = {"tests": [], "mode": mode, "testMode": TestMode}

    # Step 2: Populate the structure
    for key, item in test_results.items():
        test = find_or_create(data, "tests", item["test"])
        part = find_or_create(test, "test_parts", item["part"])
        find_or_create(part, "test_cases", item["case"])

    html_out = populate_template(TEMPLATE_NAME_TEST, data)
    tmp_file_path = create_temp_file(html_out)

    word = setup_word()

    doc = open_document(word, tmp_file_path)
    toc_length = create_table_of_contents(doc)
    create_footer_test_report(word, doc, data, toc_length)
    doc.TablesOfContents(1).Update()
    save_document(doc, output_dir)

    do_post_processing(doc, word, tmp_file_path)

def populate_template(file_name, data):
    # open html template
    env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))
    template = env.get_template(file_name)
    html_out = template.render(data)

    # inline all css since word ignores stylesheets
    with open(TEMPLATE_PATH_STYLE, "r", encoding="utf-8") as f:
        css = f.read()
    html_content = f"<style>{css}</style>\n" + html_out
    html_styled = transform(html_content)

    return html_styled


def create_temp_file(html_out):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp_file:
        tmp_file.write(html_out)
        tmp_file_path = tmp_file.name
    return tmp_file_path


def setup_word():
    word = win32.gencache.EnsureDispatch("Word.Application")
    # setting to false hides word but can lead to problems
    word.Visible = True
    word.ScreenUpdating = False
    word.DisplayAlerts = False

    return word


def open_document(word, file_path):
    return word.Documents.Open(file_path)

def save_document(doc, output_dir):
    # FileFormat 16 = wdFormatDocumentDefault (.docx)
    doc.SaveAs(os.path.join(output_dir, FILE_NAME_REPORT), FileFormat=16)

def do_post_processing(doc, word, tmp_file_path):
    doc.Close()
    word.Quit()
    os.remove(tmp_file_path)

def create_table_of_contents(doc):
    # doc.ComputeStatistics(2) return number of pages in doc
    pages_before_toc = doc.ComputeStatistics(2)
    insert_table_of_contents(doc)
    return doc.ComputeStatistics(2) - pages_before_toc

def insert_table_of_contents(doc):
    # set range to start of document
    toc_range = doc.Range(0, 0)
    doc.TablesOfContents.Add(
        Range=toc_range,
        UseHeadingStyles=True,
        UpperHeadingLevel=1,
        LowerHeadingLevel=3,
        RightAlignPageNumbers=True,
        IncludePageNumbers=True
    )
    doc.TablesOfContents(1).Update()
    # select ToC
    rng = doc.TablesOfContents(1).Range
    # move to end of ToC
    rng.Collapse(Direction=0)
    # Insert a page break
    rng.InsertBreak(win32.constants.wdPageBreak)

def create_footer_single_test_case(word, doc, data):
    # flatten data to only ids
    cases = [{
        "test": {"id": data.get("test").get("id")},
        "part": {"id": data.get("part").get("id")},
        "case": data.get("case")
    }]
    do_footer_table(word, doc, cases, [])

# GAR continue from here

def create_footer_test_report(word, doc, data, toc_length):
    cases = transform_cases(data)
    pages = get_pages(cases, toc_length)
    do_footer_table(word, doc, cases, pages)

def transform_cases(data):
    result = []
    for test in data.get("tests", []):
        test_id = test.get("id")
        for part in test.get("test_parts", []):
            part_id = part.get("id")
            for case in part.get("test_cases", []):
                result.append({
                    "test": {"id": test_id},
                    "part": {"id": part_id},
                    "case": case
                })
    return result

def get_pages(cases, offset):
    pages = []
    # start at 1 to always select next page
    total = 1 + offset
    test_id = None
    part_id = None
    for case in cases:
        total += case["case"]["calculated_page_number"]
        if case["test"]["id"] != test_id or test_id is None:
            # start page new test or new part
            total += 2
            test_id = case["test"]["id"]
            part_id = case["part"]["id"]
        elif case["part"]["id"] != part_id:
            total += 1
            part_id = case["part"]["id"]

        pages.append(total)

    return pages

def do_footer_table(word, doc, cases, pages):
    doc.Repaginate()
    page_count = pages[-1] if pages else doc.ComputeStatistics(2) + 1

    case_index = 0
    for i in range(1, page_count):
        if i in pages:
            word.Selection.GoTo(win32.constants.wdGoToPage,
                                win32.constants.wdGoToAbsolute,
                                str(i))
            word.Selection.InsertBreak(win32.constants.wdSectionBreakNextPage)
            case_index += 1

        footer_table_path = get_footer(cases[case_index])
        footer_doc = word.Documents.Open(footer_table_path)

        footer_doc.Content.Select()
        word.Selection.Copy()
        footer_doc.Close(False)

        word.Selection.GoTo(win32.constants.wdGoToPage,
                            win32.constants.wdGoToAbsolute,
                            str(i))

        sec = word.ActiveDocument.Sections(word.ActiveDocument.Sections.Count)
        footer = sec.Footers(win32.constants.wdHeaderFooterPrimary)
        footer.LinkToPrevious = False

        if i in pages:
            footer.PageNumbers.RestartNumberingAtSection = True
            footer.PageNumbers.StartingNumber = 1

        footer.Range.Paste()

        # Move the range to the end of the footer
        rng = footer.Range
        rng.Collapse(win32.constants.wdCollapseEnd)

        rng.InsertParagraphAfter()
        rng = footer.Range
        rng.Collapse(win32.constants.wdCollapseEnd)
        chapter_prefix = f"{cases[case_index]['test']['id']}.{cases[case_index]['part']['id']}.{cases[case_index]['case']['id']}-"
        # Insert the prefix text
        rng.InsertBefore(chapter_prefix)
        rng.Collapse(win32.constants.wdCollapseEnd)
        rng.Fields.Add(rng, Type=win32.constants.wdFieldPage)
        rng.ParagraphFormat.Alignment = win32.constants.wdAlignParagraphRight

def get_footer(case):
    footer_out = populate_template(TEMPLATE_NAME_CASE_FOOTER, case)
    return create_temp_file(footer_out)

def generate_case_report(test_item, test_dir, date_time, mode: TestMode):
    if not test_item['is_applicable']:
        return process_test_case_na(test_item, date_time, mode)

    # make pdf for each test, merge them into one document. check
    init_cond_ref, init_cond_mqtg, init_cond_qtg, = load_json_data(test_dir, mode)

    snapshot_data = load_json_snapshots(test_item, test_dir, mode)
    # load existing images
    plots_base64 = load_plots(test_dir, mode)
    data = process_test_case_data(test_item, snapshot_data, init_cond_ref, init_cond_mqtg, init_cond_qtg, plots_base64,
                                  date_time, mode)
    create_test_case_pdf(data, test_dir)

    plots_base64 = load_plots(test_dir, mode, only_refer=False)
    data2 = process_test_case_data(test_item, snapshot_data, init_cond_ref, init_cond_mqtg, init_cond_qtg, plots_base64,
                                   date_time, mode)
    create_graphs_pdf(data2, os.path.join(test_dir, "Graphs.pdf"))

    return data

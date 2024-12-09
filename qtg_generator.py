import shutil
from datetime import datetime
import os
import tkinter as tk
from tkinter import ttk, filedialog

# import execute_test
import platform

from test_mode import TestMode

# Check if the OS is Windows
if platform.system() == "Windows":
    import execute_test

    # Define a function to run the test if the module was imported
    def run_test(test_item, test_dir, mode, gui_output, gui_input):
        # Invoke the function from the imported module
        execute_test.execute_test(test_item, test_dir, mode, gui_output, gui_input)

from qtg_data_structure import data
import generate_report


root_dir = './data'


# Function to populate the Treeview with test cases
def populate_tree(tree, data):
    for test in data['tests']:
        for part in test['test_parts']:
            if part.get('test_cases'):
                for case in part['test_cases']:
                    item_id = f"{test['id']}.{part['id']}_{case['id']}"
                    cond = case.get('name') if case.get('condition') is None else case.get('condition')
                    item_text = f"{item_id} - {part['main_title']}: {cond}"

                    is_applicable = True if case.get('not_applicable') is None else False
                    auto_possible = case.get('automatic_testing_possible')
                    tree.insert('', 'end', text=item_text, values=("", is_applicable, auto_possible))


# Function to sort Treeview items alphabetically
def sort_treeview(tree):
    items = [(tree.item(child)["text"], child) for child in tree.get_children()]
    items.sort()
    for index, (_, text) in enumerate(items):
        tree.move(text, '', index)


# Function to toggle test type
def toggle_test_type(tt):
    tt[0] = 'Automatic' if (tt[0] == 'Manual' and eval(tt[2])) else 'Manual'
    return tt


# Function to handle item transfer between Treeviews
def on_item_click(event, source_tree, target_tree):
    selected_items = source_tree.selection()
    if selected_items:
        for selected_item in selected_items:
            item_text = source_tree.item(selected_item, 'text')
            item_values = list(source_tree.item(selected_item, 'value'))
            if source_tree == tree_available:
                # Move item from left to right
                item_values[0] = 'Manual'
                # item_value[1] means automatic_possible!
                if eval(item_values[2]):
                    item_values[0] = 'Automatic'
                target_tree.insert('', 'end', text=item_text, values=item_values)
            elif source_tree == tree_selected:
                # Move item from right to left
                tree_available.insert('', 'end', text=item_text, values=item_values)
            source_tree.delete(selected_item)
        sort_treeview(source_tree)  # Sort the source treeview
        sort_treeview(target_tree)  # Sort the target treeview


# Function to handle single click
def on_item_single_click(event, source_tree, target_tree):
    # Get the item under the cursor
    item = source_tree.identify_row(event.y)

    if item:  # If an item is under the cursor
        # Check if the item is already selected, if not, select it
        if item not in source_tree.selection():
            source_tree.selection_set(item)

    # Process all selected items
    selected_items = source_tree.selection()
    if selected_items:
        for selected_item in selected_items:
            if source_tree == tree_selected:
                # Update the item's text and values
                item_values = list(source_tree.item(selected_item, 'values'))
                item_values = toggle_test_type(item_values)
                source_tree.item(selected_item, values=item_values)


# Function to handle double-click
def on_double_click(event, source_tree, target_tree):
    double_click_flag[0] = True
    on_item_click(event, source_tree, target_tree)


# Function to handle button release
def on_release(event):
    double_click_flag[0] = False  # Reset the flag on button release


# Function to select destination directory
def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_var.set(directory)


# Function to handle button actions
def on_select_all_tests():
    for item in tree_available.get_children():
        tree_available.selection_add(item)
        on_item_click(None, tree_available, tree_selected)


def on_remove_all_tests():
    for item in tree_selected.get_children():
        tree_selected.selection_add(item)
        on_item_click(None, tree_selected, tree_available)


def on_start_reference():
    gui_output("Starting Reference...")
    start_testing(create_test_list(), output_dir=directory_var.get(), mode=TestMode.REFERENCE)


def on_start_mqtg():
    gui_output("Starting MQTG...")
    start_testing(create_test_list(), output_dir=directory_var.get(), mode=TestMode.MQTG)


def on_start_qtg():
    gui_output("Starting QTG...")
    start_testing(create_test_list(), output_dir=directory_var.get(), mode=TestMode.QTG)


def create_test_list():
    items_data = []
    for item in tree_selected.get_children():
        # Retrieve the text and values for each item
        item_text = tree_selected.item(item, 'text')
        item_values = tree_selected.item(item, 'values')

        # Split the text and save everything before the first space
        test_id = item_text.split(' ', 1)[0]  # Take the part before the first space

        # Create a boolean based on the test_type value
        is_automatic = (item_values[0] == "Automatic")
        is_applicable = eval(item_values[1])

        # Append the processed data to the list
        test_item = {
            'id': test_id,
            'is_automatic': is_automatic,
            'is_applicable': is_applicable,
            'full_name': item_text,
        }
        items_data.append(test_item)

    return items_data


def gui_output(text, nl=True):
    if nl:
        text = text + "\n"
    progress_text.insert(tk.END, text)
    progress_text.yview_moveto(1.0)
    root.update()


def on_input_submit():
    inp = input_var.get()
    if input_text:
        input_text.set(inp)
        gui_output(f"$: {inp}")
        input_var.set("")


def gui_input(prompt):
    gui_output(prompt, nl=False)
    root.wait_variable(input_text)  # Block until input_var is updated
    inp = input_text.get()
    return inp


# todo: error handling if null
def get_newest_folder(directory_path):
    # Get all folder names that match the format yyyymmdd:HHMMSS
    folders = [f for f in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, f))]

    # Get the folder with the newest date in the name
    return os.path.join(directory_path, max(folders, key=lambda f: datetime.strptime(f, "%Y%m%d_%H%M%S")))


def copy_directory_contents(src_dir, dest_dir):
    """
    Copies only .xml, .json, and .sim files from src_dir to dest_dir.
    It will create the destination directory if it doesn't exist.

    :param src_dir: Source directory path
    :param dest_dir: Destination directory path
    """
    # Check if source directory exists

    if not os.path.exists(src_dir):
        raise FileNotFoundError(f"The source directory '{src_dir}' does not exist.")

    # Create destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Allowed file extensions
    allowed_extensions = {'.xml', '.json', '.sim'}

    # Copy contents from source to destination
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isdir(src_path):
            # Recursively copy directories
            shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
        else:
            # Check if the file has an allowed extension
            _, extension = os.path.splitext(item)
            if extension in allowed_extensions:
                print(f"Copying {src_path} to {dest_path}")
                # Copy individual files with allowed extensions
                shutil.copy2(src_path, dest_path)


# this is basically the main method that controls all other programs
def start_testing(tests: [], output_dir='./', mode=TestMode.QTG, gui_output=gui_output, gui_input=gui_input):
    date_time = datetime.now()  # use this datetime for folder structure and reports

    qtg_dir = ""
    if mode == TestMode.REFERENCE:
        qtg_dir = "reference"
        reference_data = get_newest_folder(os.path.join(output_dir, "reference"))   # initial_conditions oder lassen???
    elif mode == TestMode.MQTG:
        qtg_dir = "mqtg"
        reference_data = get_newest_folder(os.path.join(output_dir, "reference"))
    elif mode == TestMode.QTG:
        qtg_dir = "qtg"
        reference_data = get_newest_folder(os.path.join(output_dir, "mqtg"))

    # Get the current date and format it as yyyymmdd
    directory_structure = os.path.join(output_dir, qtg_dir, date_time.strftime('%Y%m%d_%H%M%S'))
    # directory_structure = os.path.join(output_dir, qtg_dir, "20240827_091010")    # this is for testing purposes only!
    test_results = {}

    try:
        for test_item in tests:
            gui_output(f"Test id: {test_item['id']}\tautomatic Test: {test_item['is_automatic']}")

            ref_dir = os.path.join(reference_data, test_item['id'])
            test_dir = os.path.join(directory_structure, test_item['id'])

            if mode == TestMode.REFERENCE:
                test_item['is_automatic'] = False

            if test_item['is_applicable']:
                copy_directory_contents(ref_dir, test_dir)
                gui_output(f"Save directory: {test_dir}")

                while True:
                    # execute test
                    if platform.system() == "Windows":
                        run_test(test_item, test_dir, mode, gui_output, gui_input)
                    # execute_test.execute_test(test_item, test_dir, mqtg, gui_output, gui_input)

                    # generate report
                    gui_output("Creating Test Report. This may take a second...")
                    test_results[test_item['id']] = generate_report.generate_case_report(test_item, test_dir, date_time, mode)
                    gui_output("Done creating Report.\n")

                    if gui_input("Do you want to continue with the next test (y) or repeat the current test (n) ? ").lower() == 'y':
                        break
            else:
                gui_output(f"Test not applicable - skipping. It will be inserted to the main report")
                test_results[test_item['id']] = generate_report.generate_case_report(test_item, test_dir, date_time, mode)

        gui_output("Creating Full Report. This may take a second...")
        generate_report.create_test_report(test_results, directory_structure, mode)
        gui_output("Done creating Full Report.\n")
        gui_output("COMPLETED!")

    except Exception as e:
        gui_output(f"Error: {e}")


# Function to select items in the tree by item_id
def select_items_by_ids(tree, item_ids):
    for item_id in item_ids:
        # Iterate through all items in the tree
        for item in tree.get_children(''):  # '' is the root of the tree
            item_text = tree.item(item, 'text')
            # Check if the item_id is part of the item text (formatted as "id - other text")
            if item_text.startswith(item_id):
                # Select the matching item
                tree.selection_set(item)
                on_item_click(None, tree_available, tree_selected)


def generate_report_only():
    dir = directory_var.get()

    gui_output(f"Generating Reports: {dir}")

    try:
        test_date = datetime.strptime(os.path.basename(dir), '%Y%m%d_%H%M%S')
        print(test_date)
    except ValueError:
        gui_output("Folder name is wrong. should be yymmdd_HHMMSS. Cancelling.")
        return

    # Get all subfolders
    subfolders = [f for f in os.listdir(dir) if os.path.isdir(os.path.join(dir, f))]
    if len(subfolders) == 0:
        gui_output("No tests found in the selected folder. Cancelling.")
        return

    parent_name = os.path.basename(os.path.dirname(dir))
    print(parent_name)
    if parent_name != "reference" and parent_name != "mqtg" and parent_name != "qtg":
        gui_output("Parent dir is not reference/mqtg/qtg. Cancelling.")
        return

    mode = TestMode.QTG
    if parent_name == "reference":
        mode = TestMode.REFERENCE
    elif parent_name == "mqtg":
        mode = TestMode.MQTG
    elif parent_name == "qtg":
        mode = TestMode.QTG

    on_remove_all_tests()
    select_items_by_ids(tree_available, subfolders)

    if len(tree_selected.get_children()) == 0:
        gui_output("No tests found in the selected folder. Cancelling.")
        return

    gui_input("Check selected tests and adjust Test Type to automatic/manual. Type enter to proceed generating reports. ")
    # now we have all existing tests selected and can start generating reports...
    tests = create_test_list()
    test_results = {}
    try:
        for test_item in tests:
            gui_output(f"Creating Test Report for {test_item['id']}. This may take a second...")
            test_results[test_item['id']] = generate_report.generate_case_report(test_item, os.path.join(dir, test_item['id']), test_date, mode)

        gui_output("Creating Full Report. This may take a second...")
        generate_report.create_test_report(test_results, dir, mode)
        gui_output("Done creating Full Report.\n")
    except Exception as e:
        gui_output(f"Error: {e}")


# Initialize and configure the Tkinter window
if __name__ == "__main__":
    root = tk.Tk()
    root.title("QTG Generator v1.1")
    root.geometry('1920x1080')

    # Initialize flag to indicate a double-click
    double_click_flag = [False]

    # Create frames
    frame_left = ttk.Frame(root, padding=1)
    frame_right = ttk.Frame(root, padding=1)
    frame_controls = ttk.Frame(root, padding=1)
    frame_progress = ttk.Frame(root, padding=1)

    frame_left.grid(row=1, column=0, sticky="nsew")
    frame_right.grid(row=1, column=1, sticky="nsew")
    frame_controls.grid(row=2, column=0, columnspan=2, sticky="ew")
    frame_progress.grid(row=3, column=0, columnspan=2, sticky="nsew")

    # Labels for each list
    label_left = ttk.Label(root, text="Available Tests")
    label_right = ttk.Label(root, text="Selected Tests (right-click to toggle automatic/manual mode, double click to remove)")
    label_left.grid(row=0, column=0, sticky="nsew")
    label_right.grid(row=0, column=1, sticky="nsew")

    # Create Treeviews with increased minimum height
    tree_available = ttk.Treeview(frame_left, columns=(), show='tree', height=18)
    tree_available.grid(row=0, column=0, sticky="nsew")

    tree_selected = ttk.Treeview(frame_right, columns=('test_type', 'is_applicable', 'auto_possible'), show='tree headings', height=18)
    tree_selected.grid(row=0, column=0, sticky="nsew")
    tree_selected.heading('test_type', text='Test Type')
    tree_selected.heading('is_applicable', text='Applicable')
    tree_selected.heading('auto_possible', text="Auto possible")

    # Set column weights and widths
    tree_selected.column('test_type', width=80, stretch=tk.NO)
    tree_selected.column('is_applicable', width=80, stretch=tk.NO)
    tree_selected.column('auto_possible', width=80, stretch=tk.NO)

    # Add scrollbars
    scrollbar = ttk.Scrollbar(frame_left, orient=tk.VERTICAL, command=tree_available.yview)
    tree_available.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    scrollbar = ttk.Scrollbar(frame_right, orient=tk.VERTICAL, command=tree_selected.yview)
    tree_selected.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    # Populate the available tree
    populate_tree(tree_available, data)

    # Create directory selector
    directory_var = tk.StringVar()
    directory_var.set(root_dir)
    directory_entry = ttk.Entry(frame_controls, textvariable=directory_var, width=50)
    directory_entry.grid(row=0, column=0, padx=5, pady=5)
    directory_button = ttk.Button(frame_controls, text="Select Directory", command=select_directory)
    directory_button.grid(row=0, column=1, padx=5, pady=5)
    generate_report_button = ttk.Button(frame_controls, text="Generate Reports Only", command=generate_report_only)
    generate_report_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

    # Create action buttons
    select_all_button = ttk.Button(frame_controls, text="Select All Tests", command=on_select_all_tests)
    select_all_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    remove_all_button = ttk.Button(frame_controls, text="Remove All Tests", command=on_remove_all_tests)
    remove_all_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    start_reference_button = ttk.Button(frame_controls, text="Start Reference", command=on_start_reference)
    start_reference_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
    start_mqtg_button = ttk.Button(frame_controls, text="Start MQTG", command=on_start_mqtg)
    start_mqtg_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
    start_qtg_button = ttk.Button(frame_controls, text="Start QTG", command=on_start_qtg)
    start_qtg_button.grid(row=2, column=2, padx=5, pady=5, sticky="ew")

    # Create progress text box
    progress_text = tk.Text(frame_progress, height=15, wrap='word')
    progress_text.grid(row=0, column=0, sticky="nsew")

    # Create input text field at the bottom
    input_var = tk.StringVar()
    input_entry = ttk.Entry(root, textvariable=input_var)
    input_entry.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    input_text = tk.StringVar()

    # Bind the Enter key to the input submission function
    input_entry.bind("<Return>", lambda event: on_input_submit())

    # Make the frames expand with the window
    root.grid_rowconfigure(0, weight=0)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=0)
    root.grid_rowconfigure(3, weight=1)
    root.grid_rowconfigure(4, weight=0)  # Row for the input field

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    frame_left.grid_rowconfigure(0, weight=1)
    frame_left.grid_columnconfigure(0, weight=1)

    frame_right.grid_rowconfigure(0, weight=1)
    frame_right.grid_columnconfigure(0, weight=1)

    frame_progress.grid_rowconfigure(0, weight=1)
    frame_progress.grid_columnconfigure(0, weight=1)

    # Bind events
    tree_available.bind("<Double-1>", lambda event: on_double_click(event, tree_available, tree_selected))
    tree_selected.bind("<Double-1>", lambda event: on_double_click(event, tree_selected, tree_available))
    tree_available.bind("<ButtonRelease-3>", lambda event: on_item_single_click(event, tree_available, tree_selected))
    tree_selected.bind("<ButtonRelease-3>", lambda event: on_item_single_click(event, tree_selected, tree_available))
    root.bind("<ButtonRelease-3>", on_release)

    # Start the Tkinter event loop
    root.mainloop()

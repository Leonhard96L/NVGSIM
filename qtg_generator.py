import tkinter as tk
from tkinter import ttk, filedialog
from qtg_data_structure import qtg_data_structure


# Function to populate the Treeview with test cases
def populate_tree(tree, data):
    for test in data['tests']:
        for part in test['test_parts']:
            for case in part['test_cases']:
                item_id = f"{test['id']}.{part['id']}.{case['id']}"
                item_text = f"{item_id} - {part['main_title']}: {case['condition']}"
                tree.insert('', 'end', text=item_text)


# Function to sort Treeview items alphabetically
def sort_treeview(tree):
    items = [(tree.item(child)["text"], child) for child in tree.get_children()]
    items.sort()
    for index, (_, text) in enumerate(items):
        tree.move(text, '', index)


# Function to toggle test type
def toggle_test_type(tt):
    return 'Manual' if tt == 'Automatic' else 'Automatic'


# Function to handle item transfer between Treeviews
def on_item_click(event, source_tree, target_tree):
    selected_item = source_tree.selection()
    if selected_item:
        # item_id = source_tree.item(selected_item, 'iid')
        item_text = source_tree.item(selected_item, 'text')
        if source_tree == tree_available:
            # Move item from left to right
            test_type = 'Automatic'
            target_tree.insert('', 'end', text=item_text, values=(test_type,))
            source_tree.delete(selected_item)
        elif source_tree == tree_selected:
            # Move item from right to left
            tree_available.insert('', 'end', text=item_text)
            source_tree.delete(selected_item)
        sort_treeview(source_tree)  # Sort the source treeview
        sort_treeview(target_tree)  # Sort the target treeview


# Function to handle single click
def on_item_single_click(event, source_tree, target_tree):
    if not double_click_flag[0]:  # Check if double-click was not detected
        selected_item = source_tree.selection()
        if selected_item:
            if source_tree == tree_selected:
                # item_id = source_tree.item(selected_item, 'iid')
                item_values = source_tree.item(selected_item, 'values')
                test_type = toggle_test_type(item_values[0])  # Toggle the flag

                # Update the item's text and values
                source_tree.item(selected_item, values=(test_type))


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


def on_start_mqtg():
    progress_text.insert(tk.END, "Starting MQTG...\n")
    progress_text.yview_moveto(1.0)


def on_start_qtg():
    progress_text.insert(tk.END, "Starting QTG...\n")
    progress_text.yview_moveto(1.0)


# Initialize and configure the Tkinter window
if __name__ == "__main__":
    root = tk.Tk()
    root.title("QTG Generator v0.1")
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
    label_right = ttk.Label(root, text="Selected Tests (click to toggle automatic/manual mode, double click to remove)")
    label_left.grid(row=0, column=0, sticky="nsew")
    label_right.grid(row=0, column=1, sticky="nsew")

    # Create Treeviews with increased minimum height
    tree_available = ttk.Treeview(frame_left, columns=(), show='tree', height=18)
    tree_available.grid(row=0, column=0, sticky="nsew")

    tree_selected = ttk.Treeview(frame_right, columns=('test_type'), show='tree headings', height=18)
    tree_selected.grid(row=0, column=0, sticky="nsew")
    tree_selected.heading('test_type', text='Test Type')

    # Set column weights and widths
    # tree_selected.column('#0', minwidth=200, stretch=tk.YES)  # First column takes up remaining space
    tree_selected.column('test_type', width=70, stretch=tk.NO)

    # Add scrollbars
    scrollbar = ttk.Scrollbar(frame_left, orient=tk.VERTICAL, command=tree_available.yview)
    tree_available.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    scrollbar = ttk.Scrollbar(frame_right, orient=tk.VERTICAL, command=tree_selected.yview)
    tree_selected.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    # Populate the available tree
    populate_tree(tree_available, qtg_data_structure)

    # Create directory selector
    directory_var = tk.StringVar()
    directory_entry = ttk.Entry(frame_controls, textvariable=directory_var, width=50)
    directory_entry.grid(row=0, column=0, padx=5, pady=5)
    directory_button = ttk.Button(frame_controls, text="Select Directory", command=select_directory)
    directory_button.grid(row=0, column=1, padx=5, pady=5)

    # Create action buttons
    select_all_button = ttk.Button(frame_controls, text="Select All Tests", command=on_select_all_tests)
    select_all_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    remove_all_button = ttk.Button(frame_controls, text="Remove All Tests", command=on_remove_all_tests)
    remove_all_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    start_mqtg_button = ttk.Button(frame_controls, text="Start MQTG", command=on_start_mqtg)
    start_mqtg_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
    start_qtg_button = ttk.Button(frame_controls, text="Start QTG", command=on_start_qtg)
    start_qtg_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    # Create progress text box
    progress_text = tk.Text(frame_progress, height=15, wrap='word')
    progress_text.grid(row=0, column=0, sticky="nsew")

    # Make the frames expand with the window
    root.grid_rowconfigure(0, weight=0)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=0)
    root.grid_rowconfigure(3, weight=1)

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
    tree_available.bind("<ButtonRelease-1>", lambda event: on_item_single_click(event, tree_available, tree_selected))
    tree_selected.bind("<ButtonRelease-1>", lambda event: on_item_single_click(event, tree_selected, tree_available))
    root.bind("<ButtonRelease-1>", on_release)

    # Start the Tkinter event loop
    root.mainloop()

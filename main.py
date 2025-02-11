import PySimpleGUI as sg
import os, json, time
from pathlib import Path
import gpt_fn


def modify_files(response, base_path):
    """
    Modify local files based on the GPT response.

    Args:
        response (dict): Dictionary containing file paths and modified contents
        base_path (str): Base directory path to write files to

    The response dict should contain:
        - file_paths: List of relative file paths
        - modified_contents: List of new file contents
    """
    print("Modifying local files...")
    paths = response["file_paths"]
    contents = response["modified_contents"]
    try:
        for path, content in zip(paths, contents):
            Path.write_text(Path(base_path + path), data=content)
    except Exception as e:
        print(f"Error modifying files: {str(e)}")
    print("Modification complete...")


# Base folder path for project files
projects_folder = "/Users/hajj/Programming/Python/Projects/"

# Define the window's layout components
directory_path = sg.Input(key="-FOLDER-", enable_events=True)
browse_button = sg.FolderBrowse(initial_folder=projects_folder, target="-FOLDER-")
directory_list = sg.Listbox(
    values=[],
    size=(60, 10),
    select_mode=sg.LISTBOX_SELECT_MODE_BROWSE,
    enable_events=True,
    key="-PATHS-",
)

# Define the complete window layout with all UI elements
layout = [
    [sg.Text("Select Directory:"), directory_path, browse_button],
    [directory_list],
    [sg.Text("Enter text:"), sg.InputText(key="-INPUT-")],
    [
        sg.Button("Submit", key="-SUBMIT-"),
        sg.Button("Clear", key="-CLEAR-"),
        sg.Button("Exit"),
    ],
]

# Initialize the main application window
app_window = sg.Window("Directory Browser", layout, font=("Helvetica", 14))
selected_files = []

# Main event loop
while True:
    event, values = app_window.read()
    print("event", event)
    print("values", values)

    # Handle window close events
    if event == sg.WIN_CLOSED or event == "Exit":
        break

    # Update file list when a directory is selected
    if values["-FOLDER-"]:
        try:
            dir_path = values["-FOLDER-"]
            files = []
            # Recursively walk through directory
            for root, dirs, filenames in os.walk(dir_path):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith(".")]
                for filename in filenames:
                    # Skip hidden files
                    if not filename.startswith("."):
                        files.append(os.path.join(root, filename))
            # Convert absolute paths to relative paths
            files = [file.removeprefix(dir_path) for file in files]
            if app_window["-PATHS-"] is not None:  # Check if element exists
                directory_list.update(files)
        except:
            directory_list.update([])

    # Handle file selection/deselection in the listbox
    if event == "-PATHS-":
        if values["-PATHS-"]:  # Check if any item is selected
            selected_file = values["-PATHS-"][0]
            if selected_file in selected_files:
                selected_files.remove(selected_file)  # Unhighlight if already selected
            else:
                selected_files.append(selected_file)  # Highlight if not selected
            directory_list.set_value(selected_files)  # Update selection

    # Clear all selections when Clear button is pressed
    if event == "-CLEAR-":
        selected_files = []
        directory_list.set_value([])  # Clear all selections

    # Handle submit button press - process selected files with GPT
    if event == "-SUBMIT-":
        selected_files = values["-PATHS-"]
        input_text = values["-INPUT-"]

        if input_text and values["-FOLDER-"] and selected_files:
            # Read contents of all selected files
            contents = []
            for file in selected_files:
                contents.append(Path.read_text(Path(values["-FOLDER-"] + file)))

            # Load system prompt and response format
            system_prompt = gpt_fn.read_sys_prompt("system_prompt.txt")
            response_format = gpt_fn.read_response_format("response_format.json")

            # Build the user prompt with file contents
            user_prompt = ""
            for path, content in zip(selected_files, contents):
                user_prompt = (
                    user_prompt + f"file path: {path}\nfile content: {content}\n\n"
                )

            user_prompt = user_prompt + f"User prompt: {input_text}"
            print("All data collected for sending...")
            print("Submitting now...")

            # Send request to GPT and time the response
            time_start = time.perf_counter()
            response = gpt_fn.send_system_and_user_prompts(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_format=response_format,
            )
            time_stop = time.perf_counter()
            print(f"GPT Response in {time_stop - time_start:.2f} seconds...\n")

            # Process and apply the GPT response
            if response is not None:
                response = json.loads(s=response)
                modify_files(response, base_path=values["-FOLDER-"])
            else:
                print("No response received from GPT")
        else:
            print("Directory or/and user prompt not provided. Try again.")


# Clean up by closing the window
app_window.close()

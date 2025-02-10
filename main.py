import PySimpleGUI as sg
import os

def read_system_prompt():
    try:
        with open('system_prompt.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return "No system prompt file found"
    except Exception as e:
        return f"Error reading system prompt: {str(e)}"

system_prompt = read_system_prompt()

# Define the window's layout
layout = [
    [sg.Text("Select Directory:"), sg.FolderBrowse(key="-FOLDER-")],
    [sg.Listbox(values=[], size=(60, 10), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, key="-PATHS-")],
    [sg.Text("Enter text:"), sg.InputText(key="-INPUT-")],
    [sg.Button("Submit"), sg.Button("Exit")]
]

# Create the window
window = sg.Window("Directory Browser", layout)

# Event Loop
while True:
    event, values = window.read()

    # End program if user closes window or clicks Exit
    if event == sg.WIN_CLOSED or event == "Exit":
        break

    # Update file list when directory is selected
    if values["-FOLDER-"]:
        try:
            dir_path = values["-FOLDER-"]
            files = os.listdir(dir_path)
            window["-PATHS-"].update(files)
            # create json schema from directory with dir_path
        except:
            window["-PATHS-"].update([])

    if event == "Submit":
        selected_files = values["-PATHS-"]
        input_text = values["-INPUT-"]
        print("Selected files:", selected_files)
        print("Input text:", input_text)

window.close()

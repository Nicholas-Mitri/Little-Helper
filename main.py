import PySimpleGUI as sg

# Define the window's layout
layout = [
    [sg.Text("Welcome to My Application")],
    [sg.Text("Enter something:"), sg.InputText()],
    [sg.Button("Ok"), sg.Button("Cancel")]
]

# Create the window
window = sg.Window("My Application", layout)

# Event Loop
while True:
    event, values = window.read()

    # End program if user closes window or clicks cancel
    if event == sg.WIN_CLOSED or event == "Cancel":
        break

    if event == "Ok":
        print("You entered:", values[0])

window.close()

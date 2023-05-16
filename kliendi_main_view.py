import PySimpleGUI as sg

# Set the theme for the screen
sg.theme("Green")

# Set the font for the layout
font = "Times New Roman"

# Define the layout
layout = [
    [sg.VerticalSeparator(pad=(0, 30))],
    [sg.Text("Kaks Paskalit", font=(font, 48), justification="center", pad=((55, 0), (0, 0)))],
    [sg.VerticalSeparator(pad=(0, 10))],
    [sg.Image("logoo.png", size=(200, 200), pad=((95, 0), (0, 0)))],
    [sg.VerticalSeparator(pad=(0, 20))],
    [sg.Text("Tere tulemast!", font=(font, 38), justification="center", pad=((75, 0), (0, 0)))],
    [sg.VerticalSeparator(pad=(0, 50))],
    [sg.Button("Menüü", size=(14, 1), font=(font, 22), button_color=("black", "green"), pad=((106, 0), (0, 0)))]
]

# Create the window
window = sg.Window("Restaurant Kaks Paskalit", layout, size=(400, 600))

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

# Close the window
window.close()

import PySimpleGUI as sg

# Set the theme for the screen
sg.theme("Green")

# Set the font for the layout
font = "Times New Roman"

# Define the layout
layout = [
    [sg.Image("order_delivered.png")]

]

# Create the window
window = sg.Window("Restaurant Kaks Paskalit", layout, size=(400, 700))

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

# Close the window
window.close()

import PySimpleGUI as sg

# Define the window layout
layout = []
for i in range(10):
    layout.append([sg.Text(f'Pizza Pepperoni {i+1}', font=('Helvetica', 20))])
    layout.append([sg.Image(f'pizza pepperoni.png', size=(200, 200), pad=((150,0),(20,20))),
                   sg.Text(f'Picture {i+1} Title', font=('Helvetica', 16), pad=((0,150),(20,20)))])
    layout.append([sg.Checkbox(f'Lisa tellimusele {i+1}', default=True, pad=((150,0),(20,20)))])
layout.append([sg.Button('Send', size=(10, 2), font=('Helvetica', 14), pad=((150,0),(20,20)))])

# Create the window
window = sg.Window('My Window', layout)

# Run the event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Send':
        print('Send button was clicked!')

# Close the window
window.close()

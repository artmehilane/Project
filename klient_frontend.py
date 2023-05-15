import PySimpleGUI as sg
import data_töötlus as dt
#test layout

test_layout = [[sg.Text("tere")]]

# data for the menu to display
data = dt.fe_menu()
filtered_data = data

# list for total order
order = []
items_in_basket = 0

#create the left colmun
left_column = [
    [sg.TabGroup(
        [[
            sg.Text("", text_color="Black", key="logged_in_as"),

            sg.Tab("Drinks", test_layout)]],
            tab_location="centertop",
            title_color="White",
            selected_title_color="White",
            selected_background_color="Black",
            border_width = 5)
    ]]



tab_group_left = [
    [sg.Button("Appetizer", key="-APPETIZER-"), sg.Button("Main Course", key="-MAIN-"), sg.Button("Dessert", key="-DESSERT-"), sg.Button("Drinks", key="-DRINKS-") ],
    [sg.Button("All Menu", key="-ALL-")],
    [sg.Table(values=data, headings=["Item", "Category", "Price"], key="-TABLE-", enable_events=True)],
    [sg.Input(key="-FILTER-", enable_events=True)]
]

tab_group_right = [
    [sg.Image("photos/logo.png",key="-IMAGE-", size=(200,200), pad=((150,0),(20,20)))],
    [sg.Spin(["1", "2", "3", "4", "5"], key="-QUANTITY-"), sg.Button("Add", key="-ADD-")]]


# Define the window layout
welcome_layout = [
    [sg.Text("Tere"), sg.Button("Next", key="-TO_MENU-")]
]


menu_layout = [
    [sg.Text("Kaks Paskalit"), sg.Button("0 items in list", key="-BASKET-")],
    [tab_group_left, tab_group_right],

]

finish_layout = [
    [sg.Text("Your Order")],
    [sg.Button("Back"), sg.Button("Send Order")]
]

layouts = [
    [sg.Column(menu_layout, key="-MENU-", visible=True)],
    [sg.Column(welcome_layout, key="-WELCOME-", visible=False)],
    [sg.Column(finish_layout, key="-ORDER-", visible=False)]
]





# Create the window
window = sg.Window('Kaks Paskalit', menu_layout, size=(400,600))
# Run the event loop
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    #filtri nupud
    elif event == "-APPETIZER-":
        filtered_data = [row for row in data if
                         "appetizer" in row[1].lower()]
        window["-TABLE-"].update(values=filtered_data)
    elif event == "-MAIN-":
        filtered_data = [row for row in data if
                         "main" in row[1].lower()]
        window["-TABLE-"].update(values=filtered_data)
    elif event == "-DESSERT-":
        filtered_data = [row for row in data if
                         "dessert" in row[1].lower()]
        window["-TABLE-"].update(values=filtered_data)
    elif event == "-DRINKS-":
        filtered_data = [row for row in data if
                         "beverages" in row[1].lower()]
        window["-TABLE-"].update(values=filtered_data)
    elif event == "-ALL-":
        filtered_data = data
        window["-TABLE-"].update(values=filtered_data)

    #show the right picture with the food
    elif event == "-TABLE-":
        try:
            selected_row = values["-TABLE-"][0]
            selected_item = filtered_data[selected_row][0].lower()
            selected_item_price = filtered_data[selected_row][2]
            new_picture = "photos/" + selected_item + ".png"
            window["-IMAGE-"].update(filename=new_picture, size=(200,200))
        except:
            pass

    # send order
    elif event == "-ADD-":
        quantity = values["-QUANTITY-"]
        #[name, quant, price, total]
        try:
            add_item = [selected_item,
                        quantity,
                        selected_item_price,
                        float(selected_item_price) * int(quantity)]
            order.append(add_item)

            items_in_basket += int(quantity)
            window["-BASKET-"].update(f"{items_in_basket} items in basket")
        except:
            pass

    elif event == "-TO_MENU-":
        window["-WELCOME-"].update(visible=False)
        window["-MENU-"].update(visible=True)
        window["-ORDER-"].update(visible=False)





# Close the window
window.close()

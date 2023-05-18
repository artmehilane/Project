import PySimpleGUI as sg
import data_töötlus as dt
import os
import datetime

font = "Times New Roman"
sg.theme("Green")
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



# Define the window layout
welcome_layout = [
    [sg.VerticalSeparator(pad=(0, 30))],
    [sg.Text("Kaks Paskalit", font=(font, 48), justification="center", pad=((55, 0), (0, 0)))],
    [sg.VerticalSeparator(pad=(0, 10))],
    [sg.Image("photos/logo.png", size=(200, 200), pad=((95, 0), (0, 0)))],
    [sg.VerticalSeparator(pad=(0, 20))],
    [sg.Text("Tere tulemast!", font=(font, 38), justification="center", pad=((75, 0), (0, 0)))],
    [sg.VerticalSeparator(pad=(0, 50))],
    [sg.Button("Menüü", key="-TO_MENU-", size=(20, 1), font=(font, 24), button_color=("black", "green"), pad=((62, 0), (0, 0)))]
]



menu_layout = [

    [sg.Text("Kaks Paskalit", font=(font, 24), pad = (105,4 ))],
    [sg.Button("Appetizer", key="-APPETIZER-", size=(13,1)), sg.Button("Main Course", key="-MAIN-", size=(13,1)),
     sg.Button("Dessert", key="-DESSERT-", size=(13,1)), sg.Button("Drinks", key="-DRINKS-", size=(13,1))],
    [sg.Button("All Menu", key="-ALL-",pad = (116,12 ) ,size=(16,1))],
    [sg.Table(values=data, headings=["Item", "Category", "Price"], key="-TABLE-", enable_events=True ,font=(font, 14),size=(10,14),justification = "left",pad = (4,8) )],
    [sg.Image("photos/logo.png",key="-IMAGE-", size=(200,200), pad=((72,0),(20,20)))],
    [sg.Spin(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], key="-QUANTITY-",font=(font, 18), size=(18,2)), sg.Button("Add", key="-ADD-", size=(14,1))]

]


end_layout = [
    [sg.Image("photos/order_delivered.png")]
]


order_layout = [
    [sg.Text("Your Order", font=(font, 24))],
    [sg.Table(values=order,
              headings=["Item", "Quantity", "Cost", "Total"],
              font=(font, 14),
              justification="center",
              size=(1000, 30),
              pad=(4, 8),
              key="-ORDER_LIST-",
              enable_events=True,
              col_widths=[100, 100, 100, 100],
              expand_x=True)],  # Set expand_x=True to make the table width span the screen
    [sg.Button("+", key="-MORE-", font=(font, 12), size=(13, 1)),
     sg.Button("-", key="-LESS-", font=(font, 12), size=(13, 1)),
     sg.Button("Remove", key="-REMOVE-", font=(font, 12), size=(13, 1))],
    [sg.Text("", key="-TOTAL_SUM-", visible=False)],
    [sg.Button("Send Order", key="-SEND_ORDER-", font=(font, 12), size=(16, 1))]
]



tab_group = [[sg.TabGroup(
                    [[
                        sg.Tab("MENU", menu_layout, background_color="DarkOliveGreen4", font=(font,18)),
                        sg.Tab("Your Order", order_layout, key="-ORDER_TAB-", font=(font,18))]],
                        tab_location="centertop",
                        title_color="White",
                        selected_title_color="White",
                        selected_background_color="Black",
                        border_width = 5)
            ]]


layouts = [

    [sg.Column(end_layout, key="-DONE-", visible=False)],
    [sg.Column(tab_group, key="-MENU-", visible=False)],
    [sg.Column(welcome_layout, key="-WELCOME-", visible=True)],

]


# Create the window
window = sg.Window('Kaks Paskalit', layouts, size=(400,700))
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
                        int(quantity),
                        selected_item_price,
                        float(selected_item_price) * int(quantity)]
            order.append(add_item)
            window["-ORDER_LIST-"].update(values=order)
        except:
            pass

    # Vahetame "tere" akna "menüü" akna vastu
    elif event == "-TO_MENU-":
        window["-WELCOME-"].update(visible=False)
        window["-MENU-"].update(visible=True)

    # Vastavalt valitud reale saab tooteid juurde lisada
    elif event == "-MORE-":
        try:
            order_row = values["-ORDER_LIST-"][0]
            order[order_row][1] += 1
            order[order_row][3] = order[order_row][1] * order[order_row][2]
            window["-ORDER_LIST-"].update(values=order)
        except:
            pass

    # Vastavalt valitud reale saab tooteid vähendada
    elif event == "-LESS-":
        try:
            order_row = values["-ORDER_LIST-"][0]
            order[order_row][1] -= 1
            order[order_row][3] = order[order_row][1] * order[order_row][2]
            window["-ORDER_LIST-"].update(values=order)

            #Vaatame kas tooteid on nüüd 0, kui on küsime kas tahadki ja kui jah siis eemaldame toote
            for item in order:
                if item[1] == 0:
                    response = sg.popup_yes_no("Are you sure you want to remove this item?", font=(font,14))
                    if response == "Yes":
                        order.pop(order_row)
                    else:
                        order[order_row][1] = 1
                        order[order_row][3] = order[order_row][1] * order[order_row][2]
            window["-ORDER_LIST-"].update(values=order)
        except:
            pass

    # Vastavalt valitud reale saab tooteid eemaldada
    elif event == "-REMOVE-":
        try:
            order_row = values["-ORDER_LIST-"][0]
            order.pop(order_row)
            print(order)
            window["-ORDER_LIST-"].update(values=order)
        except:
            pass

    #Orderi saatmine ja arve tegemine
    elif event == "-SEND_ORDER-":
        if len(order) > 0:
            response = sg.popup_yes_no("Are you sure you got everything?", font=(font, 18))
            if response == "Yes":
                window["-MENU-"].update(visible=False)
                window["-DONE-"].update(visible=True)
                #loome arve
                dir_list = os.listdir("arved")

                # Get the current date and time
                current_datetime = datetime.datetime.now()
                current_date = current_datetime.date()
                current_time = datetime.datetime.now().time().strftime("%H:%M")
                current_time = current_time.replace(":","-")

                order_ID = 1001 + len(dir_list)
                file_ID = str(order_ID) + "_" + str(current_date) + "_" + current_time
                print(order_ID)
                #Siin me päriselt loome arve
                with open(f"arved/{file_ID}", "w") as file:
                    file.write(f"---------ORDER NR: {order_ID}-----------\n")
                    file.write("ITEM      QUANTITY       PRICE      TOTAL\n")
                    for item in order:
                        file.write(f"{item[0]:13s}{str(item[1]):12s}{str(item[2]):11s}{str(item[3]):10s}\n")
                    file.write("-----------------------------------------\n")
                    file.write(f"TOTAL: {total_sum}\n\n")
                    file.write("          Kaks Paskalit\n")

        else:
            sg.popup("You need to have items in order!")



   # üldine item counter, kuna kohti kus see muutub on mitu siis on hea kui on üks koht mis jälgib
    items_in_basket = 0
    total_sum = 0
    for item in order:
        items_in_basket += item[1]
        total_sum += item[3]
    window["-ORDER_TAB-"].update(f"Your Order ({items_in_basket})")
    if len(order) >= 0:
        window["-TOTAL_SUM-"].update(f"Your Total is: {total_sum} $", font=(font, 18))
        round(total_sum,2)
        window["-TOTAL_SUM-"].update(visible=True)
    else:
        window["-TOTAL_SUM-"].update(visible=False)















# Close the window
window.close()

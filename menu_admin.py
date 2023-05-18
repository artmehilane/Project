import PySimpleGUI as sg
import login
import data_töötlus
import os
import datetime

def arved_to_format(listike):
    arved = []
    for item in listike:
        item = item.split("_")
        arved.append(item)
    return arved

username = ""
food_picture = ""

sg.theme("Green")  # set the color theme for the window

# create the layout for the menu window
login_layout = [
    [sg.Text("Please log in!", font=("Arial", 20))],
    [sg.Text("Enter Username:"), sg.Input(key="username")],
    [sg.Text("Enter Password:"), sg.Input(key="password", password_char="*")],
    [sg.Text("", key="login_error")],
    [sg.Button("Log in", size=(20, 2))],
]

home_layout = [
    [sg.Text("HOME")],
    [sg.Frame("Last week statistics", [
        [sg.Text("Text", key="7_days_sum")],
        [sg.Text("Best", key="7_days_popular")],
        [sg.Text("Best", key="7_days_most_money")],
        [sg.Text("Orders", key="7_days_orders")],
        [sg.Button("refresh")]
     ])]
]

settings_layout = [
    [sg.Text("SETTINGS")],
    [sg.Text("Add new account")],
    [sg.Text("Enter username"), sg.Input(key="new_username")],
    [sg.Text("Enter Password"), sg.Input(key="new_password")],
    [sg.Text("Password again"), sg.Input(key="password_check")],
    [sg.Text("", key="new_account_message")],
    [sg.Button("Create Account", size=(20,2))]
]

# Define the data for the listbox
path = "data/menu.xlsx"
data_menu = data_töötlus.read_menu(path)
on_menu = []
off_menu = []

menu_headings = ["ID", "Item", "Category", "Sub", "Price"]
for item in data_menu:
    if item[5] == True:
        on_menu.append(item)
    else:
        off_menu.append(item)


menu_layout = [
    [sg.Text("MENU")],
    [sg.Table(values=on_menu,
              headings=menu_headings,
              auto_size_columns=True,
              justification='center',
              alternating_row_color='lightblue',
              key='-MENU-')],
    [sg.Table(values=off_menu, headings=menu_headings, key="off_the_menu", auto_size_columns=True, justification='center', size=(None, 7))],
    [sg.Button("Edit", size=(10,2)),
     sg.Button("Out of Stock", size=(10,2)),
     sg.Button("Back in the menu!", size=(10,2)),
     sg.Button("Delete item", size=(10,2)),
     sg.Button("Add new item", size=(10,2))]

]

cat_options = ["Food", "Drink"]
subfood_options = ["Appetizer", "Main Course", "Dessert"]
subdrink_options = ["Soft Drink", "Alcohol", "Juice"]

new_item_layout = [
    [sg.Text("Add a new item to the menu")],
    [sg.Frame("Item Info", [
        [sg.Text("Name of the item"), sg.Input(key="new_item_name")],
        [sg.Text("Choose the category"), sg.Combo(cat_options, size=(20,1), key="new_item_cat")],
        [sg.Text("Choose the subcategory"), sg.Combo(subfood_options, size=(20,1), key="new_item_subcat")],
        [sg.Text("Price in €"), sg.Input(key="new_item_price")],
        [sg.Text("Please choose a picture for the new item")],
        [sg.Button("Choose file"), sg.Text(f"selected : ", key="selected_file", visible=False)]
    ])],
    [sg.Button("Add item to menu"), sg.Text("", key="add_item_status", visible=False)],
    [sg.Button("Back to menu")]
]

arved_raw = os.listdir("arved")
arved_headings = ["ID", "Date", "Time"]
all_arved = arved_to_format(arved_raw)
arved = all_arved

aastad = [2023, 2024]
kuud = ["01","02","03","04","05","06","07","08","09","10","11","12"]
paevad = ["1","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]

arved_layout = [
    [sg.Text("ARVED")],
    [sg.Button("Filter", key="filter_arved"),
     sg.Combo(aastad, default_value="YEAR", key="year"),
     sg.Combo(kuud, default_value="MONTH", key="month"),
     sg.Combo(paevad, default_value="DAY", key="day")],
    [sg.Table(values=arved, headings=arved_headings, enable_events=True, key="valitud_arve"),
    sg.Frame("Check",
              [[sg.Text("ITEM      QUANTITY       PRICE      TOTAL\n", key="arve_text")],
               [sg.InputText(key="comment")],
               [sg.Button("Add Comment", key="add_comment")]]
              )]
]


"""
Kui tahad uue tabi listi lisada, siis sg.Tab(tabi nimi, tabi layout)"""
tab_group = [
                [sg.TabGroup(
                    [[
                        sg.Text("", text_color="Black", key="logged_in_as"),
                        sg.Tab("Home", home_layout, background_color="teal"),
                        sg.Tab("Settings", settings_layout),
                        sg.Tab("Menu", menu_layout),
                        sg.Tab("Arved", arved_layout, key="-ARVED-")]],

                        tab_location="centertop",
                        title_color="White",
                        selected_title_color="White",
                        selected_background_color="Black",
                        border_width = 5)
            ]]

program_layout = [
]
#login ja programm layout switch
layouts = [
    [sg.Column(login_layout, key="_LOGIN_LAYOUT_"),
    sg.Column(tab_group, key="_TAB_LAYOUT_"),
    sg.Column(new_item_layout, key="_NEW_ITEM_LAYOUT_")]
]











# create the menu window
window = sg.Window("Menu", layouts, size=(550, 500), element_justification="center")

# create a loop to handle events
while True:
    event, values = window.read()

    # if the user clicks the "X" button in the top right corner, close the window
    if event == sg.WIN_CLOSED:
        break

    """Kui ma vajutan login nuppu siis vaatab kas selline username ja salasõna on olemas.
    Kui on korras, siis lülitab login vaate välja ja avab programmi vaate"""
    if event == "Log in":
        username = values["username"]
        password = values["password"]
        try:
            login.Log_in(username, password)
            window["logged_in_as"].update(f"Logged in as: {username}")
            window["_LOGIN_LAYOUT_"].update(visible=False)
            window["_TAB_LAYOUT_"].update(visible=True)
        except:
            window["login_error"].update("Wrong username or password!")

    elif event == "Create Account":
        new_username = values["new_username"]
        new_password = values["new_password"]
        password_check = values["password_check"]

        if new_password == password_check and len(new_password) > 4:
            try:
                login.New_User(new_username, new_password)
                window["new_account_message"].update("New user added!")
            except:
                window["new_account_message"].update("Username already in use")
        elif new_password != password_check:
            window["new_account_message"].update("Passwords dont match!")
        else:
            window["new_account_message"].update("Password must be atleast 5 characters")

    elif event == "Add new item":
        window["_TAB_LAYOUT_"].update(visible=False)
        window["_NEW_ITEM_LAYOUT_"].update(visible=True)


    elif event == "Add item to menu":

        new_item_name = values["new_item_name"]
        new_item_cat = values["new_item_cat"]
        new_item_subcat = values["new_item_subcat"]
        new_item_price = values["new_item_price"]
        new_item_pic = food_picture
        new_item_message = data_töötlus.new_item(new_item_name,
                                                  new_item_cat,
                                                  new_item_subcat,
                                                  new_item_price,
                                                  new_item_pic)
        data = data_töötlus.read_menu(path)
        off_menu = []
        for item in data:
            if item[5] == False:
                off_menu.append(item)
        window['off_the_menu'].update(values=off_menu)
        window["add_item_status"].update(new_item_message, visible=True)
        data_töötlus.add_item_to_arved_excel(new_item_name)

    elif event == "Back to menu":
        window["_TAB_LAYOUT_"].update(visible=True)
        window["_NEW_ITEM_LAYOUT_"].update(visible=False)

    elif event == "valitud_arve":
        try:
            selected_row = values["valitud_arve"][0]
            selected_arve = arved[selected_row][0]
            check_name = ""
            for item in arved_raw:
                if item.startswith(selected_arve):
                    check_name = item
            filename = "arved/" + check_name
            with open(filename, "r") as arve:
                contents = arve.read()
                arve.close()
            window["arve_text"].update(contents)
        except:
            pass


    elif event == "add_comment":
        comment = values["comment"]
        if len(comment) >= 3:
            comment = data_töötlus.format_column_text(comment, 30)
            current_datetime = datetime.datetime.now()
            current_date = current_datetime.date()
            add = f"{username} // {current_date}: {comment}\n"
            with open(filename, "a") as arve:
                arve.write(add)
                arve.close()
            with open(filename, "r") as arve:
                updated_contents = arve.read()
                arve.close()
            window["arve_text"].update(updated_contents)

    elif event == "filter_arved":
        year = "year"
        month = "month"
        day = "day"
        filter_format = [False, False, False]

        try:
            if int(values["year"]) > 2022:
                year = str(values["year"])
                filter_format[0] = True
        except:
            filter_format[0] = False

        try:
            if 0 < int(values["month"]) <= 12:
                month = values["month"]
                filter_format[1] = True
        except:
            filter_format[1] = False

        try:
            if 0 < int(values["day"
                              ""]) <= 31:
                day = values["day"]
                filter_format[2] = True
        except:
            filter_format[2] = False

        print(filter_format)
        print(year, month, day)
        filtered_arved = []
        if True in filter_format:
            for arve in all_arved:
                arve_listina = arve[1].split("-")
                if filter_format[0] == True and filter_format[1] == True and filter_format[2] == True:
                    if arve_listina[0] == year and arve_listina[1] == month and arve_listina[2] == day:
                        filtered_arved.append(arve)
                elif filter_format[0] == True and filter_format[1] == True and filter_format[2] == False:
                    if arve_listina[0] == year and arve_listina[1] == month:
                        filtered_arved.append(arve)
                elif filter_format[0] == True and filter_format[1] == False and filter_format[2] == True:
                    if arve_listina[0] == year and arve_listina[2] == day:
                        filtered_arved.append(arve)
                elif filter_format[0] == False and filter_format[1] == True and filter_format[2] == True:
                    if arve_listina[1] == month and arve_listina[2] == day:
                        filtered_arved.append(arve)
                elif filter_format[0] == False and filter_format[1] == False and filter_format[2] == True:
                    if arve_listina[2] == day:
                        filtered_arved.append(arve)
                elif filter_format[0] == True and filter_format[1] == False and filter_format[2] == False:
                    if arve_listina[0] == year:
                        filtered_arved.append(arve)
                elif filter_format[0] == False and filter_format[1] == True and filter_format[2] == False:
                    if arve_listina[1] == month :
                        filtered_arved.append(arve)
            arved = filtered_arved
            print(arved, filtered_arved)
        else:
            arved = all_arved

        window["valitud_arve"].update(values=arved)

    elif event == "Out of Stock":
        try:
            selected_row = values["-MENU-"][0]
            selected_food = on_menu[selected_row][0]
            for i in range(len(on_menu)):
                if on_menu[i][0] == selected_food:
                    food_in_trasnfer = on_menu[i]
                    food_in_trasnfer[5] = False
                    on_menu.pop(i)
                    off_menu.append(food_in_trasnfer)
                    data_töötlus.on_off_menu(selected_food)
                    window["-MENU-"].update(values=on_menu)
                    window["off_the_menu"].update(values=off_menu)
                    break
        except:
            pass

    elif event == "Back in the menu!":
        try:
            selected_row = values["off_the_menu"][0]
            selected_food = off_menu[selected_row][0]
            for i in range(len(off_menu)):
                if off_menu[i][0] == selected_food:
                    food_in_trasnfer = off_menu[i]
                    food_in_trasnfer[5] = True
                    off_menu.pop(i)
                    on_menu.append(food_in_trasnfer)
                    data_töötlus.on_off_menu(selected_food)
                    window["-MENU-"].update(values=on_menu)
                    window["off_the_menu"].update(values=off_menu)
                    break
        except:
            pass

    elif event == "Delete item":
        # et itemit kustutada peab see olema off menu
        to_delete = 0
        try:
            selected_row = values["off_the_menu"][0]
            selected_food = off_menu[selected_row][0]
            if selected_food >= 1:
                for item in data_menu:
                    if selected_food == item[0]:
                        item_name = item[1]
                        delete = sg.popup_yes_no(f"Are you sure you want to delete: \n {item_name}")
                        if delete == "Yes":

                            data_töötlus.delete_food(selected_food)
                            for item in off_menu:
                                if item[0] == selected_food:
                                    off_menu.remove(item)
                                    window["off_the_menu"].update(values=off_menu)
        except:
            pass

    elif event == "Edit":
        try:
            selected_row = values["off_the_menu"][0]
            selected_food = off_menu[selected_row][0]
            if selected_food >= 1:
                for item in data_menu:
                    if selected_food == item[0]:
                        item_name = item[1]
                        new_price = sg.popup_get_text( f"Enter a new price for the {item_name}", f"Edit: {item_name}")
                        try:
                            item[4] = float(new_price)
                            data_töötlus.edit_price(item[0], new_price)
                            for i in range(len(off_menu)):
                                if off_menu[i][0] == selected_food:
                                    off_menu[i][4] = new_price
                                    window["off_the_menu"].update(values=off_menu)
                                    break
                        except:
                            sg.popup("Enter a number like 12.55")
                        break
        except:
            pass

    elif event == "Choose file":
        food_picture = sg.popup_get_file("Select a .PNG for your item")
        if food_picture.endswith(".PNG") or food_picture.endswith(".png"):
            pic_name = food_picture.split("/")
            pic_name = pic_name[-1]
            window["selected_file"].update(f"Selected: {pic_name}", visible=True)
        else:
            sg.popup("Need a PNG file")
            food_picture = ""
    elif event == "refresh":
        pass

    last_week_sum = data_töötlus.seven_days()
    window["7_days_sum"].update(f"Last week total: {last_week_sum[0]} €")
    window["7_days_popular"].update(f"Last week hit was {last_week_sum[1][1]} with {last_week_sum[1][0]} sales")
    window["7_days_most_money"].update(f"Most profitable item was {last_week_sum[2][1]} with total of {last_week_sum[2][0]} €")
    window["7_days_orders"].update(f"Total number of orders: {last_week_sum[3]}")



# close the window
window.close()
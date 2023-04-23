import PySimpleGUI as sg
import login

username = ""

sg.theme("DefaultNoMoreNagging")  # set the color theme for the window

# create the layout for the menu window
login_layout = [
    [sg.Text("Please log in!", font=("Arial", 20))],
    [sg.Text("Enter Username:"), sg.Input(key="username")],
    [sg.Text("Enter Password:"), sg.Input(key="password", password_char="*")],
    [sg.Text("", key="login_error")],
    [sg.Button("Log in", size=(20, 2))],
]

home_layout = [
    sg.Text("HOME")
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

"""
Kui tahad uue tabi listi lisada, siis sg.Tab(tabi nimi, tabi layout)"""
tab_group = [
                [sg.TabGroup(
                    [[
                        sg.Text("", text_color="Black", key="logged_in_as"),
                        sg.Tab("Home", home_layout, background_color="teal"),
                        sg.Tab("Settings", settings_layout)]],
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
    sg.Column(tab_group, key="_TAB_LAYOUT_")]
]











# create the menu window
window = sg.Window("Menu", layouts, size=(400, 300), element_justification="center")

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

    if event == "Create Account":
        new_username = values["new_username"]
        new_password = values["new_password"]
        password_check = values["password_check"]

        if new_password == password_check:
            try:
                login.New_User(new_username, new_password)
                window["new_account_message"].update("New user added!")
            except:
                window["new_account_message"].update("Username already in use")
        else:
            window["new_account_message"].update("Passwords dont match!")


# close the window
window.close()




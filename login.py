def New_User():
    data = []
    is_name_ok = False
    is_pass_ok = False

    #avame faili kus on kogu login info sees
    with open('data/login_data.txt', 'r+') as f:
        for line in f:
            user = line.rstrip("\n").split(":")
            data.append(user)
        print(data)
        f.close()

    while True:
        is_name_taken = False
        #Küsime kasutajalt uue konto nime ja salasõna
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")

        #Vaatame kas nendes on ainult tähed ja numbrid
        is_name_ok = username.isalnum()
        is_pass_ok = password.isalnum()

        #Vaatame kas selline username juba olemas
        for usersdata in data:
            if usersdata[0] == username:
                is_name_taken = True
                break

        #Palume teha muudatused mis ei sobi ja kui kõik ok siis liigume edasi
        if is_name_ok == False:
            print("chage username")
        if is_name_taken == True:
            print("This name is already taken")
            is_name_ok = False
        if is_pass_ok == False:
            print("change password")
        if is_name_ok and is_pass_ok:
            print("user successfully added!")
            break

    #Kui kõik on korras siis lisame uue kasutaja faili
    new_data = "\n" + username + ":" + password
    with open('data/login_data.txt', 'a') as f:
        f.write(new_data)
    f.close()

def Log_in():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    user_ok = False
    data = []

    # avame faili kus on kogu login info sees
    with open('data/login_data.txt', 'r') as f:
        for line in f:
            user = line.rstrip("\n").split(":")
            data.append(user)
        f.close()

    #Vaatame kas on konto millel on sama username ja password
    for user in data:
        if username == user[0] and password == user[1]:
            user_ok = True
            print("YOU ARE LOGGED IN!")
            break

    #Prindime et sellsit comot ei ole ja laseme uuesti sisestada
    if not user_ok:
        print("Username or password incorrect")
        Log_in()

Log_in()
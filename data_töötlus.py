import pandas as pd
import openpyxl
import shutil
import os
import datetime

def read_menu(path):
    df = pd.read_excel(path)
    rows_list = df.values.tolist()
    return (rows_list)

def new_item(name, cat, subcat, price, pic):
    item_name = name
    item_cat = cat
    item_subcat = subcat
    item_price = price
    item_pic = pic
    pic_name = pic.split("/")
    pic_name = pic_name[-1]





    df = pd.read_excel("data/menu.xlsx")
    rows = df.values.tolist()

    # Vaatame kas kõik välja õigesti täidetud
    if len(item_name) == 0:
        return("Item needs a name")
    elif len(item_cat) == 0:
        return("Item needs a category")
    elif len(item_subcat) == 0:
        return("Item needs a subcategory")
    elif len(item_price) <= 0:
        return("Item needs a price")
    elif len(item_pic) <= 4:
        return("Item needs a picture")


    # Vaatame, et sellist toodet ei oleks juba
    for item in rows:
        if item_name == item[1]:
            return("Item already in the menu")

    destination_file = "photos/" + item_name.lower() + ".png"
    shutil.copy(item_pic, destination_file)

    # anname toidule ID
    items_in_menu = len(rows)
    if item_cat == "Food":
        item_id = 1000 + items_in_menu + 1
    else:
        item_id = 2000 + items_in_menu + 1

    new_line = [item_id, item_name, item_cat, item_subcat, item_price, False]
    # Convert the new line to a DataFrame
    df.loc[len(df)] = new_line
    df.to_excel("data/menu.xlsx", index=False)
    return("New item successfully added")


path = "data/menu.xls"

read_menu(path)

path = "data/menu.xlsx"

#menu to display in frontend view
def fe_menu():
    data = read_menu("data/menu.xlsx")
    processed_data = []
    for item in data:
        if item[5] == True:
            item = [item[1], item[3], item[4]]
            processed_data.append(item)
    return processed_data


#abifunktsioon texti formatimiseks
def format_column_text(text, line_length):
    lines = []
    current_line = ""
    words = text.split()

    for word in words:
        if len(current_line) + len(word) + 1 <= line_length:
            current_line += word + " "
        else:
            lines.append(current_line)
            current_line = word + " "

    if current_line:
        lines.append(current_line)

    formatted_text = "\n".join(lines)
    return formatted_text

def is_substring_in_range(text, substring, start_index, end_index):
    if substring in text[start_index:end_index]:
        return True
    else:
        return False

def on_off_menu(itemID):
    data = read_menu("data/menu.xlsx")
    for item in data:
        if itemID == item[0]:
            if item[5] == True:
                item[5] = False
            else:
                item[5] = True

    data_df = pd.DataFrame(data)
    data_df.to_excel("data/menu.xlsx", index=False)
    print(data)

def delete_food(itemID):
    data = read_menu("data/menu.xlsx")
    for i in range(len(data)):
        if itemID == data[i][0]:
            data.pop(i)
            break

    data_df = pd.DataFrame(data)
    data_df.to_excel("data/menu.xlsx", index=False)
    return None

def edit_price(itemID, new_price):
    data = read_menu("data/menu.xlsx")
    for i in range(len(data)):
        if itemID == data[i][0]:
            data[i][4] = new_price
            break
    data_df = pd.DataFrame(data)
    data_df.to_excel("data/menu.xlsx", index=False)
    return None

def seven_days():
    arved_raw = os.listdir("arved")
    arved_to_show = []
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.date()
    current_date = str(current_date).split("-")

    #Filtreerime eelmise 7 päeva arved
    for i in range(len(arved_raw)):
        if is_substring_in_range(arved_raw[i], current_date[0], 4, 9):
            if is_substring_in_range(arved_raw[i], current_date[1], 8, 12):
                if int(current_date[2]) - 7 < int(arved_raw[i][13:15]) <= int(current_date[2]):
                    arveID = arved_raw[i].split("_")
                    arveID = arveID[0]
                    arved_to_show.append(arveID)

    #Loome listi arvetest ja nende sisudest viimase 7 päeva jooksul
    df = pd.read_excel('data/arved.xlsx')
    # List of values to filter
    for i in range(len(arved_to_show)):
        arved_to_show[i] = int(arved_to_show[i])
    filter_values = arved_to_show
    # Filter the DataFrame based on the first element of each row
    filtered_rows = df[df['---'].isin(filter_values)]
    filtered_rows = filtered_rows.values.tolist()

    item_names = df.columns.tolist()
    item_names.pop(0)
    total_items = [0] * (len(item_names))

    menu_df = pd.read_excel("data/menu.xlsx")
    item_prices = menu_df.values.tolist()
    for i in range(len(item_prices)):
        item_prices[i] = [item_prices[i][1] , item_prices[i][4]]

    i = 0
    total_sum = 0
    suurim_column_sum = 0
    suurim_column_sum_nimi = ""
    most_money = 0
    most_money_nimi = ""
    for item in item_names:
        if item.lower() == item_prices[i][0].lower():
            item_price = item_prices[i][1]
        column_sum = df[f'{item}'].sum()
        total_items[i] = [item, column_sum, item_price, item_price * column_sum]
        i += 1
        #arvutame kogu summa
        total_sum +=  item_price * column_sum
        total_sum = round(total_sum, 2)
        #arvutame kõige pop toote
        if column_sum > suurim_column_sum:
            suurim_column_sum = column_sum
            suurim_column_sum_nimi = item
        #arvutame enim raha teeninud toote
        if item_price * column_sum > most_money:
            most_money = item_price * column_sum
            most_money_nimi = item

    # returnime list [kokku_raha, [enim müüdud toode, kogus], [kõige rohkem raha teeninud toode, kogus], orderied kokku]
    return [total_sum, [suurim_column_sum, suurim_column_sum_nimi], [round(most_money,2), most_money_nimi],len(filtered_rows)]


def order_to_excel(info, orderID):
    #info on list [['soft drink', 1, 2.99, 2.99], ['pizza', 1, 14.99, 14.99], ['ice cream', 3, 6.99, 20.97]]
    filepath = "data/menu.xlsx"
    df = pd.read_excel(filepath)
    df = df.values.tolist()
    headings = ["---"]
    for item in df:
        headings.append(item[1])

    first_line = headings

    new_line = [0] * len(headings)
    new_line[0] = orderID
    for item in info:
        for i in range(len(headings)):
            if item[0] == headings[i].lower():
                new_line[i] += item[1]

    arved_df = pd.read_excel('data/arved.xlsx')
    # Convert DataFrame to a list of lists
    data_list = arved_df.values.tolist()

    data_list.append(new_line)

    # Convert the updated list back to a DataFrame
    updated_df = pd.DataFrame(data_list, columns=arved_df.columns)

    # Write the DataFrame to a new Excel file
    updated_df.to_excel('data/arved.xlsx', index=False)

def add_item_to_arved_excel(item_name):
    df = pd.read_excel('data/arved.xlsx')
    arveid_kokku = len(df.values.tolist())

    # Add a new column with values
    df[item_name] = [0] * arveid_kokku

    # Write the DataFrame to a new Excel file
    df.to_excel('data/arved.xlsx', index=False)













import pandas as pd
import openpyxl

def read_menu(path):
    df = pd.read_excel(path)
    rows_list = df.values.tolist()
    return (rows_list)

def new_item(name, cat, subcat, price):
    item_name = name
    item_cat = cat
    item_subcat = subcat
    item_price = price

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


    # Vaatame, et sellist toodet ei oleks juba
    for item in rows:
        if item_name == item[1]:
            return("Item already in the menu")

    # anname toidule ID
    items_in_menu = len(rows)
    if item_cat == "Food":
        item_id = 1000 + items_in_menu + 1
    else:
        item_id = 2000 + items_in_menu + 1

    item_data = {"ID" : item_id,
                 "NAME" :item_name,
                "CATEGORY" : item_cat,
                "SUBCATEGORY" : item_subcat,
                "PRICE" : item_price,
                "AVAILABLE" : False
                 }

    new_df = pd.DataFrame(item_data, index = [0])
    df = pd.concat([df, new_df], ignore_index = True)
    print(df)
    df.to_excel("data/menu.xlsx")
    return("New item successfully added")


path = "data/menu.xls"

read_menu(path)

path = "data/menu.xlsx"

def fe_menu():
    data = read_menu("data/menu.xlsx")
    processed_data = []
    for item in data:
        if item[5] == True:
            item = [item[1], item[3], item[4]]
            processed_data.append(item)
    return processed_data






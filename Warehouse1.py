from item import item
from menu import print_menu
import datetime
import pickle
import os

logs = []
items = []
id_count = 0
items_file = "items.data"
logs_file = 'logs.data'

def clear():
    return os.system('cleared')

def get_time():
    current_date = datetime.datetime.now()
    time = current_date.strftime('%X')
    return time

def save_items():
    writer = open(items_file, 'wb') # wb writes binary info
    pickle.dump(items, writer)
    writer.close()
    print('Data saved')

def save_log():
    writer = open(logs_file, 'wb') # wb = write binary info
    pickle.dump(logs, writer)
    writer.close()
    print('Log saved')
    
def read_items():
    global id_count #import variable into fn scope

    try:
        reader = open(items_file, 'rb') #rb = open the file to read
        temp_list = pickle.load(reader)

        for item in temp_list:
            items.append(item)
    except:
        # you get here if try block crash
        print('Error: data can not be loaded')

def read_log():
    try:
        reader = open(logs_file, 'rb') #rb = open the file to read
        temp_list = pickle.load(reader)

        for log in temp_list:
            logs.append(log)
    except:
        # you get here if try block crash
        print('Error: data can not be loaded')

def add_log(action,title,id):
    global logs
    log_line = str(get_time()) + ' | ' + str(action) + ' | ' + str(title) + ' | ' + str(id)
    logs.append(log_line)
   
def event_log():
    print_header('Logs')
    print('|Date        |Action        |Name        |Id')
    for log in logs:
        print(str(log))
        

def print_header(text):
    print('\n\n')
    print('*'*40)
    print(text)
    print('*'*40)

def register_item():
    # import global variable
    global id_count
    
    # validations 
    print_header('Register New Item')
    title = input('input the item name: ')
    category = input('input the item\'s category: ')
    price = float(input('input the price of the item: '))
    stock = int(input('input the items quantity in stock: '))

    if len(items) == 0:
        id_count = 0
    if len(items) > 0:
        id_count = len(items)

    new_item = item()
    new_item.id = id_count
    new_item.title = title
    new_item.category = category
    new_item.price = price
    new_item.stock = stock
    items.append(new_item)
    add_log('Item registered', title, id_count)
    save_log()
    print('Item Created')
    print(len(items))


def list_items(header_text):
    if(len(items) <= 0 ):
        print_header('Inventory Is Empty')

    else:
        print_header(header_text)
        print('id  | title        | category    | price | in stock   ')
        for item in items:
            print(str(item.id).ljust(4) + '|' + item.title.ljust(14) + '|' + item.category.ljust(10) + '|'  + str(item.price).rjust(9) + '|'  + str(item.stock).rjust(4))


def update_stock(inStock):
    if(len(items) <= 0 ):
        list_items('Inventory Is Empty')

    else:    
        #show the user all the items
        if(inStock == 'true'):
            list_items('Item Inventory')
        #ask for ID
        id = input('\n Choose item by id: ')
        # get array
        found = False

        for item in items:

            if(inStock == 'true'):
                if(str(item.id) == id):
                    new_stock = (input('update ' + item.title + ' stock: '))
                    item.stock = int(new_stock)
                    list_items('Item Inventory')
                    print('\n' + item.title + ' stock was updated')
                    add_log('Stock updated', item.title, item.id)
                    save_items()
                    save_log()
                    found = True


                    if(not found):
                        print('Error: ID doesnt exist, try again')

            elif(inStock == 'false'):
                if(str(item.id) == id):
                    new_stock = (input('\n update ' + item.title + ' stock: '))
                    item.stock = int(new_stock)

                    print_header('Updated Items')
                    print('id  | title        | category    | price | in stock   ')
                    print(str(item.id).ljust(4) + '|' + item.title.ljust(14) + '|' + item.category.ljust(10) + '|'  + str(item.price).rjust(9) + '|'  + str(item.stock).rjust(4))

                    print('\n' + item.title + ' stock was updated')
                    add_log('Stock updated', item.title, item.id)
                    save_items()
                    save_log()
                    found = True

                    if(not found):
                        print('Error: ID doesnt exist, try again')

def not_in_stock():
    
    if(len(items) <= 0 ):
        print_header('Inventory Is Empty')
    
    else: 
        # show all items with no stock
        print_header('Items Not In Stock')
        print('id  | title        | category    | price | in stock   ')
        for item in items:

            if (item.stock == 0):
                print(str(item.id).ljust(4) + '|' + item.title.ljust(14) + '|' + item.category.ljust(10) + '|'  + str(item.price).rjust(9) + '|'  + str(item.stock).rjust(4))
                ask = input('\n Update Stock? y/n: ')
                if(ask == 'y'):
                    update_stock('false')

                else:
                    continue


def delete_item():
    if(len(items) <= 0 ):
        list_items('Inventory Is Empty')

    else:
        #show list
        list_items('Item Inventory')
        #ask for id
        id = int(input('\n input the item ID to delete: '))
        #get array
        for item in items:
            if(item.id == id):
                items.remove(item)
                list_items('Item Inventory')
                print('\n' + item.title + ' has been deleted')
                add_log('Item deleted', item.title, item.id)
                save_items()
                save_log()

def print_category():
    cat_arr = []

    print_header('Item Categories')
    for item in items:
        if(item.category not in cat_arr):
            print(str(item.category))
            cat_arr.append(str(item.category))

    cat = input('\n select category: ')

    print_header('Items in the ' + str(cat) + ' category')
    print('id  | title        | category    | price | in stock   ')
    for item in items:
        if(str(item.category) == cat):
            print(str(item.id).ljust(4) + '|' + item.title.ljust(14) + '|' + item.category.ljust(10) + '|'  + str(item.price).rjust(9) + '|'  + str(item.stock).rjust(4))
            
def stock_value():
    total = 0
    last_item = items[-1]
    for item in items:
        item_sum = item.price * item.stock
        total += item_sum
        
        if(item.id == last_item.id):
            print('\n The total stock value is $' + str(total))
            add_log('Stock value', str(total),0)
            save_log()

def register_purchase():
    '''
    Show the items
    ask the user to select 1
    ask for thr quantity in the order (purchase)
    update the stock of the selected item
    '''
    list_items('Item Inventory')
    
    option = input('select a item by id: ')
    found = False
    for item in items:
        if(int(option) == item.id):
            quantity = input('how many ' + str(item.title) + ' would you like to purchase? ')
            item.stock -= int(quantity)
            found = True
            add_log('Item purchased', item.title, item.id)
            save_items()
            save_log()
            print('\n' + item.title + ' Inventory updated')

    if(not found):
        print('error cannot find item')

def register_sell():
    list_items('Item Inventory')
    option = input('select a item by id: ')
    found = False
    for item in items:
        if(int(option) == item.id):
                quantity = input('how many ' + str(item.title) + ' would you like to sell? ')
                item.stock += int(quantity)
                found = True
                add_log('Registered seller item', item.title, item.id)
                save_items()
                save_log()
                print('\n' + item.title + ' stock has been updated')    

    if(not found):
        print('Error: cannot find item')

read_log()
read_items()

opc = ''
while(opc != 'x'):
    clear()
    print('-'*40)
    print_menu()
    
    opc = input('\n please select a option: ')

    # actions based on a selected option

    if(opc == '1'):
        register_item()
        save_items()
    elif(opc == '2'):
        list_items('Item Inventory')
    elif(opc == '3'):
        update_stock('true')
    elif(opc == '4'):
        not_in_stock()
    elif(opc == '5'):
        print_category()
    elif(opc == '6'):
        delete_item()
    elif(opc == '7'):
        stock_value()
    elif(opc == '8'):
        register_purchase()
    elif(opc == '9'):
        register_sell()
    elif(opc == '10'):
        event_log()

    if(opc != 'x'):
        input('\n\n Press Enter To Continue...')
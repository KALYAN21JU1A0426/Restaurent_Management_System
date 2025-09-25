import mysql.connector as db
con=db.connect(user='root',
               password='Mysql@2003',
               host='localhost',
               database='project')


def menu_items():
    cur=con.cursor()
    cur.execute('select * from menu_card')
    data=cur.fetchall()
    for i in data:
        print(i[0],'-',i[1],'-',i[2],'-',i[3],'rs')
    cur.close()
def add_items():
    cur=con.cursor()
    ch=input("do you want to add new items(yes\no): ")
    if ch=="yes":
        item_id=int(input("enter item_id: "))
        items=input("enter an item: ")
        category=input("enter a category: ")
        price=float(input("enter item price: "))
        cur.execute("insert into menu_card(item_id,items,category,price)values(%s,%s,%s,%s)",(item_id,items,category,price))
        con.commit()
        print("item added sucessfully")
    elif ch=="no":
        print("no more items to add")
    else:
        print("choose the correct one")
    cur.close()
def delete_item():
    cur=con.cursor()
    item_id=int(input("what item id do you want to delete: "))
    cur.execute('select * from menu_card where item_id=%s',(item_id,))
    data=cur.fetchone()
    if data:
        confirm=input("do you want to delete the item(yes\no): ")
        if confirm=="yes":
            cur.execute("delete from menu_card where item_id=%s",(item_id,))
            con.commit()
            print("item deleted sucessfully")
        else:
            print("deletion cancelled")                             
    else:
        print("no item id found")
    cur.close()
def modify_item():
    cur=con.cursor()
    item_id=int(input("which item do you want to modify: "))
    cur.execute('select * from menu_card where item_id=%s',(item_id,))
    data=cur.fetchone()
    if data:
        print(f"Item ID: {data[0]}, Name: {data[1]}, category: {data[2]}, Price: {data[3]} Rs")
        confirm=input("do you want to modify the item(yes\no): ")
        if confirm=="yes":
            new_name = input("Enter new item name: ")
            new_category=input("Enter new category: ")
            new_price = float(input("Enter new price: "))
            cur.execute("UPDATE menu_card SET items=%s,category=%s, price=%s WHERE item_id=%s",(new_name, new_category, new_price, item_id))
            con.commit()
            print("item modified sucessfully")
        else:
            print("modification cancelled")
    else:
        print("item not found")
    cur.close()
    
def add_to_cart():
    
    add = int(input("Select an item ID to add: "))

    cur = con.cursor()
    cur.execute('SELECT * FROM menu_card WHERE item_id = %s', (add,))
    data = cur.fetchone()

    if data:
        confirm = input("Do you want to add the item (yes/no): ")
        if confirm.lower() == "yes":
            quantity = int(input("Select the quantity to add: "))
            item_id, name, category, price = data
            cur.execute(
                "INSERT INTO cart (item_id, name, category, price, quantity, user_mobile_no) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (item_id, name, category, price, quantity, user_mobile_no)
            )
            con.commit()
            print("Item added to cart successfully.")
        else:
            print("Item not added.")
    else:
        print("Item not found.")
    cur.close()
def view_cart():
    
    cur = con.cursor()
    cur.execute("SELECT item_id, name, category, price, quantity FROM cart WHERE user_mobile_no = %s", (user_mobile_no,))
    data = cur.fetchall()

    if not data:
        print("Cart is empty.")
        cur.close()
        return

    total = 0
    for item in data:
        item_id, name, category, price, quantity = item
        item_total = price * quantity
        total += item_total
        print(f"{name} ({category}) - {quantity} x {price} = {item_total} Rs")

    print(f"Total Amount: {total} Rs")
    
    cur.close()

def modify_cart():
    cur = con.cursor()
    cur.execute("SELECT item_id, name, category, price, quantity FROM cart WHERE user_mobile_no = %s", (user_mobile_no,))
    data = cur.fetchall()

    if not data:
        print("Cart is empty.")
        cur.close()
        return

    for item in data:
        item_id, name, category, price, quantity = item
        print(f"{item_id} - {name} ({category}) - Quantity: {quantity} - Price: {price} Rs")

    item_id_input = input("Enter the item ID you want to modify: ")

    if not item_id_input.isdigit():
        print("Invalid input. Item ID must be a number.")
        cur.close()
        return

    item_id = int(item_id_input)

    cur.execute("SELECT * FROM cart WHERE item_id = %s AND user_mobile_no = %s", (item_id, user_mobile_no))
    item = cur.fetchone()

    if not item:
        print("Item not found in your cart.")
        cur.close()
        return

    print("1. Change quantity")
    print("2. Remove item from cart")
    choice = input("Choose an option (1 or 2): ")

    if choice == '1':
        quantity_input = input("Enter new quantity: ")
        if quantity_input.isdigit():
            new_quantity = int(quantity_input)
            if new_quantity > 0:
                cur.execute(
                    "UPDATE cart SET quantity = %s WHERE item_id = %s AND user_mobile_no = %s",
                    (new_quantity, item_id, user_mobile_no)
                )
                con.commit()
                print("Quantity updated successfully.")
            else:
                print("Quantity must be greater than 0.")
        else:
            print("Invalid quantity input.")

    elif choice == '2':
        cur.execute("DELETE FROM cart WHERE item_id = %s AND user_mobile_no = %s", (item_id, user_mobile_no))
        con.commit()
        print("Item removed from cart.")
    else:
        print("Invalid choice.")

    cur.close()


def generate_bill():
    cur = con.cursor()
    cur.execute("SELECT name, category, price, quantity FROM cart WHERE user_mobile_no = %s", (user_mobile_no,))
    data = cur.fetchall()

    if not data:
        print("Cart is empty. Nothing to bill.")
        cur.close()
        return

    
    total = 0

    for item in data:
        name, category, price, quantity = item
        item_total = price * quantity
        total += item_total
        print(f"{name} ({category}) - {quantity} x {price} = {item_total} Rs")
        cur.execute(
            "INSERT INTO orders (user_name, user_mobile_no, item_name, category, quantity, price, total) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (user_name, user_mobile_no, name, category, quantity, price, item_total))

    
    con.commit()

    print(f"Total Amount: {total} Rs")
    print("Thank you for your order!")
    cur.close()

def view_all_orders():
    cur = con.cursor()
    cur.execute("SELECT * FROM orders")
    data = cur.fetchall()

    if not data:
        print("No orders found.")
    else:
        for order in data:
            print(f"User: {order[0]}, Phone: {order[1]}, Item: {order[2]}, Category: {order[3]}, "
                  f"Quantity: {order[4]}, Price: {order[5]}, Total: {order[6]} Rs")
            print(f"Date: {order[7]}")
    cur.close()

def day_wise_profit():
    cur = con.cursor()
    cur.execute("SELECT order_date, SUM(total) FROM orders GROUP BY order_date")
    data = cur.fetchall()
    for date, total in data:
        print(f"Date: {date} - Total Profit: {total} Rs")
    cur.close()

while True:
    print("1.Admin login")
    print("2.User login")
    print("3.Exit")
    choose=input("enter your choice(1/2/3):")
    if choose=="1":
        admin_id='kalyan'
        password='123'
        crct_admin_id=input("enter admin id:")
        crct_admin_password=input("enter admin password:")
        if crct_admin_id==admin_id and crct_admin_password==password:
            print("Admin login succesfully")
            print()
            while True:
                print('1.admin menu')
                print('2.add items')
                print('3.delete menu')
                print('4.modify menu')
                print('5.view all orders')
                print('6.day wise profit')
                print('7.logout')
                print()
                ch=input("choose one option: ")
                if ch=='1':
                    menu_items()
                elif ch=='2':
                    add_items()
                elif ch=='3':
                    delete_item()
                elif ch=='4':
                    modify_item()
                elif ch=='5':
                    view_all_orders()
                elif ch=='6':
                    day_wise_profit()
                elif ch=='7':
                    break
                else:
                    print("please choose the correct option")                  
                    
    elif choose=='2':
        user_name=input("enter user name: ")
        while True:
            
            user_mobile_no=input("enter user mobile no: ")
            s=['9','8','7','6']
            if len(user_mobile_no)==10 and user_mobile_no.isdigit() and  user_mobile_no[0] in s:
                print("user login sucessfull!")
                break
            else:
                print("please enter correct credentials")
                continue
        while True:
            user=input("do you want to order: ")
            if user=="yes":
                    while True:
                        print("1.view menu")
                        print("2.add items to cart")
                        print("3.view items in cart")
                        print("4.modify cart")
                        print("5.bill")
                        print("6.logout")
                        print()
                        ch=input("choose one option: ")
                        if ch=="1":
                            menu_items()
                        elif ch=="2":
                            add_to_cart()
                        elif ch=="3":
                            view_cart()
                        elif ch=="4":
                            modify_cart()
                        elif ch=="5":
                            generate_bill()    
                        elif ch=="6":
                            break
                        else:
                            print("plese choose the corrct one")
            elif user=="no":
                break
            else:
                print("please choose the correct one!")
    elif choose=='3':
        print("Thank you for visiting. please visit again!")
        break
    else:
        print("please choose the correct option")
con.close()

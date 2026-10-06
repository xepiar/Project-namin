import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'bigbrew_db',
    'autocommit': True
}

#IF HINDI NAKABUKAS YUNG XAMPP
OFFLINE_MENU = [
    (1, 'Classic Milk Tea', 29.0, 'Milk Tea'),
    (2, 'Wintermelon', 29.0, 'Milk Tea'),
    (3, 'Okinawa', 29.0, 'Milk Tea'),
    (4, 'Taro', 29.0, 'Milk Tea'),
    (5, 'Brewed Coffee', 29.0, 'Iced Coffee'),
    (6, 'Caramel Macchiato', 29.0, 'Iced Coffee'),
    (7, 'Green Apple', 29.0, 'Fruit Tea'),
    (8, 'Lychee', 29.0, 'Fruit Tea'),
]

OFFLINE_SALES = []

def get_db_connection():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        return conn
    except Exception:
        #IF HINDI LANG NAKA ON YUNG XAMPP
        return None

#ETO YUNG SA CRUD
def get_all_menu_items():
    conn = get_db_connection()
    if conn is None:
        return OFFLINE_MENU

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, price, category FROM menu_items ORDER BY id ASC")
            items = cursor.fetchall()
        conn.close()
        return items
    except Exception as e:
        print(f"Error fetching menu items: {e}")
        if conn:
            conn.close()
        return OFFLINE_MENU

def add_menu_item(name, price, category):
    conn = get_db_connection()
    if conn is None:
        new_id = len(OFFLINE_MENU) + 1
        OFFLINE_MENU.append((new_id, name, price, category))
        return True

    try:
        with conn.cursor() as cursor:
            query = "INSERT INTO menu_items (name, price, category) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, price, category))
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding menu item: {e}")
        if conn:
            conn.close()
        return False

def update_menu_item(item_id, name, price, category):
    conn = get_db_connection()
    if conn is None:
        for idx, item in enumerate(OFFLINE_MENU):
            if item[0] == item_id:
                OFFLINE_MENU[idx] = (item_id, name, price, category)
                return True
        return False

    try:
        with conn.cursor() as cursor:
            query = "UPDATE menu_items SET name = %s, price = %s, category = %s WHERE id = %s"
            cursor.execute(query, (name, price, category, item_id))
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating menu item: {e}")
        if conn:
            conn.close()
        return False

def delete_menu_item(item_id):
    conn = get_db_connection()
    if conn is None:
        global OFFLINE_MENU
        OFFLINE_MENU = [item for item in OFFLINE_MENU if item[0] != item_id]
        return True

    try:
        with conn.cursor() as cursor:
            query = "DELETE FROM menu_items WHERE id = %s"
            cursor.execute(query, (item_id,))
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting menu item: {e}")
        if conn:
            conn.close()
        return False

#DITO MAG SAVE MGA ORDERS
def save_sales_record(customer_name, timestamp, total, cash, change, items):
    conn = get_db_connection()
    if conn is None:
        OFFLINE_SALES.append({
            "order_id": len(OFFLINE_SALES) + 1,
            "customer_name": customer_name,
            "timestamp": timestamp,
            "total_amount": total
        })
        return True

    try:
        with conn.cursor() as cursor:
            order_query = """
            INSERT INTO orders (customer_name, timestamp, total_amount, cash_tendered, change_due)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(order_query, (customer_name, timestamp, total, cash, change))
            order_id = cursor.lastrowid

            item_query = """
            INSERT INTO order_items (order_id, item_name, price)
            VALUES (%s, %s, %s)
            """
            for item in items:
                cursor.execute(item_query, (order_id, item['name'], item['price']))

        conn.close()
        return True
    except Exception as e:
        print(f"Database Query Error: {e}")
        if conn:
            conn.close()
        return False

def get_all_sales():
    conn = get_db_connection()
    if conn is None:
        return OFFLINE_SALES

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT order_id, customer_name, timestamp, total_amount FROM orders ORDER BY order_id DESC")
            rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"Error fetching sales: {e}")
        if conn:
            conn.close()
        return OFFLINE_SALES
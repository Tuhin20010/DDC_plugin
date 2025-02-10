import sqlite3

def get_db_connection():
    conn = sqlite3.connect("inventory.db")
    conn.row_factory = sqlite3.Row  
    return conn

def show_inventory():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM inventory")
    rows = cursor.fetchall()

    print("Inventory List:")
    print("----------------")
    
    for row in rows:
        print(f"ID: {row['id']}, Name: {row['name']}, Quantity: {row['quantity']}")
    
    conn.close()

if __name__ == "__main__":
    show_inventory()

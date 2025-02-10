from flask import Flask, request, jsonify
import sqlite3
import time

app = Flask(__name__)

# Connect to the database
def get_db_connection():
    conn = sqlite3.connect("inventory.db")
    conn.row_factory = sqlite3.Row  
    return conn

# Initialize database
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Run database 
init_db()


# Transform data
@app.route("/transform", methods=["POST"])
def transform():
    time.sleep(10)  # Simulate delay
    data = request.json
    print(f"Received Transform Data: {data}")
    return jsonify({"message": "Transform data received"}), 200

# Translation data
@app.route('/translation', methods=["POST"])
def translation():
    time.sleep(10)
    data = request.json
    print(f"Received Translation Data: {data}")
    return jsonify({"message": "Translation data received"}), 200

# Rotation data
@app.route('/rotation', methods=["POST"])
def rotation():
    time.sleep(10)
    data = request.json
    print(f"Received Rotation Data: {data}")
    return jsonify({"message": "Rotation data received"}), 200

# Scale data
@app.route('/scale', methods=["POST"])
def scale():
    time.sleep(10)
    data = request.json
    print(f"Received Scale Data: {data}")
    return jsonify({"message": "Scale data received"}), 200

# File path for Blender file
@app.route('/file-path', methods=["GET"])
def file_path():
    project_path = request.args.get('projectpath', 'false').lower() == 'true'
    file_path = "C:\\Users\\hp\\Desktop\\DDC Integration\\ddc_plugin.blend"

    if project_path:
        project_folder = "C:\\Users\\hp\\Desktop\\DDC Integration"
        return jsonify({"file_path": project_folder}), 200
    else:
        return jsonify({"file_path": file_path}), 200


# **Add Item to Inventory**
@app.route('/add-item', methods=["POST"])
def add_item():
    data = request.json
    name = data.get("name")
    quantity = data.get("quantity", 1)

    if not name or quantity < 1:
        return jsonify({"error": "Invalid data. Name and positive quantity required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO inventory (name, quantity) VALUES (?, ?)", (name, quantity))
        conn.commit()
        response = {"message": "Item added to inventory", "name": name, "quantity": quantity}
    except sqlite3.IntegrityError:
        response = {"error": "Item already exists"}
    finally:
        conn.close()

    return jsonify(response), 200


#  **Remove Item from Inventory**
@app.route('/remove-item', methods=["POST"])
def remove_item():
    data = request.json
    name = data.get("name")

    if not name:
        return jsonify({"error": "Please provide item name"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory WHERE name=?", (name,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Item '{name}' removed from inventory"}), 200


#  **Update Item Quantity in inventory**
@app.route('/update-quantity', methods=["POST"])
def update_quantity():
    data = request.json
    name = data.get("name")
    new_quantity = data.get("quantity")

    if not name or new_quantity is None or new_quantity < 0:
        return jsonify({"error": "Please provide valid item name and quantity"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE inventory SET quantity=? WHERE name=?", (new_quantity, name))
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Item not found"}), 404

    conn.commit()
    conn.close()
    
    return jsonify({"message": f"Quantity of '{name}' updated to {new_quantity}"}), 200


# ** show All Inventory Items**
@app.route('/inventory', methods=["GET"])
def get_inventory():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()
    conn.close()

    inventory_list = [{"id": item["id"], "name": item["name"], "quantity": item["quantity"]} for item in items]
    return jsonify(inventory_list), 200


if __name__ == "__main__":
    app.run(debug=True)

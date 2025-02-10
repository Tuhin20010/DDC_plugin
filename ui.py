import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel, QHBoxLayout, QMessageBox, QHeaderView
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt

# server URL
SERVER_URL = "http://127.0.0.1:5000"

class InventoryApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("🛒 Inventory Manager")
        self.setGeometry(200, 100, 700, 500)
        self.setStyleSheet("background-color: #2E2E2E; color: white;")

        self.layout = QVBoxLayout()

        # Title
        self.title = QLabel("Inventory Management System")
        self.title.setFont(QFont("Arial", 16, QFont.Bold))
        self.title.setStyleSheet("color: #00E676; padding: 10px; text-align: center;")
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)

        # Inventory Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Quantity"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet(
            "background-color: white; color: black; font-size: 14px;"
            "border: 1px solid #00E676; font-weight: bold;"
        )
        self.layout.addWidget(self.table)

        # Input Fields
        input_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter Item Name")
        self.name_input.setStyleSheet(
            "background-color: #424242; color: white; border: 1px solid #00E676; padding: 5px;"
        )
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Enter Quantity")
        self.quantity_input.setStyleSheet(
            "background-color: #424242; color: white; border: 1px solid #00E676; padding: 5px;"
        )
        input_layout.addWidget(self.name_input)
        input_layout.addWidget(self.quantity_input)

        # Buttons
        self.add_button = QPushButton("➕ Add Item")
        self.update_button = QPushButton("🔄 Update Quantity")
        self.remove_button = QPushButton("❌ Remove Item")
        self.refresh_button = QPushButton("🔃 Refresh Inventory")

        for btn in [self.add_button, self.update_button, self.remove_button, self.refresh_button]:
            btn.setStyleSheet(
                "background-color: #00E676; color: black; font-weight: bold; padding: 8px; "
                "border-radius: 5px; font-size: 14px;"
            )
            btn.setCursor(Qt.PointingHandCursor)

        input_layout.addWidget(self.add_button)
        input_layout.addWidget(self.update_button)
        input_layout.addWidget(self.remove_button)
        self.layout.addLayout(input_layout)
        self.layout.addWidget(self.refresh_button)

        self.setLayout(self.layout)

        # Button Actions
        self.add_button.clicked.connect(self.add_item)
        self.update_button.clicked.connect(self.update_quantity)
        self.remove_button.clicked.connect(self.remove_item)
        self.refresh_button.clicked.connect(self.load_inventory)

        # Load Data
        self.load_inventory()

    def load_inventory(self):
        """Fetch and display inventory data."""
        try:
            response = requests.get(f"{SERVER_URL}/inventory")
            if response.status_code == 200:
                items = response.json()
                self.table.setRowCount(len(items))
                for row, item in enumerate(items):
                    self.table.setItem(row, 0, self.create_table_item(str(item["id"])))
                    self.table.setItem(row, 1, self.create_table_item(item["name"]))
                    self.table.setItem(row, 2, self.create_table_item(str(item["quantity"])))
            else:
                QMessageBox.critical(self, "Error", "Failed to fetch inventory data")
        except requests.exceptions.RequestException:
            QMessageBox.critical(self, "Error", "Could not connect to the server")

    def create_table_item(self, text):
        """Helper function to create styled table items."""
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        return item

    def add_item(self):
        """Add new item to inventory."""
        name = self.name_input.text().strip()
        quantity = self.quantity_input.text().strip()

        if not name or not quantity.isdigit():
            QMessageBox.warning(self, "Input Error", "Enter valid name and quantity")
            return

        data = {"name": name, "quantity": int(quantity)}
        try:
            response = requests.post(f"{SERVER_URL}/add-item", json=data)
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Item added successfully")
                self.load_inventory()
            else:
                QMessageBox.warning(self, "Error", response.json().get("error", "Failed to add item"))
        except requests.exceptions.RequestException:
            QMessageBox.critical(self, "Error", "Could not connect to the server")

    def update_quantity(self):
        """Update quantity of an existing item."""
        name = self.name_input.text().strip()
        quantity = self.quantity_input.text().strip()

        if not name or not quantity.isdigit():
            QMessageBox.warning(self, "Input Error", "Enter valid name and quantity")
            return

        data = {"name": name, "quantity": int(quantity)}
        try:
            response = requests.post(f"{SERVER_URL}/update-quantity", json=data)
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Quantity updated successfully")
                self.load_inventory()
            else:
                QMessageBox.warning(self, "Error", response.json().get("error", "Failed to update quantity"))
        except requests.exceptions.RequestException:
            QMessageBox.critical(self, "Error", "Could not connect to the server")

    def remove_item(self):
        """Remove an item from inventory."""
        name = self.name_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Input Error", "Enter valid item name")
            return

        data = {"name": name}
        try:
            response = requests.post(f"{SERVER_URL}/remove-item", json=data)
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Item removed successfully")
                self.load_inventory()
            else:
                QMessageBox.warning(self, "Error", response.json().get("error", "Failed to remove item"))
        except requests.exceptions.RequestException:
            QMessageBox.critical(self, "Error", "Could not connect to the server")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec_())

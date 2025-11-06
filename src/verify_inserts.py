from flask import Flask
from models import init_db, check_db_connection, add_inventory_item, add_transaction, find_inventory, find_transactions

app = Flask(__name__)
app.config.from_object('config.Config')

def run_test():
    try:
        init_db(app)
        ok = check_db_connection()
        print("DB ping OK" if ok else "DB ping falló")
    except Exception as e:
        print("Error init/check DB:", e)
        return

    # documento de ejemplo para inventory
    inventory_doc = {
        "id": "inv_test_1",
        "code": "ABC123",
        "product": "Producto de prueba",
        "shelves": 2,
        "floors": 1,
        "packs": 10
    }

    # documento de ejemplo para transaction
    transaction_doc = {
        "id": "tx_test_1",
        "date": "2025-11-03",
        "product": "Producto de prueba",
        "total": 5
    }

    try:
        inv_id = add_inventory_item(inventory_doc)
        tx_id = add_transaction(transaction_doc)
        print("Inserted inventory _id:", inv_id)
        print("Inserted transaction _id:", tx_id)
    except Exception as e:
        print("Error inserting documents:", e)
        return

    # listar para verificar
    try:
        print("Inventory sample:", find_inventory({"id": "inv_test_1"}))
        print("Transactions sample:", find_transactions({"id": "tx_test_1"}))
    except Exception as e:
        print("Error reading back documents:", e)

if __name__ == "__main__":
    run_test()
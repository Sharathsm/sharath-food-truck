from flask import Flask, jsonify, request
from uuid import uuid4
import datetime

app = Flask(__name__)

# simple in-memory menu + orders (for demo)
MENU = [
    {"id": 1, "name": "Paneer Roll", "price": 80},
    {"id": 2, "name": "Masala Dosa", "price": 70},
    {"id": 3, "name": "Idli (2pcs)", "price": 40},
]

ORDERS = []

@app.route("/")
def index():
    return jsonify({
        "app": "Sharath Food Truck",
        "version": "1.0",
        "time": datetime.datetime.utcnow().isoformat() + "Z"
    })

@app.route("/menu", methods=["GET"])
def get_menu():
    return jsonify(MENU)

@app.route("/order", methods=["POST"])
def create_order():
    data = request.get_json() or {}
    if not data.get("items"):
        return jsonify({"error": "items list required"}), 400

    # simple validation
    items = []
    total = 0
    for item in data["items"]:
        # item can be id or {id, qty}
        item_id = item.get("id") if isinstance(item, dict) else item
        qty = item.get("qty", 1) if isinstance(item, dict) else 1
        m = next((x for x in MENU if x["id"] == item_id), None)
        if not m:
            return jsonify({"error": f"menu item {item_id} not found"}), 400
        items.append({"id": m["id"], "name": m["name"], "qty": qty, "unit_price": m["price"]})
        total += m["price"] * qty

    order = {
        "order_id": str(uuid4()),
        "items": items,
        "total": total,
        "status": "received",
        "created_at": datetime.datetime.utcnow().isoformat() + "Z"
    }
    ORDERS.append(order)
    return jsonify(order), 201

@app.route("/orders", methods=["GET"])
def list_orders():
    return jsonify(ORDERS)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "uptime": "running"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

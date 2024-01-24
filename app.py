from flask import Flask
from flask_smorest import abort
from flask import request
from db import stores, items
import uuid

app = Flask(__name__)


@app.post("/store")  # http://127.0.0.1:5000/store
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201


@app.get("/store")  # http://127.0.0.1:5000/store
def get_stores():
    return {"stores": list(stores.values())}


@app.get("/store/<string:store_id>")  # http://127.0.0.1:5000/store/storeName
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found.")


@app.post("/item")  # http://127.0.0.1:5000/store/name/item
def create_item():
    item_data = request.get_json()

    if item_data["store_id"] not in stores:
        abort(404, message="Store not found")
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item, 201


@app.get("/item")  # http://127.0.0.1:5000/store/name/item
def get_all_items():
    return {"items": list(items.values())}


@app.get("/item:<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found")

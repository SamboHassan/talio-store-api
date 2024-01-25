from flask import Flask
from flask_smorest import abort
from flask import request
from db import stores, items
import uuid

app = Flask(__name__)


@app.get("/store")  # http://127.0.0.1:5000/store
def get_stores():
    return {"stores": list(stores.values())}


@app.get("/store/<string:store_id>")  # http://127.0.0.1:5000/store/store_id
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found.")


@app.post("/store")  # http://127.0.0.1:5000/store
def create_store():
    store_data = request.get_json()

    if "name" not in store_data:
        abort(400, message="Bad request. Ensure 'name' is included in the JSON payload")

    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message="Store already exist.")

    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201


@app.post("/item")  # http://127.0.0.1:5000/item
def create_item():
    item_data = request.get_json()

    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message="Bad request. Ensure 'price', 'name', 'store_id' is included in the JSON payload",
        )

    for item in items.values():
        if (
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, message="Item already exist.")

    if item_data["store_id"] not in stores:
        abort(404, message="Store not found")
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item, 201


@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted"}
    except KeyError:
        abort(404, message="Store not found")


@app.get("/item")  # http://127.0.0.1:5000/store/name/item
def get_all_items():
    return {"items": list(items.values())}


# "3dd842bb20914b769ff67ef4b20dddbd"
@app.get("/item/<string:item_id>")  # http://127.0.0.1:500/item/id
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found")


@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted"}
    except KeyError:
        abort(404, message="Item not found")


@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort(
            400,
            message="Bad request. Ensure 'name' and 'price' is included in the JSON payload",
        )
    try:
        item = items[item_id]
        item |= item_data
    except KeyError:
        abort(404, message="Item not found")

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

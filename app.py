from flask import Flask
from flask import request

app = Flask(__name__)

stores = [{"name": "My Store", "items": [{"name": "Chair", "price": 15.99}]}]


@app.get("/stores")  # http://127.0.0.1:5000/stores
def get_stores():
    return {"stores": stores}


@app.post("/stores")  # http://127.0.0.1:5000/stores
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201

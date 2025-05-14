from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import sqlite3
import time

app = FastAPI()

def open_connection():
    return sqlite3.connect("db.sqlite", check_same_thread=False)

# Pydantic Schemas
class Item(BaseModel):
    name: str
    price: float

class Customer(BaseModel):
    name: str
    phone: int

class Order(BaseModel):
    id: int
    customer_id: int
    notes: str

# Item Routes

@app.post("/items")
def create_item(item: Item):
    try:
        with open_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO items (name, price) VALUES (?, ?)", (item.name, item.price))
            conn.commit()
            return {"id": cursor.lastrowid, "name": item.name, "price": item.price}
    except Exception as err:
        raise HTTPException(status_code=500, detail="Failed to add item")

@app.get("/items/{item_id}")
def get_item(item_id: int):
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        record = cursor.fetchone()
        if not record:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"id": record[0], "name": record[1], "price": record[2]}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE items SET name = ?, price = ? WHERE id = ?", (item.name, item.price, item_id))
        conn.commit()
        return {"id": item_id, "name": item.name, "price": item.price}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
        return {"message": f"Item {item_id} removed"}

# Customer Routes

@app.post("/customers")
def add_customer(customer: Customer):
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (customer.name, customer.phone))
        conn.commit()
        return {"id": cursor.lastrowid, "name": customer.name, "phone": customer.phone}

@app.get("/customers/{customer_id}")
def fetch_customer(customer_id: int):
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
        data = cursor.fetchone()
        if not data:
            raise HTTPException(status_code=404, detail="Customer not found")
        return {"id": data[0], "name": data[1], "phone": data[2]}

@app.put("/customers/{customer_id}")
def edit_customer(customer_id: int, customer: Customer):
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE customers SET name = ?, phone = ? WHERE id = ?", (customer.name, customer.phone, customer_id))
        conn.commit()
        return {"id": customer_id, "name": customer.name, "phone": customer.phone}

@app.delete("/customers/{customer_id}")
def remove_customer(customer_id: int):
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE customer_id = ?", (customer_id,))
        if cursor.fetchone():
            return {"message": "Delete associated orders first."}
        cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
        conn.commit()
        return {"message": "Customer deleted"}

# Order Routes

@app.post("/orders/{order_id}")
def add_order(order: Order):
    with open_connection() as conn:
        cursor = conn.cursor()
        ts = int(time.time())
        cursor.execute("INSERT INTO orders (timestamp, customer_id, notes) VALUES (?, ?, ?)",
                       (ts, order.customer_id, order.notes))
        conn.commit()
        return {"id": cursor.lastrowid, "timestamp": ts, "customer_id": order.customer_id, "notes": order.notes}

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Order not found")
        return {"id": result[0], "timestamp": result[1], "customer_id": result[2], "notes": result[3]}

@app.put("/orders/{order_id}")
def modify_order(order_id: int, order: Order):
    with open_connection() as conn:
        cursor = conn.cursor()
        ts = int(time.time())
        cursor.execute("UPDATE orders SET timestamp = ?, customer_id = ?, notes = ? WHERE id = ?",
                       (ts, order.customer_id, order.notes, order_id))
        conn.commit()
        return {"id": order_id, "timestamp": ts, "customer_id": order.customer_id, "notes": order.notes}

@app.delete("/orders/{order_id}")
def remove_order(order_id: int):
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        conn.commit()
        return {"message": f"Order {order_id} removed"}

# Root Redirect

@app.get("/")
def docs_redirect():
    return RedirectResponse(url="/docs")

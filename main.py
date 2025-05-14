from fastapi import FastAPI,HTTPException
from fastapi.responses import RedirectResponse
import sqlite3
from pydantic import BaseModel
import time

class Item(BaseModel):
    name : str
    price : float

class Customer(BaseModel):
    name : str
    phone: int

class Orders(BaseModel):
    id : int
    customer_id: int
    notes: str
    timestamp : int

#Initialize database connection
connection = sqlite3.connect("db.sqlite")
cursor = connection.cursor()

app = FastAPI()

#Code for items database to perform CRUD operations
@app.get("/items/{item_id}")
async def read_item(item_id):
    result = cursor.execute("SELECT * FROM items WHERE id=?;", (item_id,))
    item = result.fetchone()
    if item == None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {
        "id": item[0],
        "name" : item[1],
        "price" : item[2],
            }


@app.post("/items")
async def create_items(item:Item):
    name = item.name
    price = item.price
    cursor.execute("INSERT INTO items (name,price) VALUES(?, ?);",(name,price))
    connection.commit()
    return {
       "id" : cursor.lastrowid,
       "name" : name,
       "price" : price,
    }

@app.delete("/items/{item_id}")
async def delete_item(item_id):
    cursor.execute("DELETE FROM items WHERE id=?;",(item_id,))
    connection.commit()
    return 

@app.put("/items/{item_id}")
async def update_item(item_id, item: Item):
    cursor.execute("UPDATE items SET name=?, price=? WHERE id=?;",(item.name, item.price, item_id))
    connection.commit()
    return{
        "id" : item_id,
        "name" : item.name,
        "price" : item.price,
    }


@app.get("/customers/{customer_id}")
async def read_item(customer_id):
    result = cursor.execute("SELECT * FROM customers WHERE id=?;", (customer_id,))
    customer = result.fetchone()
    return {
        "id": customer[0],
        "name" : customer[1],
        "phone" : customer[2],
            }

@app.post("/customer")
async def create_customer(customer:Customer):
    name = customer.name
    phone = customer.phone
    cursor.execute("INSERT INTO customers (name,phone) VALUES(?, ?);",(name,phone))
    connection.commit()
    return {
       "id" : cursor.lastrowid,
       "name" : name,
       "phone" : phone,
    }


@app.delete("/customers/{customer_id}")
async def delete_customer(customer_id):
    cursor.execute("SELECT * FROM orders WHERE id=?",(customer_id,))
    customer = cursor.fetchone()
    if customer == None:
        cursor.execute("DELETE FROM customers WHERE id=?;",(customer_id,))
        return {"message": "Customer deleted successfully"}
    else:
        return {"message": "Please delete the entry in orders table."}

@app.put("/customers/{customer_id}")
async def update_customer(customer_id, customer: Customer):
    cursor.execute("UPDATE customers SET name=?, phone=? WHERE id=?;",(customer.name, customer.phone, customer_id))
    connection.commit()
    return{
        "id" : customer_id,
        "name" : customer.name,
        "phone" : customer.phone,
    }

@app.get("/orders/{order_id}")
async def read_order(order_id):
    result = cursor.execute("SELECT * FROM orders WHERE id=?;", (order_id,)).fetchone()
    return {
        "id" : result[0],
        "timestamp" : result[1],
        "customer_id" : result[2],
        "notes": result[3]
    }

@app.delete("/orders/{order_id}")
async def delete_order(order_id):
    cursor.execute("DELETE FROM orders WHERE id=?;",(order_id,))
    connection.commit()
    return 

@app.post("/orders/{order_id}")
async def create_order(order: Orders):
    timestamp = order.timestamp
    customer_id = order.customer_id
    notes = order.notes
    cursor.execute("INSERT INTO orders(timestamp, customer_id, notes) VALUES(?,?,?);",(timestamp,customer_id,notes))
    connection.commit()
    return{
        "id" : cursor.lastrowid,
        "timestamp" : timestamp,
        "customer_id" : customer_id,
        "notes" : notes
    }


@app.put("/orders/{order_id}")
async def update_orders(order_id, order: Orders):
    timestamp = order.timestamp
    customer_id = order.customer_id
    notes = order.notes
    cursor.execute("UPDATE orders SET timestamp=?, customer_id=?,notes=? WHERE id=?;",(timestamp,customer_id,notes,order_id))
    connection.commit()
    return{
        "id" : order_id,
        "timestamp" : timestamp,
        "customer_id" : customer_id,
        "notes" : notes
    }

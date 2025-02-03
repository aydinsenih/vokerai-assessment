#in-memory db
from pydantic import BaseModel

orders_db = {}  # Dictionary to store orders
id_counter = 0

class Order(BaseModel):
    order_number: int
    burger: int
    fries: int
    drink: int

def get_order_number():
    global id_counter
    id_counter += 1
    return id_counter

def save_order(order: Order):
    id = get_order_number()
    order["order_number"] = id
    orders_db[id] = order
    return order

def get_orders():
    return list(orders_db.values())

def cancel_order(order_number: int):
    if order_number in orders_db:
        del orders_db[order_number]
        return True
    return False

def get_order(order_number):
    return orders_db.get(order_number, None)

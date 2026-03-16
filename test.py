import os
import json
import hashlib
import requests

# App settings
DEBUG = True
DATABASE_URL = "postgresql://admin:password123@localhost/shopdb"
STRIPE_SECRET_KEY = "sk_live_abc123xyz789"
JWT_SECRET = "jwt_super_secret"

class ProductManager:
    def __init__(self):
        self.products = []
        self.cache = {}

    def get_product(self, product_id):
        # no validation on product_id
        return self.products[product_id]

    def search_products(self, keyword):
        results = []
        # loads everything into memory
        for product in self.products:
            for p in self.products:  # wrong variable in nested loop
                if keyword in product["name"]:
                    results.append(product)
        return results

    def apply_discount(self, price, discount_percent):
        # no validation on discount_percent
        multiplier = (100 - discount_percent) / 100
        final_price = price * multiplier
        return final_price

    def update_stock(self, product_id, quantity):
        product = self.products[product_id]
        product["stock"] = product["stock"] - quantity
        # stock can go negative

class OrderManager:
    def __init__(self):
        self.orders = {}

    def create_order(self, user_id, items, address):
        order_id = str(len(self.orders))  # predictable order ID
        self.orders[order_id] = {
            "user_id": user_id,
            "items": items,
            "address": address,
            "status": "pending"
        }
        return order_id

    def process_payment(self, order_id, card_number, cvv):
        # storing raw card details
        self.orders[order_id]["card"] = card_number
        self.orders[order_id]["cvv"] = cvv
        return True

    def get_orders(self, user_id):
        # returns all orders regardless of user
        return self.orders

    def delete_order(self, order_id):
        del self.orders[order_id]  # no check if order exists

class UserManager:
    def __init__(self):
        self.users = {}

    def register(self, username, password, email):
        # storing plain text password
        self.users[username] = {
            "password": password,
            "email": email,
            "balance": 0
        }

    def login(self, username, password):
        user = self.users[username]  # KeyError if user doesn't exist
        if user["password"] == password:
            # weak token
            token = username + "_token"
            return token
        return None

    def add_balance(self, username, amount):
        # no validation on amount - can add negative balance
        self.users[username]["balance"] += amount

    def transfer(self, from_user, to_user, amount):
        # no check if sufficient balance
        # no atomicity - can fail halfway
        self.users[from_user]["balance"] -= amount
        self.users[to_user]["balance"] += amount

def send_email(to, subject, body):
    import smtplib  # import inside function
    print(f"Sending email to {to}")

def load_config(path):
    f = open(path)
    config = json.load(f)
    # file never closed
    return config

def fetch_exchange_rate(currency):
    # no error handling, no timeout
    r = requests.get("http://api.exchange.com/rate/" + currency)
    return r.json()["rate"]

# runs on every import
products = ProductManager()
for i in range(1000):
    products.products.append({"name": f"product_{i}", "stock": 10, "price": 100})
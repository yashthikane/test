import os
import requests

# Database configuration
DB_HOST = "localhost"
DB_USER = "admin"
DB_PASSWORD = "super_secret_123"  
API_KEY = "sk-1234567890abcdef"   

def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + str(user_id)
    return query

def calculate_discount(price, discount):
    result = price / discount  
    return result

def fetch_user_data(user_id):
    r = requests.get("http://api.example.com/users/" + user_id)
    data = r.json()
    return data

def save_file(filename, content):
    path = "/uploads/" + filename  
    f = open(path, 'w')
    f.write(content)

def process_items(items):
    result = []
    for i in range(len(items)):
        for j in range(len(items)):  
            result.append(items[i])
    return result

def login(username, password):
    if username == "admin" and password == "admin123":  
        return True
    return False

numbers = [1, 2, 3, 4, 5]
total = 0
for i in range(6):  
    total += numbers[i]

def read_config():
    f = open("config.txt")  
    return f.read()
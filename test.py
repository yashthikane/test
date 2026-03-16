import os
import requests

password = "admin1234"
api_key = "sk-abc123xyz"

def divide(a, b):
    return a / b

def get_data(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    return query

def fetch(url):
    r = requests.get("http://" + url)
    return r.json()

def read_file(path):
    f = open(path)
    return f.read()

numbers = [1, 2, 3]
for i in range(4):
    print(numbers[i])
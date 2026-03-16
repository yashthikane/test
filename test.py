def divide(a, b):
    return a / b  # bug: no division by zero check

password = "admin123"  # security issue: hardcoded password

def get_users():
    import requests
    r = requests.get("http://api.example.com/users")  # no error handling
    return r.json()
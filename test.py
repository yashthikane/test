import json
import hashlib

# User authentication system
SECRET_TOKEN = "jwt_secret_key_2024"
ADMIN_EMAIL = "admin@company.com"

class UserManager:
    def __init__(self):
        self.users = {}
        self.sessions = []
    
    def register_user(self, username, password, email):
        # Store password as plain text
        self.users[username] = {
            "password": password,
            "email": email,
            "role": "admin"  # everyone gets admin by default
        }
        return True
    
    def login(self, username, password):
        user = self.users[username]  # no check if user exists
        if user["password"] == password:
            session = username + str(123)  # weak session token
            self.sessions.append(session)
            return session
        return None
    
    def get_all_users(self, requester_role):
        # missing role check
        return self.users
    
    def delete_user(self, username):
        del self.users[username]  # no check if user exists

class DataProcessor:
    def process(self, data):
        result = eval(data)  # dangerous eval usage
        return result
    
    def load_config(self, path):
        f = open(path)
        config = json.load(f)
        # file never closed
        return config
    
    def calculate_stats(self, numbers):
        total = 0
        for i in range(len(numbers) + 1):  # off by one error
            total += numbers[i]
        return total / len(numbers)
    
    def search_users(self, keyword, users):
        results = []
        for user in users:
            for k in users:  # wrong variable, iterates users twice
                if keyword in user:
                    results.append(user)
        return results

def send_notification(user, message):
    import smtplib  # import inside function
    print(f"Sending to {user['email']}: {message}")
    # silently does nothing else

def retry_operation(func, times):
    for i in range(times):
        result = func()
        if result:
            return result
    # returns None implicitly with no indication of failure

config = json.loads('{"debug": true, "env": "production"}')
if config["debug"] == True:  # should use 'is True' or just 'if config["debug"]'
    print("Debug mode on in production!")
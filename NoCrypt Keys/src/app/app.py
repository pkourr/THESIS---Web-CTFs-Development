from flask import Flask, request, render_template
from pymongo import MongoClient
import json
import os

# Create a Flask app instance
app = Flask(__name__)

# Retrieve MongoDB URI from the environment variable or use default if not set
mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
# Connect to MongoDB using the URI
client = MongoClient(mongo_uri)
# Select the database for the CTF challenge
db = client.ctf
# Select the collection within the database
users = db.users

def initialize_db():
    # Initialize the database with a test user if the users collection is empty
    if users.count_documents({}) == 0:
        users.insert_one({"username": "testuser", "password": "password123"})

# Initialize the database on startup
initialize_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    # Extract username and password from form data
    username_input = request.form['username']
    password_input = request.form['password']

    try:
        # Attempt to parse input as JSON (for NoSQL injection possibility)
        username = json.loads(username_input)
        password = json.loads(password_input)
    except json.JSONDecodeError:
        # If not JSON-like, use the raw input
        username = username_input
        password = password_input

    # Vulnerable NoSQL query using user-provided input directly
    user = users.find_one({"username": username, "password": password})

    if user:
        # If a user is found, read the flag from a file and display it
        with open('flag.txt', 'r') as file:
            flag = file.read()
        return render_template('success.html', flag=flag)
    else:
        # If login fails, reload the index page with an error message
        return render_template('index.html', error="Login failed! Please try again.")

# Start the Flask app if this file is executed directly
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('APP_PORT', 4242)))

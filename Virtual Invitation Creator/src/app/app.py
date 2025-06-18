from flask import Flask, request, render_template, render_template_string, redirect, url_for, make_response, jsonify
import sqlite3
import jwt
import datetime
import bcrypt
import logging
import base64
import json

# Initialize Flask app and set a secret key for JWT encoding/decoding.
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
logging.basicConfig(level=logging.DEBUG)

# Establish a connection to the SQLite database.
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create a users table if it does not already exist in the database.
def create_users_table():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    conn.commit()
    conn.close()

# Check if a user exists in the database by username.
def user_exists(username):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user is not None

# Create a new user with a hashed password.
def create_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn = get_db_connection()
    conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()
    conn.close()

# Verify a user's credentials.
def verify_user(username, password):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return True
    return False

# Generate a JWT token. The payload includes a subscribed attribute which could be manipulated.
def generate_jwt(subscribed='no'):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'subscribed': subscribed
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

# Decode a JWT token. This function introduces a JWT vulnerability by allowing the use of 'none' as an algorithm.
def decode_jwt(token):
    try:
        # Split the JWT token into Header, Payload, and Signature parts
        header_b64, payload_b64, _ = token.split('.')

        # Decode the Header and Payload from Base64 to JSON
        header = json.loads(base64.urlsafe_b64decode(header_b64 + '==').decode('utf-8'))
        payload = json.loads(base64.urlsafe_b64decode(payload_b64 + '==').decode('utf-8'))

        # Check the algorithm specified in the JWT header
        if header.get('alg') == 'none':
            # If the algorithm is 'none', accept the token without verifying its signature.
            # This simulates a vulnerability where the server trusts the 'alg' header
            # from the client without proper verification.
            return payload
        else:
            # For all other cases, perform normal JWT signature verification.
            # This uses the application's secret key and ensures that the token
            # was not tampered with. It supports only the algorithms specified
            # (in this case, 'HS256').
            return jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except Exception as e:
        # Log any errors encountered during the JWT decoding process
        app.logger.error(f"JWT Error: {e}")
        return None


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            if user_exists(username):
                return 'User already exists. Please choose a different username.', 400

            create_user(username, password)
            return redirect(url_for('login'))
    except Exception as e:
        app.logger.error(f"Error during registration: {e}")
        return 'An error occurred during registration.', 500

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            if verify_user(username, password):
                token = generate_jwt()
                resp = make_response(redirect(url_for('profile')))
                resp.set_cookie('jwt', token)
                return resp

            return 'Invalid credentials. Please try again.', 401
    except Exception as e:
        app.logger.error(f"Error during login: {e}")
        return 'An error occurred during login.', 500

    return render_template('login.html')

# Define a route for displaying the user's profile.
@app.route('/profile')
def profile():
    # Retrieve the JWT token from the user's cookies
    token = request.cookies.get('jwt')
    # If no token is found, redirect the user to the login page.
    if not token:
        return redirect(url_for('login'))

    payload = decode_jwt(token)
    if payload is None:
        resp = make_response(redirect(url_for('login')))
        resp.set_cookie('jwt', '', expires=0)  # Clear the invalid cookie
        return resp

    subscribed = payload.get('subscribed', 'no')
    return render_template('profile.html', subscribed=subscribed)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    return jsonify({'message': 'This functionality is under maintenance'}), 200

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('jwt', '', expires=0)
    return resp

@app.route('/create-invitation', methods=['GET', 'POST'])
def create_invitation():
    token = request.cookies.get('jwt')
    if not token:
        return redirect(url_for('login'))

    payload = decode_jwt(token)
    if not payload or payload.get('subscribed') != 'yes':
        return redirect(url_for('profile', error='unsubscribed'))

    if request.method == 'POST':
        # Extract information from the JSON payload of the request.
        guest = request.json.get('guest', '')
        event = request.json.get('event', '')
        date = request.json.get('date', '')
        time = request.json.get('time', '')
        location = request.json.get('location', '')

        # Ensure exactly five fields are provided.
        if len(request.json) != 5:
            return jsonify({'error': 'Please provide exactly 5 fields.'}), 400

        # Ensure no field exceeds 25 characters in length.
        params = [guest, event, date, time, location]
        # Improper character length check without converting value to a string before checking 
        if any(len(i) > 25 for i in params):
            return jsonify({'error': 'Each field must not exceed 25 characters.'}), 400

        # Construct the invitation string using the input from the user.
        # SSTI VULNERABILITY: Using render_template_string with user-controlled input without sanitization or escaping
        # allows an attacker to inject malicious template syntax, leading to arbitrary code execution
        invitation_string = (
            f"Dear {guest},\n\n"
            f"We are delighted to invite you to the auspicious occasion of '{event}'.\n"
            f"The event will be held on {date} at {time}.\n"
            f"Please join us at {location} for a memorable experience filled with joy and celebration.\n\n"
            f"Looking forward to your presence."
        )
        # Render the invitation string directly with the user inputs, leading to an SSTI vulnerability
        return render_template_string(invitation_string)

    return render_template('invitation.html')

if __name__ == '__main__':
    try:
        # Attempt to create the users table at startup.
        create_users_table()
    except Exception as e:
        # Log any errors encountered during table creation.
        app.logger.error(f"Error during table creation: {e}")
    app.run(debug=True, host='0.0.0.0', port=4242)

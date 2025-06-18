from flask import Flask, request, redirect, render_template, send_from_directory, current_app, url_for
import os
import hmac
import hashlib
from uuid import uuid4

# Initialize Flask application with the templates directory specified
app = Flask(__name__, template_folder='templates')

# Read the flag from flag.txt, or provide a default one if not found
def read_flag():
    try:
        with open('flag.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return "CTFLIB{ex4mpl3-fl4g}"

# Initialize the messages list with the first message containing the Flag
FLAG = read_flag()
messages = [FLAG]
# Here us the vulnerability, using format string incorrectly
SECRET_KEY = "secret-{uuid4}"


@app.route('/')
def root():
    return redirect(url_for('index'))

@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')



@app.route('/robots.txt')
def robots_txt():
    # Serve the robots.txt file
    return send_from_directory(app.static_folder, 'robots.txt')


@app.route('/config-backup')
def config_backup():
    # Serve a backup configuration file, potential sensitive information exposure
    config_path = os.path.join(current_app.root_path, 'config-backup.txt')
    try:
        with open(config_path, 'r') as f:
            config_content = f.read()
        return f"<pre>{config_content}</pre>", 200
    except Exception as e:
        return f"Error reading config file: {e}", 500


def generate_token(id):
    # Generate a secure token for message authentication, but using an insecure SECRET_KEY
    return hmac.new(SECRET_KEY.encode(), str(id).encode(), hashlib.sha256).hexdigest()


@app.route('/secret')
def secret():
    # This route will now just render a 'secret.html' that gives users a hint
    return render_template('secret.html')


@app.route('/create_message', methods=['GET', 'POST'])
def create_message():
    # Create a message and generate a token for it
    if request.method == 'POST':
        data = request.form.get('data', 'no data provided.')
        id = len(messages)
        messages.append(data)
        token = generate_token(id)
        return redirect(f'/message?id={id}&token={token}')
    return render_template('create_message.html')

@app.route('/message')
def view_message():
    # Validate token and display message if valid
    id = request.args.get('id', '-1')
    token = request.args.get('token', '')

    try:
        id = int(id)
    except ValueError:
        return 'Invalid ID format'

    if id < 0 or id >= len(messages):
        return 'Message not found'

    expected_token = generate_token(id)
    if token != expected_token:
        return 'Invalid token'

    message = messages[id]
    return render_template('view_message.html', message=message)


@app.route('/message_conf')
def message_conf():
    # Serve a configuration file for messages, potentially sensitive information exposure
    config_path = os.path.join(current_app.root_path, 'messages_conf.txt')
    try:
        with open(config_path, 'r') as f:
            config_content = f.read()
        return f"<pre>{config_content}</pre>", 200
    except Exception as e:
        return f"Error reading config file: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, make_response

app = Flask(__name__)

# Function to load the flag
def load_flag():
    with open("flag.txt", "r") as file:
        return file.read().strip()

# Simulated data store for flags
flags = [
    {"id": 1, "name": "Azure Peace", "description": "A flag representing tranquility in the azure sky.", "in_stock": True},
    {"id": 2, "name": "Emerald Terrain", "description": "Symbolizes the lushness of vast green lands.", "in_stock": True},
    {"id": 3, "name": "Golden Triumph", "description": "Marks the victories achieved in golden times.", "in_stock": True},
    {"id": 4, "name": "Crimson Valor", "description": "A flag of bravery and strength in red.", "in_stock": True},
    {"id": 5, "name": "Cerulean Depths", "description": "Emblematic of the deep, mysterious oceans.", "in_stock": True},
    {"id": 6, "name": "Twilight Mystery", "description": "Captures the essence of the enigmatic twilight.", "in_stock": True},
    {"id": 7, "name": "Sunset Serenity", "description": "Represents the calmness of a beautiful sunset.", "in_stock": True},
    {"id": 8, "name": "Midnight Shadow", "description": "A dark flag, symbolizing the secrets of the night.", "in_stock": True},
    {"id": 9, "name": "Radiant Dawn", "description": "Signifies new beginnings and hope.", "in_stock": True},
    {"id": 10, "name": "Eternal Dusk", "description": "A reminder of the beauty in endings.", "in_stock": True},
    {"id": 100, "name": "Whispering Wind", "description": "Symbolizes the gentle, yet powerful force of nature.", "in_stock": False},
    {"id": 101, "name": "Mystic Flag", "description": load_flag(), "in_stock": False}
]
@app.route('/')
def index():
    # Determine if hidden flags should be shown based on the 'show_hidden' cookie
    show_hidden = request.cookies.get('show_hidden', 'false').lower() == 'true'
    # Filter flags to be displayed based on their stock status and the 'show_hidden' cookie
    available_flags = [flag for flag in flags if flag['in_stock'] or show_hidden]

    # Render the index page with the available flags and set the 'show_hidden' cookie accordingly
    response = make_response(render_template('index.html', flags=available_flags))
    response.set_cookie('show_hidden', 'true' if show_hidden else 'false')
    return response

# Route to display detailed description of a specific flag based on its ID
@app.route('/flag/<int:flag_id>')
def flag_description(flag_id):
    # Find the flag by ID or return None if not found
    flag = next((f for f in flags if f['id'] == flag_id), None)
    if not flag:
        return "Flag not found", 404

    # Check if the flag is in stock based on query parameter; if not, access is forbidden
    in_stock = request.args.get('in_stock', 'false').lower() == 'true'
    if in_stock:
        return render_template('flag_description.html', flag=flag)
    else:
        return "This flag is not in stock.", 403

# Start the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4242, debug=True)

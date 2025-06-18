import hmac
import hashlib

# Use the same simplified SECRET_KEY
SECRET_KEY = "secret-{uuid4}"

# Message ID for which you want to generate the token
message_id = "0"

# Recreating the token using the same method as in the Flask app
recreated_token = hmac.new(SECRET_KEY.encode(), message_id.encode(), hashlib.sha256).hexdigest()

print(recreated_token)


from flask import Flask, request, jsonify
import secrets

app = Flask(__name__)

users = {
    'user1': 'password1',
    'user2': 'password2',
}

tokens = {}

def generate_token():
    token = secrets.token_hex(16)
    return token

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if username in users and users[username] == password:
        token = generate_token()
        tokens[username] = token
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.before_request
def check_authentication():
    if request.endpoint != 'login':
        token = request.headers.get('Authorization')

        if token is None or token not in tokens.values():
            return jsonify({'message': 'Unauthorized'}), 401

@app.route('/protected_resource', methods=['GET'])
def protected_resource():
    return jsonify({'message': 'This is a protected resource'}), 200

if __name__ == '__main__':
    app.run(debug=True)

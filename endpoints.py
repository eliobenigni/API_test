from flask import Flask
app = Flask(__name__)

@app.route('/health')
def health():
    return 'API is up and running!'

# mock database
users = []

@app.route('/users', methods=['POST']) # POST method to create a new user
def create_user():
    user = request.get_json()
    user['id'] = len(users) + 1
    users.append(user)
    return jsonify(user), 201

@app.route('/users', methods=['GET']) # GET method to get all users
def get_users():
    return jsonify(users), 200

@app.route('/users/<int:user_id>', methods=['GET']) # GET method to get a user by id
def get_user(user_id):
    users = next((user for user in users if user['id'] == user_id), None
    if user is not None:
        return jsonify(user), 200
    else:
        return '', 404

@app.route('/users/<int:user_id>', methods=['PUT']) # PUT method to update a user by id
def update_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user is not None:
        user.update(request.get_json())
        return jsonify(user), 200
    else:
        return '', 404

@app.route('/users/<int:user_id>', methods=['DELETE']) # DELETE method to delete a user by id
def delete_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user is not None:
        users.remove(user)
        return '', 204
    else:
        return '', 404


if __name__ == '__main__':
    app.run()
from flask import Flask, request, jsonify
import unittest
import json

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
    user = next((user for user in users if user['id'] == user_id), None)
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

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = endpoints.app.test_client()
        self.app.testing = True 

    def test_health_endpoint(self):
        response = self.app.get('/health')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, 'API is up and running!')

    def test_user_creation(self):
        response = self.app.post('/users', data=json.dumps(dict(name='test', email='test@test.com')), content_type='application/json')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['name'], 'test')
        self.assertEqual(data['email'], 'test@test.com')

    def test_get_all_users(self):
        response = self.app.get('/users')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_get_user_by_id(self):
        response = self.app.get('/users/1')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], 1)

    def test_update_user(self):
        response = self.app.put('/users/1', data=json.dumps(dict(name='updated', email='updated@test.com')), content_type='application/json')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'updated')
        self.assertEqual(data['email'], 'updated@test.com')

    def test_delete_user(self):
        response = self.app.delete('/users/1')
        self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    app.run()
    unittest.main()
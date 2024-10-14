from flask import Flask, jsonify, request

app = Flask(__name__)


TOKEN = "mysecrettoken"
todos = []
next_id = 1

@app.before_request
def authenticate_token():
    token=request.headers.get("Authorization")
    if not token or token !=f"Bearer {TOKEN}":
        return jsonify({"error":"unauthorized"}),401
    

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos), 200


@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = next((todo for todo in todos if todo['id'] == todo_id), None)
    if todo is None:
        return jsonify({'message': 'To-Do not found'}), 404
    return jsonify(todo), 200


@app.route('/todos', methods=['POST'])
def create_todo():
    global next_id
    data = request.get_json()
    if 'title' not in data:
        return jsonify({'message': 'Title is required'}), 400
    new_todo = {
        'id': next_id,
        'title': data['title'],
        'completed': data.get('completed', False)
    }
    todos.append(new_todo)
    next_id += 1
    return jsonify(new_todo), 201


@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    todo = next((todo for todo in todos if todo['id'] == todo_id), None)
    if todo is None:
        return jsonify({'message': 'To-Do not found'}), 404
    todo['title'] = data.get('title', todo['title'])
    todo['completed'] = data.get('completed', todo['completed'])
    return jsonify(todo), 200


@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo['id'] != todo_id]
    return jsonify({'message': 'To-Do deleted'}), 200

if __name__ == '__main__':
    app.run(port=3000)

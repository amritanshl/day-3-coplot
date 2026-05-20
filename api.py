from flask import Flask, request, jsonify, abort
from uuid import uuid4

app = Flask(__name__)

# In-memory store for demo purposes
STORE = {}


def make_item(data):
    return {
        "id": str(uuid4()),
        "data": data
    }


@app.route('/items', methods=['GET'])
def list_items():
    """List all items"""
    return jsonify(list(STORE.values())), 200


@app.route('/items', methods=['POST'])
def create_item():
    """Create a new item. Expects JSON body (object or value)"""
    if not request.is_json:
        return jsonify({"error": "JSON body required"}), 400
    payload = request.get_json()
    item = make_item(payload)
    STORE[item['id']] = item
    return jsonify(item), 201


@app.route('/items/<item_id>', methods=['GET'])
def get_item(item_id):
    item = STORE.get(item_id)
    if not item:
        abort(404)
    return jsonify(item), 200


@app.route('/items/<item_id>', methods=['PUT', 'PATCH'])
def update_item(item_id):
    if not request.is_json:
        return jsonify({"error": "JSON body required"}), 400
    item = STORE.get(item_id)
    if not item:
        abort(404)
    payload = request.get_json()
    # Replace data
    item['data'] = payload
    STORE[item_id] = item
    return jsonify(item), 200


@app.route('/items/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = STORE.pop(item_id, None)
    if not item:
        abort(404)
    return '', 204


if __name__ == '__main__':
    # Run for local development
    app.run(host='0.0.0.0', port=5000, debug=True)

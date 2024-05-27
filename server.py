from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# A dictionary to store token trigger events
token_triggers = {}

@app.route('/id', methods=['GET'])
def token_triggered():
    token_id = request.args.get('')
    if token_id:
        # Log the token trigger event with timestamp
        token_triggers[token_id] = datetime.now()
        #TODO: Get token information from REDIS and generate alert
        return jsonify({"status": "success", "token_id": token_id, "timestamp": token_triggers[token_id]}), 200
    else:
        return jsonify({"status": "error", "message": "Missing token ID"}), 400

@app.route('/triggers', methods=['GET'])
def get_triggers():
    return jsonify(token_triggers), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


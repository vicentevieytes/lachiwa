from flask import Flask, request, jsonify
from datetime import datetime
import redismanager
from lachiwa import Token, URLToken, QRToken, ExcelToken

app = Flask(__name__)

# A dictionary to store token trigger events
token_triggers = {}

@app.route('/', methods=['GET'])
def token_triggered():
    token_id = request.args.get('id')
    #TODO: Solo realizar este paso si el token existe en redis
    if token_id:
        # Log the token trigger event with timestamp
        if token_id in token_triggers:
            token_triggers[token_id].append(datetime.now())
        else:
            token_triggers[token_id] = []
        token_attributes = redismanager.get_token_attributes(token_id)
        alert = alert_from_token_attributes(token_attributes)
        alert.send_mail()
        redismanager.write_alert_to_redis(alert)
        
        return jsonify({"status": "success", "token_id": token_id, "timestamp": token_triggers[token_id]}), 200
    else:
        return jsonify({"status": "error", "message": "Missing token ID"}), 400

@app.route('/triggers', methods=['GET'])
def get_triggers():
    return jsonify(token_triggers), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


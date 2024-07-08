from flask import Flask, request, jsonify
from datetime import datetime
import redismanager
from honeytokens import Token, URLToken, QRToken, ExcelToken
from alerts import Alert

app = Flask(__name__)

@app.route('/', methods=['GET'])
def token_triggered():
    token_id = request.args.get('id')
    if token_id:
        # Log the token trigger event with timestamp
        token = redismanager.fetch_token(token_id)
        if token is None:
            return jsonify({"status": "error", "message": f"{token_id} is not a valid token"}, 400)
        alert = Alert(token= token, remote_ip = request.remote_addr)
        redismanager.store_alert(alert)
        alert.log_alert()
        return jsonify({"status": "success", "token_id": token_id, }), 200
    else:
        return jsonify({"status": "error", "message": "Missing token ID"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


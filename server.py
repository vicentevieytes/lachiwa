from flask import Flask, request, jsonify
from datetime import datetime
import redismanager
from honeytokens import Token, URLToken, QRToken, ExcelToken
from alerts import HoneytokenAlert, log_alert
import sys

app = Flask(__name__)


@app.route('/', methods=['GET'])
def token_triggered():
    token_id = request.args.get('id')
    
    if not token_id:
        return jsonify({"status": "error", "message": "Missing token ID"}), 400
    
    token = redismanager.fetch_token(token_id)
    
    if token is None:
        return jsonify({"status": "error", "message": f"{token_id} is not a valid token"}), 400
    
    alert = HoneytokenAlert(
        token_id=token_id,
        remote_ip=request.remote_addr
    )
    
    redismanager.store_alert(alert)
    log_alert(token, alert)
    
    return jsonify({"status": "success", "token_id": token_id}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


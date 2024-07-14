from honeytokens import Token
from datetime import datetime
from redis_om import HashModel, Field
from typing import Optional

class HoneytokenAlert(HashModel):
    token_id: str = Field(index=True)
    timestamp: Optional[datetime] = Field(index=True)
    remote_ip: str

    def __init__(self, **data):
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now()
        super().__init__(**data)


def log_alert(token: Token, alert: HoneytokenAlert):
    with open(f"alerts/alert_log", "a") as alert_log:
        alert_log.write(f"Alert_timestamp: {alert.timestamp.isoformat()} Token_type: {token.token_type} Description: {token.description} Creation_timestamp: {token.timestamp.isoformat()} Token_id: {token.pk} Remote_ip: {alert.remote_ip}\n")




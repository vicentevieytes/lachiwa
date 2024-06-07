from honeytoken import Token
from datetime import datetime

class Alert:
    def __init__(self, token: Token):
        self.token = token
        self.id = token.id
        self.token_type = token.token_type
        self.host = token.host
        self.token_timestamp = token.timestamp
        self.email = token.email
        self.description = token.description
        self.timestamp = datetime.now()

    def log_alert(self):
        with open(f"alerts/alert_log", "a") as alert_log:
            alert_log.write(f"{self.timestamp} {self.token_type} Token:{self.id} {self.description}\n")

#TODO: def send_alert_email(self):



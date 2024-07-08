from honeytokens import Token
from datetime import datetime
from redis_om import HashModel, Field

class Alert(HashModel):
    timestamp: datetime = Field(index = True)
    token_id: str | None = Field(index = True)
    token_type: str = Field(index = True)
    token_description: str
    remote_ip: str | None = Field(index= True)
    
    def __init__(self, token: Token, remote_ip: str | None, **kwargs):
        super().__init__(**kwargs)
        self.token_id = token.pk
        self.token_description = token.description
        self.token_type = token.__class__.__name__
        self.timestamp = datetime.now()
        self.remote_ip = remote_ip       

    def log_alert(self):
        with open(f"alerts/alert_log", "a") as alert_log:
            alert_log.write(f"{self.timestamp} {self.token_type} Token:{self.token_id} Remote_ip:{self.remote_ip} Description: {self.description}\n")

#TODO: def send_alert_email(self):



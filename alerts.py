from lachiwa import Token, URLToken, QRToken, ExcelToken
import redismanager
from datetime import datetime

class TriggerEvent:
    def __init__(self, token_id: str, remote_ip: str):
        self.token_id = token_id
        self.remote_ip = remote_ip
        self.timestamp = datetime.now()

    def __str__(self):
        return (f"TriggerEvent(token_id = {self.token_id}, remote_ip = {self.remote_ip}, timestamp = {self.timestamp}")
    
class Alert:
    def __init__(



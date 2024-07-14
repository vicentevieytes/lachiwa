import os
from datetime import datetime
from honeytokens import *
from alerts import HoneytokenAlert
from typing import Awaitable, Union, Optional
from redis_om import get_redis_connection, NotFoundError

def store_token(token: Token):
    redis_conn = get_redis_connection(port = 6379)
    
    # Token is saved with a different PK prefix deppending on it's class.
    # URLToken would be saved like this:
    # ":honeytokens.URLToken:01J2CW166KEKT4KTDARK2FPQD4"
    token.save()
    
    # The specific class of the token is stored separately.
    redis_conn.set(f"token_type:{token.pk}", token.__class__.__name__)

def fetch_token(token_id: str) -> Token|None:
    redis_conn = get_redis_connection(port = 6379)

    # Retrieve the token type
    token_type = redis_conn.get(f"token_type:{token_id}")
    if not token_type:
        return None

    # Get the corresponding class
    token_class = globals().get(token_type)
    if not token_class:
        raise ValueError("Invalid token type")

    # Query the token
    return token_class.get(token_id)

def store_alert(alert: HoneytokenAlert):
    alert.save()


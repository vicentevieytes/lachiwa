import os
from datetime import datetime
from honeytokens import Token, URLToken
from alerts import HoneytokenAlert
from typing import Awaitable, Union, Optional
from redis_om import get_redis_connection, NotFoundError

def store_token(token: Token):
    redis_conn = get_redis_connection(port = 6379)
    token.save()
    redis_conn.set(f"token_type:{token.pk}", token.__class__.__name__)

def fetch_token(token_id: str) -> Token|None:
    redis_conn = get_redis_connection(port = 6379)
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


def main():
    print(type(fetch_token("qhcYAwII3H").timestamp))

if __name__ == "__main__":
    main()

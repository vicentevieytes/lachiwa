import os
from datetime import datetime
from honeytokens import Token
from alerts import Alert
from typing import Awaitable, Union, Optional
from redis_om import NotFoundError

def store_token(token: Token):
    print(token)
    token.save()

def fetch_token(token_id: str) -> Token|None:
    try:
        return Token.get(token_id)
    except NotFoundError:
        print("not found token")
        return None

def store_alert(alert: Alert):
    alert.save()


def main():
    print(type(fetch_token("qhcYAwII3H").timestamp))

if __name__ == "__main__":
    main()

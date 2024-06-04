import redis
import os
from datetime import datetime
from lachiwa import Token, Alert
from typing import Awaitable, Union, Optional
def token_key(token_id: str):
   return(f"Token:{token_id}")

def alert_key(token_id):
    return(f"Alert:{token_id}")


def get_redis_client() -> redis.StrictRedis:
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', 6379))
    return redis.StrictRedis(host=redis_host,port=redis_port, db=0)

def save_token(token: Token) -> Optional[bool]:
    redis_client = get_redis_client()
    try:
        key = f"Token:{token.id}"
        token_data = {
            "host": token.host,
            "description": token.description,
            "email": token.email,
            "token_type": token.token_type,
            "timestamp": token.timestamp.isoformat(),
            "id": str(token.id)
        }
        redis_client.hset(key, mapping=token_data)
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        # Ensure the Redis connection is closed properly
        redis_client.close()

def get_token_attributes(token_id: str) -> Union[Awaitable[dict], dict, None]:
    redis_client = get_redis_client()
    key = token_key(token_id)
    try:
        if not redis_client.exists(key):
            print(f"Token ID {token_id} does not exist.")
            return None
        return redis_client.hgetall(key)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        redis_client.close()

def fetch_token(token_id: str) -> Token:
    token_attributes = get_token_attributes(token_id)
    return Token.from_dict(token_attributes)

def store_alert(alert: Alert) -> Optional[bool]:
    redis_client = get_redis_client()
    timestamp = datetime.utcnow().isoformat()
    try:
        key = alert_key(alert.id)
        redis_client.rpush(key, timestamp) 
        redis_client.hset("latest_alerts", alert.id, timestamp)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        # Ensure the Redis connection is closed properly
        redis_client.close()

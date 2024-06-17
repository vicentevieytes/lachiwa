import redis
import os
from datetime import datetime
from honeytokens import Token
from alerts import Alert
from typing import Awaitable, Union, Optional

def token_key(token_id: str):
   return(f"Token:{token_id}")

def alert_key(token_id):
    return(f"Alert:{token_id}")


def get_redis_client() -> redis.StrictRedis:
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', 6379))
    return redis.StrictRedis(host=redis_host,port=redis_port, decode_responses=True, db=0)

def store_token(token: Token) -> Optional[bool]:
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
        redis_client.hset(key,mapping=token_data)
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
    if not redis_client.exists(key):
        print(f"Token ID {token_id} does not exit.")
        return None
    token_attributes = redis_client.hgetall(key) 
    token_attributes["timestamp"] = datetime.fromisoformat(token_attributes["timestamp"]) #type: ignore
    return token_attributes

def fetch_token(token_id: str) -> Token|None:
    token_attributes = get_token_attributes(token_id)
    if token_attributes is not None:
        return Token.from_dict(token_attributes)
    return None


# For every token which has been alerted, there is a Alert:token_id key, which maps to a list of all the individual timestamps when it was alerted.
def store_alert(alert: Alert) -> Optional[bool]:
    redis_client = get_redis_client()
    timestamp = datetime.now().isoformat()
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

def main():
    print(type(fetch_token("qhcYAwII3H").timestamp))

if __name__ == "__main__":
    main()

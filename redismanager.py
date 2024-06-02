import redis
import os
from lachiwa import Token
from typing import Awaitable, Union, Optional

def get_redis_client() -> redis.StrictRedis:
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', 6379))
    return redis.StrictRedis(host=redis_host,port=redis_port, db=0)

def save_token(token: Token) -> Optional[bool]:
    redis_client = get_redis_client()
    try:
        token_key = f"Token:{token.id}"
        token_data = {
            "host": token.host,
            "description": token.description,
            "email": token.email,
            "token_type": token.token_type,
            "timestamp": token.timestamp.isoformat(),
            "id": str(token.id)
        }
        redis_client.hset(token_key, mapping=token_data)
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        # Ensure the Redis connection is closed properly
        redis_client.close()

def get_token_attributes(token_id: str) -> Union[Awaitable[dict], dict, None]:
    redis_client = get_redis_client()
    token_key = f"Token:{token_id}"
    try:
        if not redis_client.exists(token_key):
            print(f"Token ID {token_id} does not exist.")
            return None
        return redis_client.hgetall(token_key)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        redis_client.close()

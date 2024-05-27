import click
from trogon import tui
from lachiwa import Token, URLToken, QRToken
import redis
import os

def save_to_redis(token: Token):
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', 6379))
    #Redis connection
    redis_client = redis.StrictRedis(host=redis_host,port=redis_port, db=0)
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
    finally:
        # Ensure the Redis connection is closed properly
        redis_client.close()

@tui()
@click.command()
@click.option('--host', prompt='Host', help='The host for the honeytoken.', type= str)
@click.option('--description', prompt='Description', help='Description of the honeytoken.', type= str)
@click.option('--email', prompt='Email', help='Email associated with the honeytoken.',type= str)
@click.option('--token_type', prompt='Token Type', help='Type of the honeytoken.',type= str)
def create_honeytoken(host: str, description: str, email: str, token_type: str):
    return from_token_type_str(host, description, email, token_type)

def from_token_type_str(host: str, description: str, email: str, token_type: str) -> "Token":
    match token_type:
        case "url":
            token = URLToken(host, description, email)
            save_to_redis(token)
            click.echo(f"Generated URL: {token.url}")
            click.echo(f"Token Details: {token}")
            return token
        case "qr":
            token = QRToken(host, description, email)
            save_to_redis(token)
            click.echo(f"Generated QR: {token.filename}")
            click.echo(f"Token Details: {token}")
            return token
        case _:
            print("Wrong token type indicated")
            exit(1)

if __name__ == '__main__':
    create_honeytoken()

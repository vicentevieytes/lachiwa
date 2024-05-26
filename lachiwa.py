import click
import uuid
from datetime import datetime

class Token:
    def __init__(self, host, description, email, token_type):
        self.host = host
        self.description = description
        self.email = email
        self.token_type = token_type
        self.created_at = datetime.now()
        self.id = uuid.uuid4()

    def __str__(self):
        return (f"Token(host={self.host}, description={self.description}, email={self.email}, "
                f"token_type={self.token_type}, created_at={self.created_at}, id={self.id})")

class URLToken(Token):
    def __init__(self, host, description, email):
        super().__init__(host, description, email,"URLToken")
        self.url = f"http://{self.host}/id?={self.id}"

    def __str__(self):
        return (f"URLToken(host={self.host}, description={self.description}, email={self.email}, "
                f"token_type={self.token_type}, created_at={self.created_at}, id={self.id}, url={self.url})")

@click.command()
@click.option('--host', prompt='Host', help='The host for the honeytoken.')
@click.option('--description', prompt='Description', help='Description of the honeytoken.')
@click.option('--email', prompt='Email', help='Email associated with the honeytoken.')
#@click.option('--token_type', prompt='Token Type', help='Type of the honeytoken.')
def create_honeytoken(host, description, email):
    token = URLToken(host, description, email)
    click.echo(f"Generated URL: {token.url}")
    click.echo(f"Token Details: {token}")

if __name__ == '__main__':
    create_honeytoken()

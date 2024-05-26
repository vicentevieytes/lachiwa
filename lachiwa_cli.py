import click
from lachiwa import Token, URLToken, QRToken

@click.command()
@click.option('--host', prompt='Host', help='The host for the honeytoken.')
@click.option('--description', prompt='Description', help='Description of the honeytoken.')
@click.option('--email', prompt='Email', help='Email associated with the honeytoken.')
@click.option('--token_type', prompt='Token Type', help='Type of the honeytoken.')
def create_honeytoken(host: str, description: str, email: str, token_type: str):
    return from_token_type_str(host, description, email, token_type)

def from_token_type_str(host: str, description: str, email: str, token_type: str) -> "Token":
    match token_type:
        case "url":
            token = URLToken(host, description, email)
            click.echo(f"Generated URL: {token.url}")
            click.echo(f"Token Details: {token}")
            return token
        case "qr":
            token = QRToken(host, description, email)
            click.echo(f"Generated QR: {token.filename}")
            click.echo(f"Token Details: {token}")
            return token
        case _:
            print("Wrong token type indicated")
            exit(1)

if __name__ == '__main__':
    create_honeytoken()

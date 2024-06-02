import click
from trogon import tui
from lachiwa import Token, URLToken, QRToken, ExcelToken
from redismanager import save_token 

@tui()
@click.command()
@click.option('--host', prompt='Host', help='The host for the honeytoken.', type=str)
@click.option('--description', prompt='Description', help='Description of the honeytoken.', type=str)
@click.option('--email', prompt='Email', help='Email associated with the honeytoken.', type=str)
@click.option('--token_type', prompt='Token Type', help='Type of the honeytoken.', type=str)
def create_honeytoken(host: str, description: str, email: str, token_type: str):
    return from_token_type_str(host, description, email, token_type)


def from_token_type_str(host: str, description: str, email: str, token_type: str) -> Token:
    token = Token.from_token_type_str(host, description, email, token_type)
    save_token(token)
    match token:
        case URLToken():
            click.echo(f"Generated URL: {token.url}")
        case QRToken():
            click.echo(f"Generated QR: {token.filename}")
        case ExcelToken():
            click.echo(f"Generated Excel: {token.filename}")
        case _:
            print("Wrong token type indicated")
            exit(1)
    click.echo(f"Token Details: {token}")
    return token

if __name__ == '__main__':
    create_honeytoken()

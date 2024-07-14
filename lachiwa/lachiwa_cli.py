import click
from honeytokens import DockerfileToken, Token, URLToken, QRToken, ExcelToken, HTMLToken, WindowsDirectoryToken
from redismanager import store_token


def common_options(f):
    """Common options for all tokens."""
    f = click.option('--host', required=True,
                     help='The host for the token.')(f)
    f = click.option('--description', required=True,
                     help='The description for the token.')(f)
    return f


@click.group()
def create():
    """Create a token."""
    pass


@create.command()
@common_options
def urltoken(host, description):
    token = URLToken(
        host = host,
        description = description,
    )
    token.write_out()
    store_token(token)
    click.echo(f"Your URLToken: {token.url()}")


@create.command()
@common_options
def qrtoken(host, description):
    token = QRToken(
        host = host,
        description = description,
    )
    token.write_out()
    store_token(token)
    click.echo(f"Your QRToken file: {token.filename()}")

@create.command()
@common_options
def exceltoken(host, description):

    token = ExcelToken(
        host = host,
        description = description,
    )
    token.write_out()
    store_token(token)
    click.echo(f"Your ExcelToken file: {token.filename()}")


@create.command()
@common_options
def dockertoken(host, description):
    token = DockerfileToken(
        host = host,
        description = description,
    )
    token.write_out()
    store_token(token)
    click.echo(f"Your DockerfileToken file: {token.filename()}")


@create.command()
@common_options
@click.option("--file", required=True, help="file path for input html file")
@click.option("--allowed", required=True, help="The domain where your website should be hosted at")
def htmltoken(host, description, file, allowed):
    token = HTMLToken(
        host = host,
        description = description,
        allowed_url = allowed,
        input_html_path = file)
    token.write_out()
    store_token(token)
    click.echo(f"Your HTMLToken file: {token.filename()}")


@create.command()
@common_options
def windowstoken(host, description):
    token = WindowsDirectoryToken(
        host = host,
        description = description,
    ) 
    token.write_out()
    store_token(token)
    click.echo(f"Your WindowsToken file: {token.filename()}")


@click.group()
def get():
    """Create a token."""
    pass


@get.command()
def alerts():
    print("traeme las alertas wachin")


@click.group()
def cli():
    pass


cli.add_command(create)
cli.add_command(get)

if __name__ == '__main__':
    cli()

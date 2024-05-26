import click
import uuid
from datetime import datetime
import qrcode

def create_qr_code(url, file_name):
    # Create a QR code object
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    # Add data to the QR code
    qr.add_data(url)
    qr.make(fit=True)
    # Create an image from the QR code object
    img = qr.make_image(fill_color="black", back_color="white")
    # Save the image to a file
    img.save(file_name)
    print(f"QR code saved as {file_name}")

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

class QRToken(Token):
    def __init__(self, host, description, email):
        super().__init__(host, description, email, "QRToken")
        self.qr = create_qr_code(f"http://{self.host}/id?={self.id}", f"honeytokens/QR{datetime.today()}.jpg")
        
@click.command()
@click.option('--host', prompt='Host', help='The host for the honeytoken.')
@click.option('--description', prompt='Description', help='Description of the honeytoken.')
@click.option('--email', prompt='Email', help='Email associated with the honeytoken.')
@click.option('--token_type', prompt='Token Type', help='Type of the honeytoken.')
def create_honeytoken(host, description, email, token_type):
    if token_type == "url": 
        token = URLToken(host, description, email)
        click.echo(f"Generated URL: {token.url}")
        click.echo(f"Token Details: {token}")
    elif token_type == "qr":
        token = QRToken(host, description, email)




if __name__ == '__main__':
    create_honeytoken()

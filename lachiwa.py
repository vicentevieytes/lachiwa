import uuid
from datetime import datetime
from qrcode.main import QRCode
from qrcode.constants import ERROR_CORRECT_L

def url_from_host_and_tokenid(host, id, protocol="http"): 
    return f"{protocol}://{host}/id?={id}"

class Token:
    def __init__(self, host: str, description: str, email: str, token_type: str):
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
        self.url = url_from_host_and_tokenid(self.host, self.id, "http")

    def __str__(self):
        return (f"URLToken(host={self.host}, description={self.description}, email={self.email}, "
                f"token_type={self.token_type}, created_at={self.created_at}, id={self.id}, url={self.url})")


class QRToken(Token):
    def __init__(self, host: str, description :str, email: str):
        super().__init__(host, description, email, "QRToken")
        self.filename = f"QR_{description}_{datetime.today()}.jpg"
        self.create_qr_code(url_from_host_and_tokenid(self.host, self.id), f"honeytokens/{self.filename}")

    def create_qr_code(self, url: str, file_name :str):
        # Create a QR code object
        qr = QRCode(
            version=1,
            error_correction=ERROR_CORRECT_L,
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




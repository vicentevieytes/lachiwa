from datetime import datetime
from qrcode.main import QRCode
from qrcode.constants import ERROR_CORRECT_L
import nanoid
from openpyxl import Workbook


def url_from_host_and_tokenid(host, id, protocol="http"):
    return f"{protocol}://{host}/?id={id}"

class Token:
    def __init__(self, host: str, description: str, email: str, token_type: str):
        self.host = host
        self.description = description
        self.email = email
        self.token_type = token_type
        self.timestamp = datetime.now()
        self.id = nanoid.generate(size=10)

    def __str__(self):
        return (f"Token(host={self.host}, description={self.description}, email={self.email}, "
                f"token_type={self.token_type}, timestamp={self.timestamp}, id={self.id})")
    
    @classmethod
    def from_token_type_str(cls, host: str, description: str, email: str, token_type: str) -> "Token":
        match token_type:
            case "url":
                token = URLToken(host, description, email)
                return token
            case "qr":
                token = QRToken(host, description, email)
                return token
            case "ExcelToken":
                token = ExcelToken(host, description, email)
                return token
            case _:
                print("Wrong token type indicated")
                exit(1)


class URLToken(Token):
    def __init__(self, host, description, email):
        super().__init__(host, description, email, "URLToken")
        self.url = url_from_host_and_tokenid(self.host, self.id, "http")
        with open(f"honeytokens/URL_{description}_{datetime.today()}", "w") as output_file:
            output_file.write(self.url)

    def __str__(self):
        return (f"URLToken(host={self.host}, description={self.description}, email={self.email}, "
                f"token_type={self.token_type}, timestamp={self.timestamp}, id={self.id}, url={self.url})")


class QRToken(Token):
    def __init__(self, host: str, description: str, email: str):
        super().__init__(host, description, email, "QRToken")
        self.filename = f"QR_{description}_{datetime.today()}.jpg"
        self.create_qr_code(url_from_host_and_tokenid(
            self.host, self.id), f"honeytokens/{self.filename}")

    def create_qr_code(self, url: str, file_name: str):
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


class ExcelToken(Token):

    def __init__(self, host: str, description: str, email: str):
        super().__init__(host, description, email, "ExcelToken")
        self.filename = f"Excel_{description}_{datetime.today()}.xlsx"
        self.create_excel_file(f"honeytokens/{self.filename}")

    def create_excel_file(self, file_name: str):
        workbook = Workbook()
        workbook.active
        workbook.save(file_name)

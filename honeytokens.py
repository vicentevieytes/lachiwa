from datetime import datetime
from qrcode.main import QRCode
from qrcode.constants import ERROR_CORRECT_L
import nanoid
from openpyxl import Workbook
from typing import Optional


def url_from_host_and_tokenid(host, id, protocol="http"):
    return f"{protocol}://{host}/?id={id}"


class Token:
    def __init__(
        self,
        host: str,
        description: str,
        email: str,
        token_type: str,
        id: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ):
        self.host = host
        self.description = description
        self.email = email
        self.token_type = token_type
        self.timestamp = timestamp if timestamp is not None else datetime.now()
        self.id = id if id is not None else nanoid.generate(size=10)
        self.url = url_from_host_and_tokenid(host, self.id)

    def __str__(self):
        return (
            f"Token(host={self.host}, description={self.description}, email={self.email}, "
            f"token_type={self.token_type}, timestamp={self.timestamp}, id={self.id})"
        )

    @classmethod
    def from_token_type_str(
        cls,
        host: str,
        description: str,
        email: str,
        token_type: str,
        id: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ) -> "Token":
        match token_type:
            case "URLToken":
                token = URLToken(host, description, email, id=id, timestamp=timestamp)
                return token
            case "QRToken":
                token = QRToken(host, description, email, id=id, timestamp=timestamp)
                return token
            case "ExcelToken":
                token = ExcelToken(host, description, email, id=id, timestamp=timestamp)
                return token
            case _:
                print("Wrong token type indicated")
                exit(1)

    @classmethod
    def from_dict(cls, token_attributes_mapping):
        id = token_attributes_mapping.get("id")
        host = token_attributes_mapping.get("host")
        description = token_attributes_mapping.get("description")
        email = token_attributes_mapping.get("email")
        token_type = token_attributes_mapping.get("token_type")
        timestamp = token_attributes_mapping.get("timestamp")
        return Token.from_token_type_str(host, description, email, token_type, id=id, timestamp=timestamp)

    def write_out(self) -> None:
        pass


class URLToken(Token):
    def __init__(self, host, description, email, id: Optional[str] = None, timestamp=None):
        super().__init__(host, description, email, "URLToken", id=id, timestamp=timestamp)

    def write_out(self):
        with open(
            f"honeytokens/URL_{self.description}_{self.timestamp}", "w"
        ) as output_file:
            output_file.write(self.url)

    def __str__(self):
        return (
            f"URLToken(host={self.host}, description={self.description}, email={self.email}, "
            f"token_type={self.token_type}, timestamp={self.timestamp}, id={self.id}, url={self.url})"
        )


class QRToken(Token):
    def __init__(self, host: str, description: str, email: str, id: Optional[str] = None, timestamp=None):
        super().__init__(host, description, email, "QRToken", id=id, timestamp=timestamp)
        self.filename = f"QR_{description}_{datetime.today()}.jpg"

    def write_out(self):
        self.create_qr_code(f"honeytokens/{self.filename}")

    def create_qr_code(self, file_name: str):
        # Create a QR code object
        qr = QRCode(
            version=1,
            error_correction=ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        # Add data to the QR code
        qr.add_data(self.url)
        qr.make(fit=True)
        # Create an image from the QR code object
        img = qr.make_image(fill_color="black", back_color="white")
        # Save the image to a file
        img.save(file_name)


class ExcelToken(Token):

    def __init__(self, host: str, description: str, email: str, id: Optional[str] = None, timestamp=None):
        super().__init__(host, description, email, "ExcelToken", id=id, timestamp=timestamp)
        self.filename = f"Excel_{description}_{datetime.today()}.xlsx"

    def write_out(self):
        self.create_excel_file(f"honeytokens/{self.filename}")

    def create_excel_file(self, file_name: str):
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Data"

        # Canary Token hiden in the excel
        hidden_sheet = workbook.create_sheet(title="Hidden")
        hidden_sheet["A1"] = self.url
        workbook.active.sheet_state = "hidden"

        workbook.save(file_name)


class DockerfileToken(Token):
    def __init__(self, host: str, description: str, email: str, id: Optional[str] = None, timestamp=None):
        super().__init__(host, description, email, "DockerfileToken", id=id, timestamp = timestamp)
        self.dockerfile_content = ""

    def write_out(self):
        with open(
            f"honeytokens/Dockerfile{self.description}{self.timestamp}.txt", "w"
        ) as output_file:
            output_file.write(self.dockerfile_content)

    def create_honeytoken(self, dockerfile_content: str): 
        honeytoken_content = f"""
RUN exec {{NFD}}<>/dev/tcp/{self.url}/80 <<EOF
GET / HTTP/1.1
Host: {self.url}
EOF
"""
        self.dockerfile_content = dockerfile_content + "\n" + honeytoken_content

# class DockerfileToken2(Token): 
#    def __init__(
#        self, host: str, description: str, email: str, id: Optional[str] = None
#    ):
#        super().__init__(host, description, email, "DockerfileToken", id=id)
#        self.dockerfile_content = ""
#
#    def write_out(self):
#        with open(
#            f"honeytokens/Dockerfile{self.description}{self.timestamp}.txt", "w"
#        ) as output_file:
#            output_file.write(self.dockerfile_content)
#
#    def str(self):
#        return (
#            f"DockerfileToken(host={self.host}, description={self.description}, email={self.email}, "
#            f"token_type={self.token_type}, timestamp={self.timestamp}, id={self.id}, dockerfile_content={self.dockerfile_content})"
#        )
#
#    def create_honeytoken(self, dockerfile_content: str):
#        honeytoken_content = (
#            f"RUN nc {self.url} 80"  # Asuming that has netcat, short and simple. CANT ASSUME THIS.
#        )
#
#        self.dockerfile_content = dockerfile_content + "\n" + honeytoken_content
#
#    def write_dockerfile(self):
#        with open(
#            f"honeytokens/Dockerfile{self.description}{self.timestamp}.txt", "w"
#        ) as output_file:
#            output_file.write(self.dockerfile_content)
#

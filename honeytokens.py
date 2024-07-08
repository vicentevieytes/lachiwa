from datetime import datetime
from io import BytesIO
import shutil
import tempfile
from zipfile import ZipFile
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
        timestamp: Optional[datetime] = None,
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
        timestamp: Optional[datetime] = None,
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
        return Token.from_token_type_str(
            host, description, email, token_type, id=id, timestamp=timestamp
        )

    def write_out(self) -> None:
        pass


class URLToken(Token):
    def __init__(
        self, host, description, email, id: Optional[str] = None, timestamp=None
    ):
        super().__init__(
            host, description, email, "URLToken", id=id, timestamp=timestamp
        )

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
    def __init__(
        self,
        host: str,
        description: str,
        email: str,
        id: Optional[str] = None,
        timestamp=None,
    ):
        super().__init__(
            host, description, email, "QRToken", id=id, timestamp=timestamp
        )
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

    def __init__(self, host: str, description: str, email: str):
        super().__init__(host, description, email, "ExcelToken")
        self.filename = f"Excel_{description}_{datetime.today()}.xlsx"
        self.makeToken(f"honeytokens/{self.filename}")

    def makeToken(self, file_name: str):
        with open(file_name, "rb") as f:
            input_buf = BytesIO(f.read())
        output_buf = BytesIO()
        # un XML es esencialmente un ZIP file (Open XML standard), por eso
        # creamos un ZIP
        output_zip = ZipFile(output_buf, "w")

        # El XML tiene diferentes contenidos, solo queremos modificar el workbook.xml
        # y sus relaciones
        with ZipFile(input_buf, "r") as doc:
            for entry in doc.filelist:
                if entry.external_attr:  # Aca se hace ademas que sea un
                    # directory, no se que tan necesario sea, porque no veo
                    # que se creen directorios
                    continue
                dirname = tempfile.mkdtemp()
                fname = doc.extract(entry, dirname)
                url = url_from_host_and_tokenid(self.host, self.id)
                with open(fname, "r") as fd:
                    contents = fd.read().replace(search="HONEYDROP_TOKEN_URL", url=url)
                shutil.rmtree(dirname)
                output_zip.writestr(entry, contents)

        output_zip.close()
        output_buf.seek(0)
        with open(file_name, "wb") as f:
            f.write(output_buf.read())
        output_buf.close()

        """
        Supuestamente esta es otra manera de hacerlo, poniendo un pedazo de codigo que se ejecute cuando se abre
        el archivo, pero no la puedo probar...
        https://www.xlwings.org
        """
        # wb = xw.Book()

        # # Añade el VbModule
        # vbmodule = wb.api.VBProject.VBComponents.Add(1)

        # # escribimos para que se ejecute la url
        # url = url_from_host_and_tokenid(self.host, self.id)
        # vbmodule.CodeModule.AddFromString(f"""
        # Private Sub Workbook_Open()
        #     ThisWorkbook.FollowHyperlink "{url}"
        # End Sub
        # """)

        # wb.save(file_name)
        # wb.close()


class DockerfileToken(Token):
    def __init__(
        self,
        host: str,
        description: str,
        email: str,
        id: Optional[str] = None,
        timestamp=None,
    ):
        super().__init__(
            host, description, email, "DockerfileToken", id=id, timestamp=timestamp
        )
        self.filename = f"Dockerfile_{description}_{self.timestamp}"
        self.create_honeytoken()

    def write_out(self):
        with open(
            f"honeytokens/Dockerfile{self.description}{self.timestamp}.txt", "w"
        ) as output_file:
            output_file.write(self.dockerfile_payload)

    def create_honeytoken(self):
        self.dockerfile_payload = f"""
        CMD ["bash", "-c", "echo -e 'GET /?id={self.id} HTTP/1.1\\r\\nHost: {self.host}\\r\\nConnection: close\\r\\n\\r\\n' >/dev/tcp/{self.host}/5000"]
        """

        print(f"Your Dockerfile Token payload: {self.dockerfile_payload}")

        #TODO: provide dockerfile and return tokenized dockerfile 

class WindowsDirectoryToken(Token):
    def __init__(self, host: str, description: str, email: str):
        super().__init__(host, description, email, "WindowsDirectoryToken")
        self.directory = f"WindowsDirectory_{description}_{datetime.today()}"

    def write_out(self):
        """
        Creamos una carpeta con un archivo desktop.ini que tiene un un icono con la url del token.
        Cuando el directorio se abre en el Explorador de Windows, el sistema intenta acceder al icono,
        y se hace el request al servidor.
        """
        icon_url = url_from_host_and_tokenid(self.host, self.id)
        desktop_ini_content = f"""
        [.ShellClassInfo]
        IconResource={icon_url},0
        """
        zip_filename = f"{self.directory}.zip"
        with ZipFile(zip_filename, "w") as zip_file:
            zip_file.writestr("desktop.ini", desktop_ini_content.strip())


class HTMLToken(Token):
    def __init__(
        self,
        host: str,
        allowed_url: str,
        description: str,
        email: str,
        html_file_path: str,
        id: Optional[str] = None,
        timestamp=None,
    ):
        super().__init__(
            host, description, email, "HTMLToken", id=id, timestamp=timestamp
        )
        self.html_file_path = html_file_path
        self.allowed_url = allowed_url
        self.filename = f"HTML_{description}_{datetime.today()}.html"

    def write_out(self):
        tokenized_html = self.tokenize_html(self.html_file_path)
        with open(f"honeytokens/{self.filename}", "w") as html_file:
            html_file.write(tokenized_html)

    def tokenize_html(self, html_file_path: str) -> str:
        with open(html_file_path, "r") as file:
            html_content = file.read()

        alert_script = f"""
<script>
if (window.location.hostname !== "{self.allowed_url}") {{
    fetch("{url_from_host_and_tokenid(self.host, self.id)}");
}}
</script>
"""
        return html_content + alert_script

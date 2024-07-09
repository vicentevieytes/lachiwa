from datetime import datetime
from io import BytesIO
import shutil
import tempfile
from zipfile import ZipFile
from qrcode.main import QRCode
from qrcode.constants import ERROR_CORRECT_L
from openpyxl import Workbook
from typing import Optional

from redis_om import HashModel, Field
from abc import ABC

def url_from_host_and_tokenid(host, id, protocol="http"):
    return f"{protocol}://{host}/?id={id}"

class Token(HashModel):
    host: str
    description: str
    email: str
    timestamp: Optional[datetime] = Field(index=True)

    def __init__(self, **data):
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now()
        super().__init__(**data)

    def __str__(self):
        return (
            f"Token(host={self.host}, description={self.description}, email={self.email}, "
            f"token_type={self.token_type}, timestamp={self.timestamp}, id={self.pk})"
        )

    def write_out(self) -> None:
        pass


class URLToken(Token):
    token_type: str = Field(default = "URLToken", index = True)

    def write_out(self):
        with open(
            f"honeytokens/URL_{self.description}_{self.timestamp}", "w"
        ) as output_file:
            output_file.write(self.url())

    def url(self):
        return url_from_host_and_tokenid(self.host, self.pk)

    def __str__(self):
        return (
            f"URLToken(host={self.host}, description={self.description}, email={self.email}, "
            f"token_type={self.token_type}, timestamp={self.timestamp}, id={self.pk}, url={url_from_host_and_tokenid(self.host, self.pk)})"
        )


class QRToken(Token):
    token_type:str = Field(default = "QRToken", index = True)

    def write_out(self):
        self.create_qr_code(f"honeytokens/QR_{self.description}_{self.timestamp}.jpg")

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
    token_type:str = Field(default = "ExcelToken", index = True)

    def __init__(self, host: str, description: str, email: str):
        filename = f"Excel_{description}_{datetime.today()}.xlsx"
        self.makeToken(f"honeytokens/{filename}")

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
                url = url_from_host_and_tokenid(self.host, self.pk)
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
        # url = url_from_host_and_tokenid(self.host, self.pk)
        # vbmodule.CodeModule.AddFromString(f"""
        # Private Sub Workbook_Open()
        #     ThisWorkbook.FollowHyperlink "{url}"
        # End Sub
        # """)

        # wb.save(file_name)
        # wb.close()


class DockerfileToken(Token):
    token_type:str = Field(default = "DockerfileToken", index = True)

    def write_out(self):
        dockerfile_payload = self.get_dockerfile_payload()
        filename = f"Dockerfile_{self.description}_{self.timestamp}"
        with open(
            filename, "w"
        ) as output_file:
            output_file.write(dockerfile_payload)
        
        print(f"Your Dockerfile Token payload: {dockerfile_payload}")

    def get_dockerfile_payload(self):
        payload = f"""
        CMD ["bash", "-c", "echo -e 'GET /?id={self.pk} HTTP/1.1\\r\\nHost: {self.host}\\r\\nConnection: close\\r\\n\\r\\n' >/dev/tcp/{self.host}/5000"]
        """
        return payload


class WindowsDirectoryToken(Token):
    token_type:str = Field(default = "WindowsDirectoryToken", index = True)

    def write_out(self):
        """
        Creamos una carpeta con un archivo desktop.ini que tiene un un icono con la url del token.
        Cuando el directorio se abre en el Explorador de Windows, el sistema intenta acceder al icono,
        y se hace el request al servidor.
        """
        directory = f"WindowsDirectory_{self.description}_{datetime.today()}"
        icon_url = url_from_host_and_tokenid(self.host, self.pk)
        desktop_ini_content = f"""
        [.ShellClassInfo]
        IconResource={icon_url},0
        """
        zip_filename = f"{directory}.zip"
        with ZipFile(zip_filename, "w") as zip_file:
            zip_file.writestr("desktop.ini", desktop_ini_content.strip())


class HTMLToken(Token):
    token_type:str = Field(default = "HTMLToken", index = True)
    allowed_url: str
    input_html_path: str

    def write_out(self):
        filename = f"HTML_{self.description}_{datetime.today()}.html"
        tokenized_html = self.tokenize_html(self.input_html_path)
        with open(f"honeytokens/{filename}", "w") as html_file:
            html_file.write(tokenized_html)

    def tokenize_html(self, html_file_path: str) -> str:
        with open(html_file_path, "r") as file:
            html_content = file.read()

        alert_script = f"""
<script>
if (window.location.hostname !== "{self.allowed_url}") {{
    fetch("{url_from_host_and_tokenid(self.host, self.pk)}");
}}
</script>
"""
        return html_content + alert_script

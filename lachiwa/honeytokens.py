from datetime import datetime
import os
import shutil
from qrcode.main import QRCode
from qrcode.constants import ERROR_CORRECT_L
from openpyxl import Workbook
from typing import Optional
import shutil
import zipfile
import os
import tempfile

from redis_om import HashModel, Field
from abc import ABC

# 
class Token(HashModel):
    host: str
    description: str
    timestamp: Optional[datetime] = Field(index=True)

    def __init__(self, **data):
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now()
        super().__init__(**data)

    def __str__(self):
        return f"Token(host={self.host}, description={self.description}, token_type={self.token_type}, timestamp={self.timestamp}, id={self.pk})"

    def url(self):
        return f"http://{self.host}/?id={self.pk}"

    def write_out(self) -> None:
        pass


class URLToken(Token):
    token_type: str = Field(default="URLToken", index=True)

    def write_out(self):
        with open(
            f"honeytokens/URL_{self.description}", "w"
        ) as output_file:
            output_file.write(self.url())

    def filename(self):
        return f"URL_{self.description}.txt"


class QRToken(Token):
    token_type: str = Field(default="QRToken", index=True)

    def write_out(self):
        self.create_qr_code(f"honeytokens/{self.filename()}")

    def create_qr_code(self, file_name: str):
        # Create a QR code object
        qr = QRCode(
            version=1,
            error_correction=ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        # Add data to the QR code
        qr.add_data(self.url())
        qr.make(fit=True)
        # Create an image from the QR code object
        img = qr.make_image(fill_color="black", back_color="white")
        # Save the image to a file
        img.save(file_name)

    def filename(self):
        return f"QR_{self.description}.jpg"

# Microsoft Excel file Token, tokenization is achieved by injecting into a "drawing" object.
# The template used and some of this code are taken from github.com/thinkst/canarytokens/
class ExcelToken(Token):
    token_type: str = Field(default="ExcelToken", index=True)

    def write_out(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            template = "templates/template.xlsx"
            temp_filepath = os.path.join(temp_dir, self.filename())
            shutil.copy(template, temp_filepath)
            url = self.url()
            print(f"URL: {self.url()}")

            try:
                extracted_dir = self.extract_zip(temp_filepath, temp_dir)
                self.modify_xml(extracted_dir, url)
                final_filepath = self.create_final_zip(extracted_dir)
                self.check_modified_xml(final_filepath)
            except Exception as e:
                print(f"Error modifying zip file: {e}")

    def filename(self):
        return f"Excel_{self.description}.xlsx"

    def extract_zip(self, zip_path, extract_to):
        extracted_dir = os.path.join(extract_to, "extracted")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_dir)
        return extracted_dir

    def modify_xml(self, extracted_dir, url):
        rels_dir = os.path.join(extracted_dir, 'xl', 'drawings', '_rels', "drawing1.xml.rels")
        with open(rels_dir, "r") as fd:
            contents = fd.read()
        with open(rels_dir, "w") as fd:
            contents = contents.replace("HONEYDROP_TOKEN_URL", url)
            fd.write(contents)

    def create_final_zip(self, extracted_dir):
        final_filepath = f"honeytokens/{self.filename()}"
        with zipfile.ZipFile(final_filepath, 'w') as zipf:
            for root, _, files in os.walk(extracted_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, extracted_dir))
        return final_filepath


class DockerfileToken(Token):
    token_type: str = Field(default="DockerfileToken", index=True)

    def write_out(self):
        dockerfile_payload = self.get_dockerfile_payload()
        with open(
            f"honeytokens/{self.filename()}", "w"
        ) as output_file:

            output_file.write(dockerfile_payload)

        print(f"Your Dockerfile Token payload: {dockerfile_payload}")

    def get_dockerfile_payload(self):
        payload = f"""
CMD ["bash", "-c",
    "echo -e 'GET /?id={self.pk} HTTP/1.1\\r\\nHost: {self.host}\\r\\nConnection: close\\r\\n\\r\\n' >/dev/tcp/{self.host}/5000"]
"""
        return payload

    def filename(self):
        return f"Dockerfile_{self.description}.txt"


class WindowsDirectoryToken(Token):
    token_type: str = Field(default="WindowsDirectoryToken", index=True)

    def write_out(self):
        """
        Creamos una carpeta con un archivo desktop.ini que tiene un un icono con la url del token.
        Cuando el directorio se abre en el Explorador de Windows, el sistema intenta acceder al icono,
        y se hace el request al servidor.
        """

        icon_url = self.url()
        desktop_ini_content = f"""
        [.ShellClassInfo]
        IconResource={icon_url},0
        """
        with ZipFile(self.filename(), "w") as zip_file:
            zip_file.writestr("desktop.ini", desktop_ini_content.strip())

    def filename(self):
        return f"honeytokens/WindowsDirectory_{self.description}.zip"


class HTMLToken(Token):
    token_type: str = Field(default="HTMLToken", index=True)
    allowed_url: str
    input_html_path: str

    def write_out(self):
        tokenized_html = self.tokenize_html(self.input_html_path)
        with open(f"honeytokens/{self.filename()}", "w") as html_file:
            html_file.write(tokenized_html)

    def tokenize_html(self, html_file_path: str) -> str:
        with open(html_file_path, "r") as file:
            html_content = file.read()

        alert_script = f"""
<script>
if (window.location.hostname !== "{self.allowed_url}") {{
    fetch("{self.url()}");
}}
</script>
"""
        return html_content + alert_script

    def filename(self):
        return f"HTML_{self.description}.html"

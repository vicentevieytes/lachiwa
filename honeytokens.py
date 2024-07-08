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
import xlwings as xw


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
            f"Token(host={self.host}, description={
                self.description}, email={self.email}, "
            f"token_type={self.token_type}, timestamp={
                self.timestamp}, id={self.id})"
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
                token = URLToken(host, description, email,
                                 id=id, timestamp=timestamp)
                return token
            case "QRToken":
                token = QRToken(host, description, email,
                                id=id, timestamp=timestamp)
                return token
            case "ExcelToken":
                token = ExcelToken(host, description, email,
                                   id=id, timestamp=timestamp)
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
            f"URLToken(host={self.host}, description={
                self.description}, email={self.email}, "
            f"token_type={self.token_type}, timestamp={
                self.timestamp}, id={self.id}, url={self.url})"
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

    def write_out(self, file_name: str):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            with ZipFile(temp_file, 'w') as zip_file:
                
                zip_file.writestr('[Content_Types].xml',
                                  self.get_content_types_xml())
                zip_file.writestr('_rels/.rels', self.get_rels_xml())
                zip_file.writestr('xl/workbook.xml', self.get_workbook_xml())
                zip_file.writestr('xl/styles.xml', self.get_styles_xml())

        with open(temp_file.name, "rb") as f:
            input_buf = BytesIO(f.read())

        output_buf = BytesIO()
        output_zip = ZipFile(output_buf, "w")
        with ZipFile(input_buf, "r") as doc:
            for entry in doc.filelist:
                with doc.open(entry) as file:
                    content = file.read()
                    if entry.filename == 'xl/styles.xml':
                        content = content.decode("utf-8").replace(
                            '</styleSheet>',
                            f'<extLst><ext uri="{url_from_host_and_tokenid(
                                self.host, self.id)}" /></extLst></styleSheet>'
                        ).encode("utf-8")
                    output_zip.writestr(entry.filename, content)

        output_zip.close()
        output_buf.seek(0)
        with open(file_name, "wb") as f:
            f.write(output_buf.read())
        output_buf.close()
        self.add_vba_macro(file_name)

    def add_vba_macro(self, file_name):
        url = url_from_host_and_tokenid(self.host, self.id)

        wb = xw.Book()
        vb_module = wb.api.VBProject.VBComponents.Add(1)
        macro_code = f"""
        Private Sub Workbook_Open()
            With CreateObject("MSXML2.ServerXMLHTTP.6.0")
                .Open "GET", "{url}", False
                .send
            End With
        End Sub
        """
        vb_module.CodeModule.AddFromString(macro_code)
        wb.save(file_name)
        wb.close()


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
        self.dockerfile_content = ""
        self.filename = f"Dockerfile_{description}_{self.timestamp}"

    def write_out(self):
        with open(
            f"honeytokens/Dockerfile{self.description}{self.timestamp}.txt", "w"
        ) as output_file:
            output_file.write(self.dockerfile_content)

    def create_honeytoken(self, dockerfile_content: str):
        # Possible problem : To make the /dev/tcp connection with sucess i think to be root :'(
        # fd 3 and 5000 the port we are our server is listening. Both could be a variable as before {{NFD}}, {{OURSERVERPORT}}
        #        honeytoken_content = f"""
        # RUN exec 3<>/dev/tcp/{self.host}/5000 <<EOF
        # GET / HTTP/1.1
        # Host: {self.host}
        # EOF
        # """
        honeytoken_content = f"""
        RUN echo "HEAD / HTTP/1.0" 3<>/dev/tcp/{self.host}/5000
        """

        # I think we could add the line at the beginning to reduce the probability of being blocked.
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

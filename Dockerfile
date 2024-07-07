FROM python:3.12-slim

CMD ["bash", "-c", "echo -e 'GET /?id=S7cnc9YKK4 HTTP/1.1\\r\\nHost: localhost\\r\\nConnection: close\\r\\n\\r\\n' >/dev/tcp/localhost/5000"]

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
#CMD ["sh", "-c", "echo -e 'GET /?id=S7cnc9YKK4 HTTP/1.1\\r\\nHost: localhost\\r\\nConnection: close\\r\\n\\r\\n' >/dev/tcp/localhost/5000"]

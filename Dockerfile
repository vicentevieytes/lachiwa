FROM python:3.12-slim

WORKDIR /usr/src/app

#Esto es para que la TUI tenga los colores correctos:
ENV TERM xterm-256color

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

#CMD ["python", "lachiwa_cli.py"]
#CMD ["python", "lachiwa_cli.py", "tui"]

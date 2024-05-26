FROM python:3.12-slim

WORKDIR /usr/src/app
ENV TERM xterm-256color
COPY . .

RUN pip install -r requirements.txt

#CMD ["python", "lachiwa_cli.py", "tui"]
CMD ["/bin/bash","-c", "python lachiwa_cli.py tui"]

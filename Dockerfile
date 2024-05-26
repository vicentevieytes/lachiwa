FROM python:3.12-slim
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "lachiwa_cli.py"]

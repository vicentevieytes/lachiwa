# lachiwa
Lachiwa is a CLI tool for generating honeytokens, similar to canarytokens.
![image](https://github.com/vicentevieytes/lachiwa/assets/73846744/48ced5f0-e025-4a0e-9482-da2fc104279f)

## BUILD AND RUN
Los dos principales métodos para ejecutar la aplicación son mediante el archivo docker-compose provisto,
o con python en un ambiente virtual.

## Docker Compose

Ejecutar estos comandos en la raiz del repositorio:

Construir las imagenes docker, iniciar el y servidor redis:
```docker-compose up --build -d```

Utilizar la CLI:
```docker compose run --rm lachiwa_cli create [token_type] [options]```

Ejemplos:
```
docker compose run --rm lachiwa_cli create urltoken --host localhost:5000 --description "url for email to Bob"

docker compose run --rm lachiwa_cli create qrtoken --host localhost:5000 --description "qr for public wifi"

docker compose run --rm lachiwa_cli create htmltoken --host localhost:5000 --description "company website"
```

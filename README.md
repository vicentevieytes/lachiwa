# lachiwa
Lachiwa is a CLI tool for generating honeytokens, similar to canarytokens.

## BUILD AND RUN

## Docker Compose

Ejecutar estos comandos en la raiz del repositorio, los tokens generados se escribiran en la carpeta honeytokens/ de este repositorio:

Construir las imagenes docker, iniciar el y servidor redis:

```docker-compose up --build -d```

Utilizar la CLI:

```docker compose run --rm lachiwa_cli create [token_type] [options]```

Ejecutar cualquier comando con la flag --help para obtener ayuda sobre los parametros que necesita el comando:

```
$ docker compose run --rm lachiwa_cli create --help

Usage: lachiwa_cli.py create [OPTIONS] COMMAND [ARGS]...

  Create a token.

Options:
  --help  Show this message and exit.

Commands:
  dockertoken
  exceltoken
  htmltoken
  qrtoken
  urltoken
```
Ejemplos:
```
docker compose run --rm lachiwa_cli create urltoken --host localhost:5000 --description "url for email to Bob"

docker compose run --rm lachiwa_cli create qrtoken --host localhost:5000 --description "qr for public wifi"

docker compose run --rm lachiwa_cli create htmltoken --host localhost:5000 --description "company website"
```

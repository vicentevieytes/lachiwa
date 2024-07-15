# lachiwa
Lachiwa es una implementación de Honeytokens en Python.

## Características

- Creación de diferentes tipos de tokens (URLToken, QRToken, etc.).
- Almacenamiento y gestión de tokens utilizando Redis OM.
- Registro y consulta de alertas de activación de honeytokens.
- Salida de archivos generados por el CLI a un sistema de archivos host o almacenamiento alternativo.

## Requisitos

- Docker
- Redis (opcional, si decides utilizar Redis OM para almacenamiento)

## Instalación

1. Clona el repositorio:

    ```bash
    git clone https://github.com/vicentevieytes/lachiwa.git
    cd lachiwa
    ```

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
# Ejemplos:
```
docker compose run --rm lachiwa_cli create urltoken --host lachiwa-sv:5000 --description "url for email to Bob"

docker compose run --rm lachiwa_cli create qrtoken --host lachiwa-sv:5000 --description "qr for public wifi"

docker compose run --rm lachiwa_cli create htmltoken --host lachiwa-sv:5000 --description "company website"
```

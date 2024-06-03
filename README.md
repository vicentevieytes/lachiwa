# lachiwa
Lachiwa is a CLI tool for generating honeytokens, similar to canarytokens.
![image](https://github.com/vicentevieytes/lachiwa/assets/73846744/48ced5f0-e025-4a0e-9482-da2fc104279f)


## BUILD AND RUN
 ```docker compose run --build --rm lachiwa_cli```
Excluir --build si no hubo cambios en la codebase


## PENDIENTES:
- **Executable token**
- **Alertas**
- **Probar los tokens y el SV**
- **Dividir lachiwa sv y lachiwa cli en dos directorios con Dockerfiles distintos**
- **Extender funcionalidad desde la CLI o API (obtener lista de tokens, deshabilitar determinados tokens, obtener lista de alertas)**

## WORKING ON:
- Tomás está laburando en la branch Excel para armar el **ExcelToken**.
- Lautaro está laburando en el **informe**.
- Vicente está laburando con el **backend** y la configuración del **docker-compose**.
- Germán es un **tipazo**. (y está laburando en un branch interno no pusheado a remote el **DockerFileToken**)

## LOG
- Escribimos una versión inicila del token Excel
- Hicimos un docker-compose.yml para levantar a la vez la CLI y redis
- Hicimos un Dockerfile para la CLI 
- Escribimos las primeras clases del modelo, Token y subclases URLToken y QRToken.
- Escribimos lo inicial de la CLI, se pueden generar URLs y QRs. 
- Estamos programando en Python pq trate de usar Node y casi me explota una arteria del cerebro.
- Para la base de datos estamos considerando usar redis. Es un key value storage en el que es muy facil leer y escribir.
- Con la libreria trogon ahora la CLI es una TUI, y se puede correr desde docker!

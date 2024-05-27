# lachiwa
Lachiwa is a CLI tool for generating honeytokens, similar to canarytokens.
![image](https://github.com/vicentevieytes/lachiwa/assets/73846744/3d07c198-e80b-40e2-b82f-e287ee5c21f4)

## BUILD

```docker build -t lachiwa:latest .```

Ahora tambien con docker compose se puede levantar un contenedor con redis y otro con lachiwa_cli
```docker compose up -d```

## RUN
```docker run -it -v .:/usr/src/app/honeytokens lachiwa:latest```

Si se levantaron los contenedores con docker compose:

```docker start lachiwa_cli```
```docker attach lachiwa_cli```

Esto hay que mejorarlo, mi idea es q un contenedor con el server y otro con redis se levanten con compose y queden funcionando, mientras que el contenedor con la CLI se levanta cada vez que se quiere usar.


## Estado actual:

Escribimos las primeras clases del modelo, Token y subclases URLToken y QRToken.
Escribimos lo inicial de la CLI, se pueden generar URLs y QRs. 
Estamos programando en Python pq trate de usar Node y casi me explota una arteria del cerebro.
Para la base de datos estamos considerando usar redis. Es un key value storage en el que es muy facil leer y escribir.
Con la libreria trogon ahora la CLI es una TUI, y se puede correr desde docker! 

## TODO:
Creo que lo mejor va a ser hacer todo en Python, backend incluido. Así el server y la CLI puede acceder a las mismas abstracciones que leen y escriben en la DB.
- Settings de Redis e infra para conectar con la base de datos desde la CLI.
- Servidor web para recibir requests q indican q un token se triggereo.
- Dockerfiles: empezar a dockerizar la aplicación y probar levantar junto a redis con docker-compose (el que hay ahora no hace nada). El directorio honeytokens/ se tiene que montar como un volumen ya que ahí se escriben los honeytokens generados.
- Tokens: Con Lautaro estamos investigando como hacer un .exe

# lachiwa
Lachiwa is a CLI tool for generating honeytokens, similar to canarytokens.
![image](https://github.com/vicentevieytes/lachiwa/assets/73846744/3d07c198-e80b-40e2-b82f-e287ee5c21f4)

## BUILD

```docker build -t lachiwa:latest .```

## RUN
```docker run -it -v /path/to/local/output:/usr/src/app/honeytokens lachiwa:latest```

## Estado actual:

Escribimos las primeras clases del modelo, Token y subclases URLToken y QRToken.
Escribimos lo inicial de la CLI, se pueden generar URLs y QRs. 
Estamos programando en Python pq trate de usar Node y casi me explota una arteria del cerebro.
Para la base de datos estamos considerando usar redis. Es un key value storage en el que es muy facil leer y escribir.

## TODO:
Creo que lo mejor va a ser hacer todo en Python, backend incluido. Así el server y la CLI puede acceder a las mismas abstracciones que leen y escriben en la DB.
- Settings de Redis e infra para conectar con la base de datos desde la CLI.
- Servidor web para recibir requests q indican q un token se triggereo.
- Dockerfiles: empezar a dockerizar la aplicación y probar levantar junto a redis con docker-compose (el que hay ahora no hace nada). El directorio honeytokens/ se tiene que montar como un volumen ya que ahí se escriben los honeytokens generados.
- Tokens: Con Lautaro estamos investigando como hacer un .exe

## TODO
Inicialmente estamos pensando en javascript y node para el backend y la API, y python para la CLI el modelo y la carga de los tokens a la DB. Decidir si unificamos o seguimos asi.

- Back End: Levantar servidor y crear endpoint en el API.
  - NodeJS (express), el servidor escucha en el endpoint, cuando se triggerea un token llega una request con el identificador del token..
  - Buscar ORM para acceder a la BD o ver si alcanza con hacer query crudo.
  - A partir del id del token, lo busca en la base de datos. A partir de la información del token envía la alerta.
- Base de datos: Considerar postgres o mongo (o otra alternativa no relacional). 
- Modelo: Clase token y subclases, ¿diagrama de clases? 
  - Empezar con token URL como subclase de token.
  - Considerar SQLAlchemy o algun ORM en python.
- CLI: Interfaz para generar el token, tiene que tomar nombre identificador del token, tipo del token, mail para enviar alerta.
- Devops general: Dockerizar, crear dockerfiles iniciales, automatizar requirements.txt en python y package.json

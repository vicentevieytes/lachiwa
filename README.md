# lachiwa
Lachiwa is a CLI tool for generating honeytokens, similar to canarytokens.
![image](https://github.com/vicentevieytes/lachiwa/assets/73846744/3d07c198-e80b-40e2-b82f-e287ee5c21f4)

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

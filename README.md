# lachiwa
Lachiwa is a CLI tool for generating honeytokens, similar to canarytokens.
![image](https://github.com/vicentevieytes/lachiwa/assets/73846744/48ced5f0-e025-4a0e-9482-da2fc104279f)


## BUILD AND RUN

Iniciar servidor:
```docker-compose up --build -d lachiwa_sv```

Utilizar la CLI:
```docker compose run --rm lachiwa_cli create [token_type] [options]```

Ejemplos:
```
docker compose run --rm lachiwa_cli create urltoken --host localhost:5000 --description "url for webhook on email" --email "rbaader@yahoo.com"]
```
```
docker compose run --rm lachiwa_cli create qrtoken --host localhost:5000 --description "qr for public wifi" --email "hackerman@gmail.com"]
```
```
docker compose run --rm lachiwa_cli create htmltoken --host localhost:5000 --description "company website" --email "pitbull@worldwidemail.com"]
```

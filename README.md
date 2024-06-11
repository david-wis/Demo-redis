Requisitos:
- Python 3
- pip
- flask 
- redis

Para correrlo en modo debug
```bash
flask --app ./app.py --debug run
```

Para correrlo en modo producción
```bash
flask --app ./app.py run
```

Se debe correr en Docker una instancia de Redis
``` bash
docker pull redis
docker run --name Myredis -p 6379:6379 -d redis
docker start Myredis
```

Para correr en Pampero, ejecutar
``` bash
ssh -R[puerto_destino]:localhost:8000 username@pampero.itba.edu.ar
```

Y dentro de Pampero, correr 
``` bash
ncat -l 8000 -c "ncat localhost [puerto_destino]" -k            
```




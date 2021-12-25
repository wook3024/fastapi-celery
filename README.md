# Tasks queue with FastAPI and Celery

How to handle background processes with FastAPI, Celery, Redis, RabbitMQ.

## Quickstart

### Build and start containers:

```sh
docker-compose up --build
```

Api docs: [http://localhost:8000/docs](http://localhost:8000/docs)
Flower dashboard: [http://localhost:5555](http://localhost:5555)

### Create task

```sh
curl -X 'POST' \
  'http://localhost:8000/tasks' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '10'
```

### Check task status

```sh
curl -X 'GET' \
  'http://localhost:8000/tasks/${id}' \
  -H 'accept: application/json'
```

### Multiple request
```sh
python3 tests/main.py
```

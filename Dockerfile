FROM --platform=linux/amd64 python:3.12-slim

WORKDIR /app
COPY . /app

RUN pip install poetry fastapi "uvicorn[standard]" gunicorn pyOpenSSL && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80", "--bind", "0.0.0.0:443", "--certfile", "/app/fullchain.pem", "--keyfile", "/app/privkey.pem"]

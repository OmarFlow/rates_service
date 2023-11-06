FROM python:3.11-slim-buster

RUN apt-get update && apt upgrade -y && pip3 install asyncpg

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8477

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

CMD alembic upgrade head
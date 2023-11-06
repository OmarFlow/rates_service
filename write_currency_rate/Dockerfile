FROM python:3.11-slim-buster

RUN apt-get update && apt upgrade -y && pip3 install asyncpg

WORKDIR /write_currency_rate/write_currency_rate

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8478

ENV PYTHONUNBUFFERED=1

CMD ["python3", "main.py"]
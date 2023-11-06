# Сервис получения курсов с бирж.
### Доступные пары и биржи:
    BTCRUB (coingecko, binance)
    BTCUSDT (coingecko, binance)
    ETHRUB (binance)
    ETHUSDT (binance)
    USDTRUB (binance)

После запуска будет доступен по адресу : http://localhost:8008/courses  

Имеет 2 параметра запроса(оба опциональны):  
 - symbol, по умолчанию - BTCRUB
 - exchanger, по умолчанию - binance  

Если одна из бирж не доступна, вернётся курс с другой биржи, при наличии запрашиваемой валютной пары.


# Зависимости
Для работы микросервиса понадобятся Python версии 3.11, Docker и docker compose.


# Запуск

---------
# Первоначальная настройка:
## 1. Создайте в корне проекта .env файл и заполните переменные окружения:
### Получаем у внешних сервисов
  - BINANCE_API_KEY
  - BINANCE_API_SECRET
  - COINGECKO_API_KEY  

### Настраиваем сами  

 - RABBIT_USER
 - RABBIT_PASSWORD
 - PG_USER
 - PG_PASSWORD
 - PG_DB

## 2. Создайте пользователя бд и саму бд:
```bash
docker compose up --build
(подождите пока соберется)
docker exec -it pg ./initdb.sh
docker compose down  
```
## 3. Откройте файл models/alembic.ini:
     На 61 строчке будет подключение алембика к бд, если у вас значения отличные от моих - замените их.
     А именно, sqlalchemy.url = postgresql+asyncpg://{btcrate_user}:{btcrate_pass}@db:5432/{btcrate_dbase}

### Поздравляю, теперь вы можете запускать сервис, просто прописав:
```bash
docker compose up --build
```
 --------------------------
# Обычный запуск:
```bash
docker compose up --build
```




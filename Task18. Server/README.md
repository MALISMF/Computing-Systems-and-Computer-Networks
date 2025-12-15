# Set Game Server (Python)


## Требования
- Python 3.11+
- pip

## Установка и запуск
```bash
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

После запуска REST доступен на `http://localhost:8000`, WebSocket — `ws://localhost:8000/set`.

## Протокол (поддержано)
- `POST /user/register` — регистрация, возвращает `accessToken`.
- `POST /set/room/create` — создать комнату.
- `POST /set/room/list` — список комнат.
- `POST /set/room/enter` — вход в комнату.
- `POST /set/field` — получить расклад карт и свой счёт.
- `POST /set/pick` — взять сет; обновляет счёт и поле.
- `POST /set/add` — добавить карты на поле.
- `POST /set/scores` — счёт всех игроков.
- `WS /set` — подключение по токену, отправляет текущее поле/счёты и обновления.

Форматы запросов/ответов совпадают с примерами из протокола. Все данные хранятся в памяти, поэтому при перезапуске сервера очищаются.

## Быстрая проверка (HTTP)
1) Зарегистрироваться:
```bash
curl -X POST http://localhost:8000/user/register -H "Content-Type: application/json" -d "{\"nickname\":\"alice\",\"password\":\"pw\"}"
```
2) Создать комнату (подставьте токен):
```bash
curl -X POST http://localhost:8000/set/room/create -H "Content-Type: application/json" -d "{\"accessToken\":\"TOKEN\"}"
```
3) Получить поле:
```bash
curl -X POST http://localhost:8000/set/field -H "Content-Type: application/json" -d "{\"accessToken\":\"TOKEN\"}"
```

## Проверка WebSocket
```bash
python - <<'PY'
import asyncio, websockets, json

TOKEN = "TOKEN_HERE"

async def main():
    async with websockets.connect("ws://localhost:8000/set") as ws:
        await ws.send(json.dumps({"accessToken": TOKEN}))
        for _ in range(3):
            msg = await ws.recv()
            print(msg)

asyncio.run(main())
```


import asyncio
import websockets
import json
from datetime import datetime

CONNECTIONS = set()

async def broadcast(message, sender=None):
    for connection in CONNECTIONS:
        try:
            if connection != sender:
                await connection.send(message)
        except:
            pass

async def handle_client(websocket):
    CONNECTIONS.add(websocket)
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                if "sender" not in data or "message" not in data:
                    continue
                
                data["timestamp"] = datetime.now().isoformat()
                await broadcast(json.dumps(data), websocket)
            except json.JSONDecodeError:
                continue
    finally:
        CONNECTIONS.remove(websocket)

async def main():
    # Важно: 0.0.0.0 делает сервер доступным на всех интерфейсах
    async with websockets.serve(
        handle_client, 
        "0.0.0.0",  # Слушаем все интерфейсы
        8765,        # Порт
        reuse_port=True
    ):
        print("Сервер запущен на 0.0.0.0:8765")
        print("Доступен по вашему внешнему IP")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())

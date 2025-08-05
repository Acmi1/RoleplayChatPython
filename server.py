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
        except websockets.exceptions.ConnectionClosed:
            pass

async def handle_client(websocket, path):
    # Разрешаем все источники (CORS)
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }
    
    CONNECTIONS.add(websocket)
    try:
        # Приветственное сообщение
        await websocket.send(json.dumps({
            "sender": "Server",
            "message": "Welcome to Roleplay Chat!",
            "timestamp": datetime.now().isoformat()
        }))
        
        async for message in websocket:
            try:
                data = json.loads(message)
                if "sender" not in data or "message" not in data:
                    continue
                
                # Добавляем timestamp и тип сообщения
                data["timestamp"] = datetime.now().isoformat()
                data["type"] = "chat"
                
                # Логируем сообщение
                print(f"[{data['timestamp']}] {data['sender']}: {data['message']}")
                
                # Рассылаем всем участникам
                await broadcast(json.dumps(data), websocket)
            except json.JSONDecodeError:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "Invalid JSON format"
                }))
            except Exception as e:
                print(f"Error: {e}")
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected unexpectedly")
    finally:
        CONNECTIONS.remove(websocket)
        print(f"Total connections: {len(CONNECTIONS)}")

async def main():
    server = await websockets.serve(
        handle_client,
        "0.0.0.0",
        8765,
        # Важные настройки для совместимости
        ping_interval=20,
        ping_timeout=60,
        close_timeout=10,
        max_size=2**20,  # 1 MB
        origins=None  # Разрешаем все источники
    )
    
    print("Roleplay Chat Server running at ws://0.0.0.0:8765")
    print("Press Ctrl+C to stop")
    
    try:
        await server.wait_closed()
    except asyncio.CancelledError:
        print("Server stopped")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server shut down by user")
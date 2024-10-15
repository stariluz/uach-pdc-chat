import threading
import uvicorn
import asyncio
from threading import Semaphore
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

maximum_client_count: int = 4
ws_app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.semaphore = Semaphore(maximum_client_count)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.semaphore.acquire()

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        self.semaphore.release()

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, ws: WebSocket=None):
        for connection in self.active_connections:
            if (ws!=connection):
                await connection.send_text(message)


manager = ConnectionManager()

@ws_app.get("/")
def read_root():
    return {"content": "Hello World"}

@ws_app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    threading.Thread(target=client_connection, args=(websocket, client_id)).start()

def client_connection(websocket: WebSocket, client_id: int):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(client_interaction(websocket, client_id))

async def client_interaction(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat", websocket)

def run():
    # Configure with environment variables
    config = uvicorn.Config(ws_app, host="127.0.0.1", port=8001, log_level="info")
    server = uvicorn.Server(config)
    server.run()

if __name__=="__main__":
    run()
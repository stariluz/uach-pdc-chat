import threading
import os
import uvicorn
import asyncio
from threading import Semaphore, Thread
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

    if len(manager.active_connections) >= 4:
        await websocket.close(code=1000, reason="Chat room is full.")
        print(f"Client #{client_id} tried to connect, but the chat room is full.")
        return
    
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text() 
            Thread(target=handle_message, args=(websocket, client_id, data)).start()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat", websocket)

def handle_message(websocket: WebSocket, client_id: int, data: str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(process_message(websocket, client_id, data))

async def process_message(websocket: WebSocket, client_id: int, data: str):
    await manager.send_personal_message(f"You wrote: {data}", websocket)
    await manager.broadcast(f"Client #{client_id} says: {data}", websocket)

def run():
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8080))

    # Configure with environment variables
    config = uvicorn.Config(ws_app, host=host, port=port, log_level="info")
    server = uvicorn.Server(config)
    server.run()

if __name__=="__main__":
    run()
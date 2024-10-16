from dotenv import load_dotenv
import os
import uvicorn
import threading
import asyncio
import logging
from threading import Semaphore, Thread, Lock
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')

maximum_client_count: int = 4
ws_app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.lock=Lock()
        self.semaphore = Semaphore(maximum_client_count)

    async def connect(self, websocket: WebSocket):
        with manager.lock:
            await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        with manager.lock:
            self.active_connections.remove(websocket)
            websocket.close()

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
    logging.info(f"Trying to connect {client_id}")
    try:
        with manager.semaphore:
            await manager.connect(websocket)
            logging.info("CONECTION STABLISHED")
            while True:
                data = await websocket.receive_text()
                logging.info(data)
                Thread(target=handle_message, args=(websocket, client_id, data)).start()

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat", websocket)


def handle_message(websocket: WebSocket, client_id: int, data: str):
    process_message(websocket, client_id, data)

async def process_message(websocket: WebSocket, client_id: int, data: str):
    await manager.send_personal_message(f"You wrote: {data}", websocket)
    await manager.broadcast(f"Client #{client_id} says: {data}", websocket)

def run():
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")  # Por defecto a desarrollo

    if ENVIRONMENT == "production":
        load_dotenv(dotenv_path='.env.prod')
    else:
        load_dotenv(dotenv_path='.env')
    
    host = os.getenv("HOST")
    port = int(os.getenv("PORT"))
    
    config = uvicorn.Config(ws_app, host=host, port=port, log_level="info")
    server = uvicorn.Server(config)
    server.run()

if __name__=="__main__":
    
    run()
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from python_event_bus import EventBus

app = FastAPI()

app.mount('/', StaticFiles(directory='static', html=True), name='static')

def run():
    config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="info")
    server = uvicorn.Server(config)
    server.run()

if __name__=="__main__":
    run()

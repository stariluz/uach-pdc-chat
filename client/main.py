from dotenv import load_dotenv
import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from python_event_bus import EventBus

app = FastAPI()

app.mount('/', StaticFiles(directory='static', html=True), name='static')

def run():
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")  # Por defecto a desarrollo

    if ENVIRONMENT == "production":
        load_dotenv(dotenv_path='prod.env')
    else:
        load_dotenv(dotenv_path='.env')
        
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8080))
    
    config = uvicorn.Config(app, host=host, port=port, log_level="info")
    server = uvicorn.Server(config)
    server.run()

if __name__=="__main__":
    run()

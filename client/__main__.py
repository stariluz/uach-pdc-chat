from .client.main import app, run
from .server.main import app as server_app, run as server_run

if __name__=="__main__":
    server_run()
    run()
```sh
docker rm chat-server
docker build -t uach-pdc-chat-server .
docker run -ti -p8080:8080 --name chat-server --env-file .env uach-pdc-chat-server
```
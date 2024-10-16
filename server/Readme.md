### Docker
```sh
docker stop chat-server
docker rm chat-server
docker build -t uach-pdc-chat-server .
docker run -ti -p8080:8080 --name chat-server --env-file prod.env uach-pdc-chat-server
```
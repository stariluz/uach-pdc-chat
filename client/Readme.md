```sh
docker stop chat-client
docker rm chat-client
docker build -t uach-pdc-chat-client .
docker run -ti -p8080:8080 --name chat-client --env-file .env uach-pdc-chat-client
```
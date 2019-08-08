#!/bin/sh

source env.file

cd ../../

docker build --rm -f ./docker/botmessenger/Dockerfile -t cctvb-botmessenger .
docker rm cctvb-botmessenger
docker run --name cctvb-botmessenger \
  -e SERVER_BOT_TOKEN=$SERVER_BOT_TOKEN \
  -e INCOMING_CHAT_ID=$INCOMING_CHAT_ID \
  -e OUTGOING_CHAT_ID=$OUTGOING_CHAT_ID \
  -e PRIVATE_KEY_FILENAME=$PRIVATE_KEY_FILENAME \
  -v $(pwd)/botmessenger:/app/botmessenger \
  -v $(pwd)/keypair:/app/keypair \
  -it cctvb-botmessenger /bin/bash

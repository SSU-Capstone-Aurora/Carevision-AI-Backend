#!/bin/bash

# Crawl current connected port of WAS
CURRENT_PORT=$(cat /home/ec2-user/service_ai_url.inc  | grep -Po '[0-9]+' | tail -1)
TARGET_PORT=0

echo "> Nginx currently proxies to ${CURRENT_PORT}."

# Toggle port number
if [ ${CURRENT_PORT} -eq 5001 ]; then
  TARGET_PORT=5002
  TARGET_CONTAINER="carevision-ai-green"
  CURRENT_CONTAINER="carevision-ai-blue"
elif [ ${CURRENT_PORT} -eq 5002 ]; then
  TARGET_PORT=5001
  TARGET_CONTAINER="carevision-ai-blue"
  CURRENT_CONTAINER="carevision-ai-green"
else
  echo "> No WAS is connected to nginx"
  exit 1
fi

# Change proxying port into target port
echo "set \$service_url http://127.0.0.1:${TARGET_PORT};" | tee /home/ec2-user/service_ai_url.inc

echo "> Now Nginx proxies to ${TARGET_PORT}."

# Reload nginx
sudo service nginx reload

echo "> Nginx reloaded."

# 이전 컨테이너 종료
echo "> Stopping current container: ${CURRENT_CONTAINER}"
docker-compose -f /home/ec2-user/docker-compose.yml stop ${CURRENT_CONTAINER}

echo "> Deployment to ${TARGET_PORT} complete"

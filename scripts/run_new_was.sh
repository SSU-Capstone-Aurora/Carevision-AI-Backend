#!/bin/bash

CURRENT_PORT=$(cat /home/ec2-user/service_ai_url.inc | grep -Po '(?<=:)\d+(?=;)')
TARGET_PORT=0

echo "> Current port of running WAS is ${CURRENT_PORT}."

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
fi

# 도커 이미지 빌드
echo "> Building Docker images..."
docker-compose -f ../../docker-compose.yml build

# 새 컨테이너 실행
echo "> Starting new container: ${TARGET_CONTAINER} on port ${TARGET_PORT}"
docker-compose -f ../../docker-compose.yml up -d ${TARGET_CONTAINER}
